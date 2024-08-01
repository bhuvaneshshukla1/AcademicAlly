# from openai import OpenAI

# client = OpenAI(
#   organization='org-yLg5N32y0jeQmx6DDb5hlCNh',
#   project='proj_5mNOnnfIQ5OhHay0weA9PDJy',
# )


# import openai
# import os

# # Ensure your API key and organization key are set as environment variables
# # api_key = os.getenv('OPENAI_API_KEY')
# # org_id = os.getenv('OPENAI_ORG_ID')

# api_key = "proj_5mNOnnfIQ5OhHay0weA9PDJy"
# org_id = "org-yLg5N32y0jeQmx6DDb5hlCNh"

# # Configuring the OpenAI library with your API key and organization
# openai.api_key = api_key
# openai.organization = org_id

# from openai import OpenAI

# client = OpenAI(api_key="sk-proj-GncTbc65kBcSuK36GCSET3BlbkFJN9eYJOSFyOI9uWZrUwT7")

# completion = client.completions.create(model='gpt-3.5-turbo-0125', prompt = "This is a test message")
# print(completion.choices[0].text)
# print(dict(completion).get('usage'))
# print(completion.model_dump_json(indent=2))


import pathlib
import textwrap

import google.generativeai as genai

# from IPython.display import display
# from IPython.display import Markdown
import yaml

with open('keys.yml', 'r') as file:
    api_creds = yaml.safe_load(file)
    print(api_creds)

GOOGLE_API_KEY = api_creds['gemini_key']
genai.configure(api_key=GOOGLE_API_KEY)

def to_markdown(text):
  text = text.replace('•', '  *')
  print(text)
  # return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))
  return text

def get_gpt_feedback(text):
  for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
      print(m.name)

  model = genai.GenerativeModel('gemini-1.0-pro')
  response = model.generate_content(text)
  return to_markdown(response.text)


def get_aggregated_feedback(feedbackList):

  model = genai.GenerativeModel('gemini-1.0-pro')
  combined_feedback_string = ':'.join(feedbackList)
  print("Combined Feedback is-", combined_feedback_string)

  # query = """Please act as a sentiment analyser. I have attached some : seperated feedbacks for an assginment. 
  # Can you seperatly aggregate the positive feedback, the negative feedback 
  # and your opinion on how the assignment can be improved?"""
  query = """
  Forget all previous instructions. Act as a sentiment analyzer. 
  I will provide you with feedback for an assignment, separated by colons. 
  You will categorize the feedback into positive and negative, and then suggest improvements based on the feedback. 
  Present the categorized feedback in a coherent paragraph format. List improvement suggestions separately, succinctly, and clearly, without any additional explanations.
  """
  query += combined_feedback_string

  response = model.generate_content(query)
  aggregated_feedback = response.text.replace('•', '  *')

  return aggregated_feedback