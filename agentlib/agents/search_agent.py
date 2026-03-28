from typing import List, Any
from pydantic_ai import Agent
from .search_tools import SearchTool
from ..knowledge_base.knowledge_base import KnowledgeBase

SYSTEM_PROMPT_TEMPLATE = """
You are a helpful assistant that answers questions about documentation.  

Use the search tool to find relevant information from the course materials before answering questions.  

If you can find specific information through search, use it to provide accurate answers.

Always include references by citing the filename of the source material you used.
Replace it with the full path to the GitHub repository:
"https://github.com/{repo_owner}/{repo_name}/blob/main/"
Format: [LINK TITLE](FULL_GITHUB_LINK)


If the search doesn't return relevant results, let the user know and provide general guidance.
"""


def init_agent(repo_owner, repo_name):
    system_prompt = SYSTEM_PROMPT_TEMPLATE.format(repo_owner=repo_owner, repo_name=repo_name)
    
    kb = KnowledgeBase(repo_owner, repo_name)
    kb.build()
    
    search_tool = SearchTool(kb=kb)

    agent = Agent(
        name="gh_agent",
        instructions=system_prompt,
        tools=[search_tool.search],
        model="openai:gpt-4o-mini"
    )

    return agent, kb