import streamlit as st
import requests

# Set the title of the Streamlit app
st.title("🧠 Wavemark Connect")

# Test API URL
API_URL = "https://jsonplaceholder.typicode.com/comments"

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Function to fetch bot reply using a simple GET request
def fetch_bot_reply(prompt):
    try:
        response = requests.get(
            API_URL,
            headers={"User-Agent": "MyAppServiceClient/1.0"},
            timeout=10
        )
        response.raise_for_status()
        return str(response.json())
    except requests.RequestException as e:
        return f"Error: {str(e)}"

# Handle user input
if prompt := st.chat_input("Type your message:"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    bot_reply = fetch_bot_reply(prompt)

    with st.chat_message("assistant"):
        st.markdown(bot_reply[:500])  # Limit the response length for display

    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
