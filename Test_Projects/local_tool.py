from toolhouse import Toolhouse
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.environ.get('GROQCLOUD_API_KEY'),
    base_url="https://api.groq.com/openai/v1")

th = Toolhouse()

@th.register_local_tool("get_latest_emails")
def gmail_api():
  # Code goes here
  pass


my_local_tools = [
    {
        "type": "function",
        "function": {
            "name": "get_latest_emails",
            "description": "Retrieves the latest messages from the user's inbox.",
            "parameters": {}
        }
    }
  ]

messages = [
  {
    "role": "user",
    "content": "what's in my inbox?",
  }
]

response = client.chat.completions.create(
  model="llama3-groq-70b-8192-tool-use-preview",
  messages=messages,
  tools=th.get_tools() + my_local_tools,
)

# Runs your local tool, gets the result, 
# and appends it to the context
tool_run = th.run_tools(response)
messages += tool_run

response = client.chat.completions.create(
  model="llama3-groq-70b-8192-tool-use-preview",
  messages=messages,
  tools=th.get_tools() + my_local_tools,
)

print(response.choices[0].message.content)