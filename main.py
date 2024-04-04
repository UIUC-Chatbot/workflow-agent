import inspect
import json
import asyncio
import logging
import traceback
import uuid

from dotenv import load_dotenv
import ray
from agent.langgraph_agent_v2 import WorkflowAgent
from type.issue import Issue
from langchain import hub

from utils.utils import post_sharable_url

# load API keys from globally-availabe .env file
load_dotenv(dotenv_path='.env', override=True)

async def main():
  """

  DOCS: 
  API reference for Webhook objects: https://docs.github.com/en/webhooks-and-events/webhooks/webhook-events-and-payloads#issue_comment
  WEBHOOK explainer: https://docs.github.com/en/apps/creating-github-apps/registering-a-github-app/using-webhooks-with-github-apps
  """
  with open('issue.json') as f:
    issue_data = json.load(f)

  if issue_data:
    issue: Issue = Issue.from_json(issue_data)
    
  langsmith_run_id = str(uuid.uuid4())
  
  if not issue:
    raise ValueError(f"Missing the body of the webhook response. Response is {issue}")

  try:
    result_futures = []

    # 1. INTRO COMMENT
    # issue.create_comment(messageForNewIssues)
    # result_futures.append(post_comment.remote(issue_or_pr=issue, text=MESSAGE_HANDLE_ISSUE_OPENED, time_delay_s=0))

    # 2. SHARABLE URL (in background)
    result_futures.append(post_sharable_url.remote(issue=issue, langsmith_run_id=langsmith_run_id, time_delay_s=20))

    # 3. RUN BOT
    # bot = github_agent.GH_Agent.remote()
    prompt = hub.pull("kastanday/new-github-issue").format(issue_description=issue.format_issue())

    print("ABOUT TO CALL WORKFLOW AGENT on COMMENT OPENED")
    bot = await WorkflowAgent.create(langsmith_run_id=langsmith_run_id)
    result = await bot.run(prompt)

    # COLLECT PARALLEL RESULTS
    for _i in range(0, len(result_futures)):
      ready, not_ready = ray.wait(result_futures)
      result = ray.get(ready[0])
      result_futures = not_ready
      if not result_futures:
        break

    # FIN: Conclusion & results comment
    # ray.get(post_comment.remote(issue_or_pr=issue, text=str(result['output']), time_delay_s=0))
    logging.info(f"✅✅ Successfully completed the issue: {issue}")
    logging.info(f"Output: {str(result['output'])}")
  except Exception as e:
    logging.error(f"❌❌ Error in {inspect.currentframe().f_code.co_name}: {e}\nTraceback:\n", traceback.print_exc())
    err_str = f"Error in {inspect.currentframe().f_code.co_name}: {e}" + "\nTraceback\n```\n" + str(
        traceback.format_exc()) + "\n```"
    
    print(err_str)

  return '', 200

if __name__ == '__main__':
  asyncio.run(main())
