# SafeSpace - AI Mental Health Chatbot

SafeSpace is an AI-powered mental health chatbot built with **FastAPI** and **Streamlit**. It uses **Groq** for fast normal conversations and routes emotional or serious mental health concerns to a **MedGemma-based specialist response system**. The chatbot also includes emergency detection and therapist assistance tools.

## Features

- Fast normal chat using Groq
- Mental health support using MedGemma
- Emergency/self-harm detection
- Therapist location assistance
- FastAPI backend
- Streamlit chatbot frontend
- Tool-call tracking to show which AI flow was used

## Tech Stack

- Python
- FastAPI
- Streamlit
- LangChain
- Groq API
- MedGemma
- Twilio, for emergency call support

## Project Structure

```text
safespace/
│
├── backend/
│   ├── main.py
│   ├── ai_agent.py
│   ├── tools.py
│   └── config.py
│
├── frontend/
│   └── app.py
│
└── README.md
````

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/safespace.git
cd safespace
```

### 2. Create Virtual Environment

```bash
uv venv
```

Activate it:

```bash
.venv\Scripts\activate
```

### 3. Install Dependencies

```bash
uv add fastapi uvicorn streamlit requests langchain langchain-groq
```

### 4. Create `config.py`

Inside the `backend` folder, create a file named:

```text
config.py
```

Add your API keys:

```python
GROQ_API_KEY = "your_groq_api_key_here"

TWILIO_ACCOUNT_SID = "your_twilio_account_sid_here"
TWILIO_AUTH_TOKEN = "your_twilio_auth_token_here"
TWILIO_PHONE_NUMBER = "your_twilio_phone_number_here"
EMERGENCY_PHONE_NUMBER = "your_emergency_phone_number_here"
```

Add any MedGemma API/model configuration here if your `tools.py` requires it.

## How to Run

### 1. Start Backend

From the project root, run:

```bash
uv run uvicorn backend.main:app --reload
```

Backend will run at:

```text
http://localhost:8000
```

You can test the API docs here:

```text
http://localhost:8000/docs
```

### 2. Start Frontend

Open a new terminal and run:

```bash
uv run streamlit run frontend/app.py
```

Frontend will open in your browser.

## API Endpoint

### POST `/ask`

Request:

```json
{
  "message": "I am feeling anxious today"
}
```

Response:

```json
{
  "response": "AI response here...",
  "tool_called": "ask_mental_health_specialist"
}
```

## AI Routing Flow

```text
Normal chat/questions        → Groq
Mental health concerns       → MedGemma
Emergency/self-harm messages → Emergency call tool
Therapist request            → Therapist location tool
```

## Example Tool Calls

```text
User: hi
Tool Called: groq_normal_chat

User: I am feeling low today
Tool Called: ask_mental_health_specialist

User: I need a therapist in Karachi
Tool Called: find_nearby_therapists_by_location

User: I want to hurt myself
Tool Called: emergency_call_tool
```

## Note

SafeSpace is an educational AI project and is not a replacement for professional mental health care. In emergency situations, users should contact local emergency services or trusted people immediately.

```
```
