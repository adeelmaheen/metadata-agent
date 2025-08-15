# Chat Agent with Metadata Tracing (OpenAI Agents SDK)

**A simple and powerful Streamlit-based chat app** where you can attach session info through `metadata`. This app uses OpenAI Agents SDK's tracing feature to help with **logging, debugging, and analytics**.

---

## Features

- Streamlit chat interface with basic **chat history**
- Use of SDK's `metadata` to tag each call with info like `user_id` and `timestamp`
- Tracing of agent runs using `trace()` and `RunConfig(trace_metadata=...)`
- View trace metadata in **OpenAI Traces Dashboard**
- Easy to customize and inspect performance per session

---

## Why Metadata & Tracing Matter

- `metadata` lets you attach **custom key/value tags** (e.g. session ID) to trace logs and analytics
- `trace()` builds spans for each agent, tool call, generation, etc.—traceable via OpenAI's dashboard

---

## Getting Started

### 1. Clone & Install

```bash
git clone <this-repo-url>
cd metadata-chat-agent
python -m venv .venv

# On Linux/Mac:
source .venv/bin/activate

# On Windows:
.venv\Scripts\activate

pip install streamlit openai-agents
```

### 2. Set OpenAI API Key

```bash
export OPENAI_API_KEY="YOUR_API_KEY_HERE"
```

Or use `set_default_openai_key()` in code.

### 3. Run the App

```bash
streamlit run app.py
```

Open browser at http://localhost:8501.

---

## App Overview

```python
from agents import Agent, Runner, ModelSettings, trace
from agents.run import RunConfig
import streamlit as st
from datetime import datetime
import os, asyncio

# UI Setup: User enters user_id and types questions
# Chat History: Maintained in st.session_state.messages

# Metadata
metadata = {
    "user_id": user_id,
    "timestamp": datetime.utcnow().isoformat()
}

# Tracing & RunConfig
with trace(workflow_name="ChatSession", metadata=metadata):
    run_cfg = RunConfig(trace_metadata=metadata)
    agent = Agent(..., model_settings=ModelSettings())
    result = asyncio.run(Runner.run(agent, input=prompt, run_config=run_cfg))

# Result Displayed: Agent's final_output shown, and chat history updates
```

---

## Customization Ideas

- Add more metadata like `"chat_topic": "homework"`, `"model_used": "gpt-5"`
- Filter/search sessions in Traces Dashboard by metadata tags
- Export traces to Langfuse for better analytics
- Disable tracing with: `set_tracing_disabled(True)`
