import os
import streamlit as st
import requests
from dotenv import load_dotenv

# ✅ Load environment variables
load_dotenv()

# ✅ Groq API Key
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# ✅ Function to interact with Groq API
def ask_groq(chat_history):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
    data = {"model": "llama3-8b-8192", "messages": chat_history}

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json().get("choices", [{}])[0].get("message", {}).get("content", "No response.")
    else:
        return f"⚠ Groq API Error: {response.json()}"

# ✅ Streamlit UI
st.title("🤖 AI AGENT BY JITENDRA PAL")

# ✅ Initialize Chat History
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ✅ Display Chat Messages using Streamlit's Chat Feature
for msg in st.session_state.chat_history:
    with st.chat_message("user" if msg["role"] == "user" else "assistant"):
        st.write(msg["content"])

# ✅ User Input
query = st.chat_input("💬 Type your message:")

if query:
    # ✅ Add user message to history
    st.session_state.chat_history.append({"role": "user", "content": query})

    # ✅ Get AI response
    ai_response = ask_groq(st.session_state.chat_history)

    # ✅ Add AI response to history
    st.session_state.chat_history.append({"role": "assistant", "content": ai_response})

    # ✅ Refresh UI
    st.rerun()