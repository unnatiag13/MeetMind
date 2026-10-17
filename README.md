# MeetMind 📝

**MeetMind** is an open-source, lightweight meeting intelligence agent. It ingests meeting transcripts, uses AI to extract key decisions and structured action items (with assigned owners and deadlines), and automates follow-ups by sending email recaps and generating Google Calendar event links.

## ✨ Features

* **Automated Processing:** Extracts structured insights from raw text transcripts using high-speed LLM inference.

* **Executive Summaries:** Generates concise 2–3 sentence overviews of key discussions.

* **Decision Tracking:** Captures immutable decisions made during meetings.

* **Action Item Extraction:** Parses specific tasks, assigns owners, and identifies deadlines.

* **Automated Email Recaps:** Formats meeting outputs into clean HTML emails sent via Gmail SMTP.

* **Google Calendar Integration:** Generates 1-click follow-up calendar event links pre-filled with attendees and meeting details.

* **Zero API Cost Architecture:** Built using free infrastructure (Groq Cloud LLM engine + Python `smtplib`).

## 🛠️ Tech Stack

* **Frontend / UI:** [Streamlit](https://streamlit.io/)

* **LLM Engine:** [Groq Cloud](https://console.groq.com/) (`llama-3.3-70b-versatile`)

* **SDK & Schemas:** OpenAI Python SDK, [Pydantic](https://docs.pydantic.dev/) (Structured Outputs)

* **Email Service:** Python `smtplib` (Gmail SMTP)

* **Environment Management:** `python-dotenv`

## 📁 Project Structure

```
MeetMind/
├── app.py              # Main application logic and Streamlit UI
├── requirements.txt    # Project dependencies
├── .env                # Environment variables (API keys & credentials)
└── README.md           # Project documentation

```

## 🚀 Quick Start Guide

### 1. Prerequisites

* Python 3.9 or higher installed.

* A **Groq API Key** (Free from [console.groq.com](https://console.groq.com)).

* A **Gmail App Password** (Generated via Google Account > Security > App Passwords).

### 2. Clone / Setup Workspace

Navigate to your project directory in terminal:

```
cd path/to/MeetMind

```

### 3. Virtual Environment Setup

Create and activate a virtual environment:

* **macOS / Linux:**

  ```
  python3 -m venv venv
  source venv/bin/activate
  
  ```

* **Windows (Command Prompt):**

  ```
  python -m venv venv
  venv\Scripts\activate
  
  ```

* **Windows (PowerShell):**

  ```
  python -m venv venv
  .\venv\Scripts\Activate.ps1
  
  ```

### 4. Install Dependencies

```
pip install -r requirements.txt

```

### 5. Configure Environment Variables

Create a `.env` file in the root folder of the project:

```
GROQ_API_KEY=gsk_your_groq_api_key_here
SENDER_EMAIL=your_email@gmail.com
SENDER_PASSWORD=your_16_character_app_password

```

> **Note:** Ensure there are no spaces around the `=` sign and `.env` is added to your `.gitignore` file to protect your credentials.

## 🏃 Running the Application

Launch the Streamlit web application:

```
streamlit run app.py

```

The app will automatically open in your default browser at `http://localhost:8501`.

## 📖 How to Use

1. **Setup Sidebar Metadata:**

   * Enter participant email addresses (comma-separated).

   * Select the follow-up meeting date and time.

2. **Input Transcript:**

   * Paste the raw meeting transcript into the central text area.

3. **Process Meeting:**

   * Click **Process Meeting** to generate the executive summary, decisions, and action items.

4. **Execute Automations:**

   * Click **📧 Send Email via Gmail** to send an HTML recap to all participants.

   * Click **📅 Add Follow-up to Google Calendar** to open a pre-filled calendar invite tab.

## 📝 License

This project is open source and available under the [MIT License](LICENSE).