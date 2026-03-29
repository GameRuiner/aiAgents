import json
from pydantic import BaseModel

from ..core_agent.search_agent import Agent


EVALUATION_PROMPT = """
Use this checklist to evaluate the quality of an AI agent's answer (<ANSWER>) to a user question (<QUESTION>).
We also include the entire log (<LOG>) for analysis.

For each item, check if the condition is met. 

Checklist:

- instructions_follow: The agent followed the user's instructions (in <INSTRUCTIONS>)
- instructions_avoid: The agent avoided doing things it was told not to do  
- answer_relevant: The response directly addresses the user's question  
- answer_clear: The answer is clear and correct  
- answer_citations: The response includes proper citations or sources when required  
- completeness: The response is complete and covers all key aspects of the request
- tool_call_search: Is the search tool invoked? 

Output true/false for each check and provide a short explanation for your judgment.
""".strip()

class EvaluationCheck(BaseModel):
    check_name: str
    justification: str
    check_pass: bool


class EvaluationChecklist(BaseModel):
    checklist: list[EvaluationCheck]
    summary: str

def create_evaluation_agent():
    return Agent(
        name="eval_agent",
        model="openai:gpt-5-nano",
        instructions=EVALUATION_PROMPT,
        output_type=EvaluationChecklist,
    )

async def evaluate_log_record(eval_agent: Agent, log_record: dict):
    """
    Evaluates a single log record produced by agentlib.utils.logs.
    """
    messages = log_record["messages"]

    instructions = log_record["system_prompt"]
    question = messages[0]["parts"][0]["content"]
    answer = messages[-1]["parts"][0]["content"]

    log_json = json.dumps(messages)

    user_prompt = f"""
<INSTRUCTIONS>
{instructions}
</INSTRUCTIONS>

<QUESTION>
{question}
</QUESTION>

<ANSWER>
{answer}
</ANSWER>

<LOG>
{log_json}
</LOG>
""".strip()

    result = await eval_agent.run(user_prompt, output_type=EvaluationChecklist)
    return result.output