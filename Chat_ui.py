import streamlit as st
import httpx
import asyncio
import itertools
import nest_asyncio

# Patch event loop for Streamlit compatibility
nest_asyncio.apply()

# Set the title of the Streamlit app
st.title("🧠 Wavemark Connect")
#API_URL = "http://127.0.0.1:8000/chat"  # Replace with your actual API URL
API_URL = "https://vqwjjdsh-8000.use.devtunnels.ms/chat"  # Replace with your actual API URL

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Async function to fetch bot reply
async def fetch_bot_reply(prompt):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(API_URL, json={"message": prompt},headers={"Content-Type": "application/json"}, timeout=100)
            response.raise_for_status()
            return response.json().get("response", "No response from server")
    
    except httpx.RequestError as e:
        return f"Error contacting backend: {str(e)}"
    except httpx.HTTPStatusError as e:
        return f"HTTP error: {e.response.status_code} - {e.response.text}"
    except Exception as e:
        return f"Unexpected error: {type(e).__name__} - {str(e)}"


# Typing animation coroutine
async def typing_animation(placeholder):
    dots = itertools.cycle([".", "..", "..."])
    try:
        while True:
            placeholder.markdown(f"{next(dots)}")
            await asyncio.sleep(0.2)
    except asyncio.CancelledError:
        placeholder.empty()

# Main async handler
async def handle_chat(prompt):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        typing_placeholder = st.empty()
        response_placeholder = st.empty()

        # Start typing animation in background
        animation_task = asyncio.create_task(typing_animation(typing_placeholder))

        # Fetch bot reply
        bot_reply = await fetch_bot_reply(prompt)

        # Stop animation
        animation_task.cancel()
        try:
            await animation_task
        except asyncio.CancelledError:
            pass

        # Stream the bot reply character by character
        streamed_text = ""
        chunk_size = 5
        delay = 0.01

        for i in range(0, len(bot_reply), chunk_size):
            streamed_text += bot_reply[i:i+chunk_size]
            response_placeholder.markdown(streamed_text)
            await asyncio.sleep(delay)

        st.session_state.messages.append({"role": "assistant", "content": bot_reply})

# Entry point for user input
if prompt := st.chat_input("Type your message:"):
    asyncio.run(handle_chat(prompt))