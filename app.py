import streamlit as st
import asyncio
import os

# Import your custom agent and logging functions
from agentlib.agents.search_agent import init_agent
from agentlib.utils.logs import log_interaction_to_file

# Configuration
REPO_OWNER = "google"
REPO_NAME = "adk-python"

# --- Page Configuration ---
st.set_page_config(
    page_title="Pydantic AI Search Agent",
    page_icon="🤖",
    layout="centered"
)

# --- API Key Handling ---
with st.sidebar:
    st.header("Configuration")
    api_key = st.text_input("OpenAI API Key", type="password", help="Paste your OpenAI API key here.")
    
    if api_key:
        # Set it as an environment variable so Pydantic AI automatically picks it up
        os.environ["OPENAI_API_KEY"] = api_key

st.title("🤖 Pydantic AI Search Agent")
st.caption(f"Querying repository: `{REPO_OWNER}/{REPO_NAME}`")

# Stop execution if the key isn't provided (and isn't in the environment)
if not os.environ.get("OPENAI_API_KEY"):
    st.info("👈 Please enter your OpenAI API Key in the sidebar to start.")
    st.stop()

# --- Session State Initialization ---
# 1. Initialize the agent only once
if "agent" not in st.session_state:
    with st.spinner("Initializing agent..."):
        agent, _ = init_agent(REPO_OWNER, REPO_NAME)
        st.session_state.agent = agent

# 2. UI chat history (for rendering the Streamlit interface)
if "messages" not in st.session_state:
    st.session_state.messages = []

# 3. Pydantic AI message history (to give the agent conversation context)
if "pydantic_messages" not in st.session_state:
    st.session_state.pydantic_messages = []


# --- Chat Interface ---
# Display previous chat messages from history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- Chat Interface ---
if prompt := st.chat_input("Ask a question about the repository..."):
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        
        async def run_agent_stream():
            # Initialize the string INSIDE the function to avoid scope issues
            full_text = ""
            try:
                async with st.session_state.agent.run_stream(
                    prompt, 
                    message_history=st.session_state.pydantic_messages
                ) as result:
                    async for chunk in result.stream_text(delta=True):
                        full_text += chunk
                        response_placeholder.markdown(full_text + "▌")
                    
                    response_placeholder.markdown(full_text)
                    
                    # Update the history in session state
                    st.session_state.pydantic_messages = result.all_messages()
                    return full_text # Return the final string
            except Exception as e:
                st.error(f"Error: {e}")
                return None

        # Execute and capture the returned string
        final_response = asyncio.run(run_agent_stream())
        
        if final_response:
            st.session_state.messages.append({"role": "assistant", "content": final_response})