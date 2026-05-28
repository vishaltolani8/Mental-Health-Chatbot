# Step 1: Setup Streamlit
import streamlit as st
import requests

Backend_URL = "http://localhost:8000/ask"

st.set_page_config(page_title="AI Mental Health Therapist", layout="wide")
st.title("SafeSpace - AI Mental Health Therapist")

# Initialize chat session
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# Step 2: User chat input
user_input = st.chat_input("What is on your mind today?")

if user_input:
    # Append user message
    st.session_state.chat_history.append({
        "role": "user",
        "content": user_input
    })

    try:
        # Send message to backend
        response = requests.post(
            Backend_URL,
            json={"message": user_input}
        )

        if response.status_code == 200:
            data = response.json()

            assistant_response = data.get("response", "No response received.")
            tool_called = data.get("tool_called", "None")

            # Append assistant message with tool info
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": assistant_response,
                "tool_called": tool_called
            })

        else:
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": "Backend error. Please try again.",
                "tool_called": "Error"
            })

    except Exception as e:
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": f"Could not connect to backend: {str(e)}",
            "tool_called": "Connection Error"
        })


# Step 3: Show chat history
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

        if msg["role"] == "assistant":
            tool_called = msg.get("tool_called", "None")
            st.caption(f"Tool called: {tool_called}")