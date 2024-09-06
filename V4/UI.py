from pinecone import Pinecone

# initialize connection to pinecone (get API key at app.pinecone.io)
api_key = '1d17b85b-355b-47cb-b352-5f77df519849'

# configure client
pc = Pinecone(api_key=api_key)

from pinecone import ServerlessSpec

spec = ServerlessSpec(
    cloud="aws", region="us-west-2"
)

import time

index_name = 'books'

# connect to index
index = pc.Index(index_name)

from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

def cut_context(context):
    sum_tokens = 0
    context.reverse()
    for i, qna in enumerate(context):
        sum_tokens += len(str(qna).split())
        if sum_tokens > 2048:
            context.reverse()
            return context[i:]
    context.reverse()
    return context

def augment_prompt(query: str, history:list):
    # get top 3 results from knowledge base
    results = cut_context([match['metadata'] for match in index.query(4,model.encode(str(history) + '\n' + query).tolist(),include_metadata=True)['matches']])
    # get the text from the results
    source_knowledge = "\n".join([str(x) for x in results])
    # feed into an augmented prompt
    augmented_prompt = f"""Using the contexts and chat history below, answer the query.

    Contexts:
    {source_knowledge}

    Chat history:
    {str(history)}

    Query: {query}"""
    return augmented_prompt



import os
os.environ["OPENAI_API_KEY"] = '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' # ال OpenAI API key اللي هندفع بيه لOpenAI

from openai import OpenAI

client = OpenAI()

import gradio as gr


chat_history_ = []

def cut_history(history):
    sum_tokens = 0
    history.reverse()
    for i, qna in enumerate(history):
        sum_tokens += len(str(qna).split())
        if sum_tokens > 2048:
            history.reverse()
            return history[i:]
    history.reverse()
    return history


def chat_(chat_history, question):
  global chat_history_

  prompt = augment_prompt(question, str(cut_history(chat_history_[-9:])).replace('{','<').replace('}','>')) # دي concatenated message 

  print(prompt)
  bot_response = client.chat.completions.create(
  model="ft:gpt-3.5-turbo-0125:personal::90DRTKLr",
  messages=[
    {"role": "system", "content": "You are Dr.Bassel, you're a Mental Health Professional who helps people with mental disorders like autism and ADHD."},
    {"role": "user", "content": prompt}
  ]
).choices[0].message.content.strip().replace('.  ', '.').replace(' .', '.').replace('.  ', '. ').replace('..', '.').replace('-.', '-').replace('- ', '-')

      


  response = ""
  chat_history_.append({"Question": question, "Answer": bot_response})

  for letter in ''.join(bot_response):
      response += letter + ""
      yield chat_history + [(question, response)]





with gr.Blocks() as demo:
    gr.Markdown('# Version4')
    with gr.Tab("Dr:Bassel"):

          chatbot = gr.Chatbot()
          message = gr.Textbox(placeholder='Type your message',label='Message Box')
          message.submit(chat_, [chatbot, message], chatbot)

demo.queue().launch(debug = True, share=True, server_port=8000)