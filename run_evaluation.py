import asyncio
import pandas as pd
from tqdm.asyncio import tqdm_asyncio as tqdm
from dotenv import load_dotenv

from agentlib.utils.logs import log_interaction_to_file, load_log_file, LOG_DIR
from agentlib.evaluation.evaluator_agent import create_evaluation_agent, evaluate_log_record
from agentlib.evaluation.question_generator import create_question_generator, generate_questions
from agentlib.core_agent.search_agent import init_agent

load_dotenv()
REPO_OWNER = "google"
REPO_NAME = "adk-python"

async def main(sample_size: int = 10):
    agent, knowledge = init_agent(REPO_OWNER, REPO_NAME)
    docs = knowledge.get_docs()
    question_gen = create_question_generator()
    questions = await generate_questions(question_gen, docs, sample_size=sample_size)

    print(f"Generated {len(questions)} questions:\n")
    for q in questions:
        print("-", q)

    for q in tqdm(questions):
        result = await agent.run(user_prompt=q)
        print(result.output)

        log_interaction_to_file(
            agent,
            result.new_messages(),
            source='ai-generated'
        )

    eval_set = []

    for log_file in LOG_DIR.glob("*.json"):
        if 'gh_agent' not in log_file.name:
            continue

        log_record = load_log_file(log_file)
        if log_record.get('source') != 'ai-generated':
            continue

        eval_set.append(log_record)

    eval_agent = create_evaluation_agent()
    eval_results = []

    for log_record in tqdm(eval_set):
        eval_result = await evaluate_log_record(eval_agent, log_record)
        eval_results.append((log_record, eval_result))

    rows = []

    for log_record, eval_result in eval_results:
        messages = log_record['messages']

        row = {
            'file': log_record['log_file'].name,
            'question': messages[0]['parts'][0]['content'],
            'answer': messages[-1]['parts'][0]['content'],
        }

        checks = {c.check_name: bool(c.check_pass) for c in eval_result.checklist}
        row.update(checks)

        rows.append(row)

    df_evals = pd.DataFrame(rows)
    bool_cols = df_evals.columns.difference(['file', 'question', 'answer', 'example'])
    df_evals[bool_cols] = df_evals[bool_cols].astype('boolean')

    print("\nEvaluation Summary (mean scores per check):")
    print(df_evals.mean(numeric_only=True))

    return df_evals


if __name__ == "__main__":
    asyncio.run(main(sample_size=10))