import os
import streamlit as st
import requests
from dotenv import load_dotenv
import time
import threading

# Load environment variables
load_dotenv()

# Fetch Groq API Key from .env file
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Function to interact with Groq API
def ask_groq(chat_history):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "llama3-8b-8192",
        "messages": chat_history
    }

    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        return response.json().get("choices", [{}])[0].get("message", {}).get("content", "No response.")
    else:
        return f"⚠ Groq API Error: {response.json()}"

# Streamlit UI Setup
st.title("🤖 AI AGENT BY JITENDRA PAL")

# Sidebar: Chat History Management
st.sidebar.header("📜 Chat History")

# Live Time Display
current_time_placeholder = st.sidebar.empty()

def update_time():
    while True:
        current_time_placeholder.write(f"🕒 {time.strftime('%Y-%m-%d %H:%M:%S')}")
        time.sleep(1)

time_thread = threading.Thread(target=update_time, daemon=True)
time_thread.start()

if st.sidebar.button("🗑 Clear Chat History"):
    st.session_state.chat_history = []
    st.rerun()

# Initialize chat history if not present
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display only user messages in sidebar chat history
if st.session_state.chat_history:
    selected_message = st.sidebar.radio("", 
                                        [msg["content"] for msg in st.session_state.chat_history if msg["role"] == "user"],
                                        index=None, key="chat_history_radio")
else:
    selected_message = None

# Display chat messages in main window
for msg in st.session_state.chat_history:
    with st.chat_message("user" if msg["role"] == "user" else "assistant"):
        st.write(msg["content"])

# If a message is selected in the sidebar, scroll to its response
if selected_message:
    for i, msg in enumerate(st.session_state.chat_history):
        if msg["content"] == selected_message and msg["role"] == "user":
            st.markdown("---")
            if i + 1 < len(st.session_state.chat_history) and st.session_state.chat_history[i + 1]["role"] == "assistant":
                st.markdown(f"{st.session_state.chat_history[i + 1]['content']}", unsafe_allow_html=True)
            st.markdown("---")
            break

# User Input Section
query = st.chat_input("💬 Type your message:")

if query:
    # Add user message to chat history
    st.session_state.chat_history.append({"role": "user", "content": query})
    
    # Get AI response
    ai_response = ask_groq(st.session_state.chat_history)
    
    # Add AI response to chat history
    st.session_state.chat_history.append({"role": "assistant", "content": ai_response})
    
    # Refresh UI to display new messages
    st.rerun()
