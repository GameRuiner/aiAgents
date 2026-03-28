import streamlit as st
import asyncio
from dotenv import load_dotenv

# Import your custom agent and logging functions
from agentlib.agents.search_agent import init_agent
from agentlib.utils.logs import log_interaction_to_file

# Configuration
REPO_OWNER = "google"
REPO_NAME = "adk-python"

# Load environment variables
load_dotenv()

# --- Page Configuration ---
st.set_page_config(
    page_title="Pydantic AI Search Agent",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 Pydantic AI Search Agent")
st.caption(f"Querying repository: `{REPO_OWNER}/{REPO_NAME}`")

# --- Session State Initialization ---
# 1. Initialize the agent only once
if "agent" not in st.session_state:
    with st.spinner("Initializing agent..."):
        agent, _ = init_agent(REPO_OWNER, REPO_NAME)
        st.session_state.agent = agent

# 2. Initialize chat history for the UI
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Chat Interface ---
# Display previous chat messages from history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Handle new user input
if prompt := st.chat_input("Ask a question about the repository..."):
    
    # Add user message to state and display it
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate and display the assistant's response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                # Run the async agent synchronously within Streamlit
                response = asyncio.run(st.session_state.agent.run(user_prompt=prompt))
                
                # Extract the output
                agent_output = response.output
                
                # Display the response
                st.markdown(agent_output)
                
                # Log the interaction just like in the CLI version
                log_interaction_to_file(st.session_state.agent, response.new_messages())
                
                # Add assistant response to state
                st.session_state.messages.append({"role": "assistant", "content": agent_output})
                
            except Exception as e:
                st.error(f"An error occurred: {e}")