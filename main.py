from agentlib.core_agent.search_agent import init_agent
from agentlib.utils.logs import log_interaction_to_file
import asyncio
from dotenv import load_dotenv

REPO_OWNER = "google"
REPO_NAME = "adk-python"

def main():
    agent, _ = init_agent(REPO_OWNER, REPO_NAME)
    
    print("\nReady to answer your questions!")
    print("Type 'stop' to exit the program.\n")
    
    while True:
        question = input("Your question: ")
        if question.strip().lower() == 'stop':
            print("Goodbye!")
            break

        print("Processing your question...")
        response = asyncio.run(agent.run(user_prompt=question))
        log_interaction_to_file(agent, response.new_messages())

        print("\nResponse:\n", response.output)
        print("\n" + "="*50 + "\n")

if __name__ == "__main__":
    load_dotenv()
    main()