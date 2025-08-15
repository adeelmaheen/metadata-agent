import os
import streamlit as st
import asyncio
from agents import Agent, Runner, ModelSettings, trace
from agents.run import RunConfig
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        st.error("OpenAI API key is not set in the environment variables.")

st.title("Chat with Metadata/Trace")

user_id = st.text_input("Enter your user ID:", value=f"user_{os.getpid()}")

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hello! Ask me something :)"}]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ask something..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").markdown(prompt)

    metadata = {
        "user_id": user_id,
        "timestamp": datetime.utcnow().isoformat()
    }

    with trace(workflow_name="ChatSession", metadata=metadata):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            st.error("OpenAI API key is not set in the environment variables.")
            
        run_cfg = RunConfig(trace_metadata=metadata)
        model_settings = ModelSettings()
        agent = Agent(
            name="MetaGPT",
            instructions="Explain simply, like talking to a friend.",
            model="gpt-5",
            model_settings=model_settings
        )
        result = asyncio.run(Runner.run(agent, input=prompt, run_config=run_cfg))

    reply = result.final_output
    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.chat_message("assistant").markdown(reply)
