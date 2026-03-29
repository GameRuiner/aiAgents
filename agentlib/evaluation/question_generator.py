import json
import random
from pydantic import BaseModel
from ..core_agent.search_agent import Agent

QUESTION_GEN_PROMPT = """
You are the question_generator agent.
Your task is to create a list of user questions that will be used to evaluate another agent called “adk_agent”.

---------------------
🎯 YOUR TASK
---------------------
Generate a list of **diverse, realistic, challenging user questions** that a developer might ask about the Google ADK Python repository based on the provided content.

Requirements:
• Include easy, medium, and advanced level questions.
• Generate one question per provided input document.
• Questions should be grounded in the content.

Output format:
A JSON object with a single field:
{{
  "questions": [ "question 1", "question 2", ... ]
}}

Keep questions short, concrete, and specific.
Use the documents below as the source material:
<DOCS>
{docs}
</DOCS>
""".strip()


class QuestionsList(BaseModel):
    questions: list[str]


def create_question_generator():
    """
    Returns a ready-made question generator agent.
    """
    return Agent(
        name="question_generator",
        instructions=QUESTION_GEN_PROMPT,
        model="openai:gpt-4o-mini",
        output_type=QuestionsList,
    )


async def generate_questions(question_generator: Agent, docs: list[dict], sample_size: int = 10):
    """
    docs: list of dicts containing at least 'content'
    sample_size: how many random docs to sample for questions

    Returns: list[str]
    """
    if len(docs) == 0:
        raise ValueError("No documents provided for question generation.")

    sample = random.sample(docs, min(sample_size, len(docs)))
    doc_contents = [d["content"] for d in sample]

    formatted_prompt = QUESTION_GEN_PROMPT.format(docs=json.dumps(doc_contents))

    result = await question_generator.run(formatted_prompt)
    return result.output.questions