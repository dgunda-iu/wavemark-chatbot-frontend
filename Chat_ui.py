
import streamlit as st
import httpx
import asyncio
import itertools
import nest_asyncio

# Patch event loop for Streamlit compatibility
nest_asyncio.apply()

st.title("🧠 Wavemark Connect (Test API Mode)")

API_URL = "https://api.restful-api.dev/objects"

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Async function to simulate bot reply using test API
async def fetch_bot_reply(prompt):
    try:
        payload = {
            "name": "Test Object",
            "data": {
                "message": prompt
            }
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(API_URL, json=payload, timeout=30)
            response.raise_for_status()
            json_data = response.json()
            return f"✅ Object created with ID: `{json_data.get('id')}`\n\n**Name:** {json_data.get('name')}\n**Data:** {json_data.get('data')}"
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

        animation_task = asyncio.create_task(typing_animation(typing_placeholder))
        bot_reply = await fetch_bot_reply(prompt)
        animation_task.cancel()
        try:
            await animation_task
        except asyncio.CancelledError:
            pass

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
