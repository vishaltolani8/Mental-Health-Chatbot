from typing import Tuple
import json

from langchain_core.tools import tool
from langchain_groq import ChatGroq

from config import GROQ_API_KEY
from tools import query_medgemma, call_emergency


# -----------------------------
# Groq Setup
# -----------------------------

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.3,
    api_key=GROQ_API_KEY,
)


# -----------------------------
# Tools
# -----------------------------

@tool
def ask_mental_health_specialist(query: str) -> str:
    """
    Generate a therapeutic response using the MedGemma model.
    Use this only for serious mental health concerns.
    """
    print("DEBUG: MedGemma tool called")
    print("DEBUG query:", query)

    response = query_medgemma(query)

    print("DEBUG: MedGemma returned")

    if not response:
        return "I am here with you. Could you tell me a little more about what you are feeling?"

    return response


@tool
def emergency_call_tool(reason: str = "Mental health emergency detected.") -> str:
    """
    Place an emergency call through Twilio.
    Use this only for suicidal ideation, self-harm intent, or immediate crisis.
    """
    print("DEBUG: emergency_call_tool called")
    print("DEBUG reason:", reason)

    call_emergency()

    return "Emergency support has been contacted."


@tool
def find_nearby_therapists_by_location(location: str) -> str:
    """
    Finds therapists near the specified location.
    """
    print("DEBUG: therapist tool called")
    print("DEBUG location:", location)

    return (
        f"Here are some therapists near {location}:\n"
        "- Dr. Ayesha Kapoor - +1 (555) 123-4567\n"
        "- Dr. James Patel - +1 (555) 987-6543\n"
        "- MindCare Counseling Center - +1 (555) 222-3333"
    )


# -----------------------------
# Prompts
# -----------------------------

ROUTER_PROMPT = """
You are a router for a mental health AI chatbot.

Classify the user message into exactly one action:

1. normal_chat
2. serious_mental_health
3. emergency
4. therapist

Rules:

normal_chat:
- greetings
- casual conversation
- normal questions
- general advice
- productivity questions
- mild emotional check-ins like "I feel a bit low today" or "I am tired"

serious_mental_health:
- strong anxiety, depression, trauma, panic, grief, hopelessness
- emotional breakdown
- intense distress
- user asks for therapy-like help
- user describes ongoing mental health struggle
- but there is no clear immediate self-harm intent

emergency:
- suicidal thoughts
- self-harm intent
- intent to harm others
- immediate danger
- phrases like "I want to die", "I want to kill myself", "I will hurt myself"

therapist:
- user asks for therapist, counselor, psychologist, psychiatrist, clinic, or nearby professional help

Return only valid JSON in this format:

{
  "action": "normal_chat | serious_mental_health | emergency | therapist",
  "location": "city or area if available, otherwise empty string"
}
"""


NORMAL_CHAT_PROMPT = """
You are a warm, friendly AI assistant.

The user is not in a serious mental health crisis.
Reply naturally, clearly, and supportively.

Rules:
- Keep responses concise.
- Be kind and human.
- Do not over-medicalize normal sadness or stress.
- Do not diagnose.
- If the user casually feels low, gently support them and ask one caring follow-up question.
"""


# -----------------------------
# Local Safety Checks
# -----------------------------

def detect_emergency_locally(user_input: str) -> bool:
    text = user_input.lower()

    emergency_keywords = [
        "i want to die",
        "i want to kill myself",
        "i will kill myself",
        "i am going to kill myself",
        "i want to end my life",
        "i will end my life",
        "i am going to end my life",
        "i want to hurt myself",
        "i will hurt myself",
        "i am going to hurt myself",
        "suicide",
        "suicidal",
        "self harm",
        "self-harm",
    ]

    return any(keyword in text for keyword in emergency_keywords)


# -----------------------------
# Router
# -----------------------------

def route_user_input(user_input: str) -> dict:
    if detect_emergency_locally(user_input):
        return {
            "action": "emergency",
            "location": "",
        }

    try:
        response = llm.invoke(
            [
                {
                    "role": "system",
                    "content": ROUTER_PROMPT,
                },
                {
                    "role": "user",
                    "content": user_input,
                },
            ]
        )

        content = response.content.strip()
        print("DEBUG router raw:", content)

        return json.loads(content)

    except Exception as e:
        print("DEBUG router error:", str(e))

        return {
            "action": "normal_chat",
            "location": "",
        }


# -----------------------------
# Groq Normal Response
# -----------------------------

def ask_groq_normal_chat(user_input: str) -> str:
    response = llm.invoke(
        [
            {
                "role": "system",
                "content": NORMAL_CHAT_PROMPT,
            },
            {
                "role": "user",
                "content": user_input,
            },
        ]
    )

    return response.content


# -----------------------------
# Main Agent Flow
# -----------------------------

def run_agent(user_input: str) -> Tuple[str, str]:
    user_input = user_input.strip()

    if not user_input:
        return "None", "Please type something so I can support you."

    route = route_user_input(user_input)

    action = route.get("action", "normal_chat")
    location = route.get("location", "")

    print("DEBUG route:", route)

    if action == "emergency":
        try:
            emergency_call_tool.invoke(
                {
                    "reason": user_input
                }
            )

            return (
                "emergency_call_tool",
                "I’m really sorry you’re feeling this way. Emergency support has been contacted. "
                "Please stay near someone you trust and move away from anything you could use to harm yourself."
            )

        except Exception as e:
            print("DEBUG emergency error:", str(e))

            return (
                "emergency_call_tool",
                "I’m really sorry you’re feeling this way. I could not place the emergency call automatically. "
                "Please call your local emergency number or contact someone you trust immediately."
            )

    if action == "therapist":
        if not location:
            location = "your area"

        response = find_nearby_therapists_by_location.invoke(
            {
                "location": location
            }
        )

        return "find_nearby_therapists_by_location", response

    if action == "serious_mental_health":
        response = ask_mental_health_specialist.invoke(
            {
                "query": user_input
            }
        )

        return "ask_mental_health_specialist", response

    response = ask_groq_normal_chat(user_input)

    return "groq_normal_chat", response


# -----------------------------
# CLI Test
# -----------------------------
"""
if __name__ == "__main__":
    while True:
         = input("User: ").strip()

        if user_input.lower() in {"exit", "quit", "q"}:
            print("Goodbye.")
            break
user_input
        print(f"Received user input: {user_input[:200]}...")

        tool_called_name, final_response = run_agent(user_input)

        print("TOOL CALLED:", tool_called_name)
        print("ANSWER:", final_response)
    
"""