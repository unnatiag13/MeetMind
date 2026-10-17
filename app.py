import email.mime.multipart
import email.mime.text
import os
import smtplib
import urllib.parse
from datetime import datetime, timedelta
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
from pydantic import BaseModel, Field

load_dotenv()

# Verify key exists
groq_key = os.getenv("GROQ_API_KEY")

if not groq_key:
    st.error("Missing GROQ_API_KEY! Please check your .env file.")
    st.stop()

# 2. INITIALIZE CLIENT
client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=groq_key,
)

SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")

# 2. Pydantic Schemas
class ActionItem(BaseModel):
    task: str = Field(description="Description of the task")
    owner: str = Field(description="Person assigned to this task")
    deadline: str = Field(description="Target deadline for the task")


class MeetingSummary(BaseModel):
    summary: str = Field(description="A concise 2-3 sentence overview of the meeting")
    decisions: list[str] = Field(description="Key decisions made during the meeting")
    action_items: list[ActionItem] = Field(description="List of extracted action items")


# 3. SMTP Email Function
def send_email_via_smtp(recipient_list, subject, html_content):
    msg = email.mime.multipart.MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = SENDER_EMAIL
    msg["To"] = ", ".join(recipient_list)

    msg.attach(email.mime.text.MIMEText(html_content, "html"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, recipient_list, msg.as_string())


# 4. Google Calendar URL Builder
def generate_gcal_link(title, start_dt, end_dt, details, attendees):
    base_url = "https://calendar.google.com/calendar/render?action=TEMPLATE"
    fmt = "%Y%m%dT%H%M%SZ"
    params = {
        "text": title,
        "dates": f"{start_dt.strftime(fmt)}/{end_dt.strftime(fmt)}",
        "details": details,
        "add": ",".join(attendees),
    }
    return f"{base_url}&{urllib.parse.urlencode(params)}"


# 5. UI Layout
st.set_page_config(page_title="MeetMind Free MVP", page_icon="📝", layout="wide")
st.title("MeetMind — Free Meeting Intelligence Agent")

st.sidebar.header("Meeting Setup")
recipient_emails = st.sidebar.text_input(
    "Participant Emails (comma-separated)",
    placeholder="alice@example.com, bob@example.com",
)
followup_date = st.sidebar.date_input("Follow-up Date", datetime.now() + timedelta(days=7))
followup_time = st.sidebar.time_input("Follow-up Time", datetime.strptime("10:00", "%H:%M").time())

transcript_input = st.text_area(
    "Paste Meeting Transcript",
    height=250,
    placeholder="Alice: Let's release the feature on Friday. Bob will test the endpoints by Wednesday...",
)

if st.button("Process Meeting", type="primary"):
    if not transcript_input:
        st.error("Please enter a transcript.")
    else:
        with st.spinner("Extracting insights using Groq (Llama 3.3)..."):
            try:
                response = client.beta.chat.completions.parse(
                    model="openai/gpt-oss-120b",
                    messages=[
                        {
                            "role": "system",
                            "content": "You are MeetMind. Extract structured meeting summaries, decisions, and action items.",
                        },
                        {"role": "user", "content": transcript_input},
                    ],
                    response_format=MeetingSummary,
                )
                st.session_state["result"] = response.choices[0].message.parsed
            except Exception as e:
                st.error(f"Error processing with Groq: {e}")

if "result" in st.session_state:
    data = st.session_state["result"]

    st.subheader("1. Executive Summary")
    st.write(data.summary)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("2. Key Decisions")
        for decision in data.decisions:
            st.markdown(f"- {decision}")

    with col2:
        st.subheader("3. Action Items")
        for item in data.action_items:
            st.markdown(
                f"- **{item.task}**  \n  👤 *Owner:* {item.owner} | 📅 *Deadline:* {item.deadline}"
            )

    st.divider()

    st.subheader("4. Execute Automations")
    exec_col1, exec_col2 = st.columns(2)

    with exec_col1:
        if st.button("📧 Send Email via Gmail"):
            emails = [e.strip() for e in recipient_emails.split(",") if e.strip()]
            if not emails:
                st.warning("Please enter recipient emails in the sidebar.")
            elif not SENDER_EMAIL or not SENDER_PASSWORD:
                st.error("Missing SENDER_EMAIL or SENDER_PASSWORD environment variables.")
            else:
                email_body = f"""
                <h2>Meeting Summary</h2>
                <p>{data.summary}</p>
                <h3>Key Decisions</h3>
                <ul>{"".join([f"<li>{d}</li>" for d in data.decisions])}</ul>
                <h3>Action Items</h3>
                <ul>{"".join([f"<li><b>{item.task}</b> (Owner: {item.owner}, Deadline: {item.deadline})</li>" for item in data.action_items])}</ul>
                """
                try:
                    send_email_via_smtp(emails, "Meeting Recap & Action Items", email_body)
                    st.success("Recap email sent successfully via Gmail!")
                except Exception as e:
                    st.error(f"Failed to send email: {e}")

    with exec_col2:
        start_dt = datetime.combine(followup_date, followup_time)
        end_dt = start_dt + timedelta(minutes=30)
        attendee_list = [e.strip() for e in recipient_emails.split(",") if e.strip()]

        gcal_url = generate_gcal_link(
            title="Follow-up: Action Items Check-in",
            start_dt=start_dt,
            end_dt=end_dt,
            details=f"Summary: {data.summary}",
            attendees=attendee_list,
        )

        st.markdown(
            f'<a href="{gcal_url}" target="_blank"><button style="background-color:#4CAF50;color:white;padding:10px 20px;border:none;border-radius:4px;cursor:pointer;">📅 Add Follow-up to Google Calendar</button></a>',
            unsafe_allow_html=True,
        )