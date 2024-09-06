from openai import OpenAI
import os
os.environ["OPENAI_API_KEY"] = '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' # ال OpenAI API key اللي هندفع بيه لOpenAI

client = OpenAI()

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

def response_func(query: str, history:list):
    # feed into an augmented prompt
    augmented_prompt = client.chat.completions.create(
  model="ft:gpt-3.5-turbo-0125:personal::90DRTKLr",
  messages=[
    {"role": "system", "content": "You are Dr.Bassel, you're a Mental Health Professional who helps people with mental disorders like autism and ADHD."},
    {"role": "user", "content": f"Using this chat history {str(history)}, response to this message: {query}"}
    ]
    ).choices[0].message.content.strip().replace('.  ', '.').replace(' .', '.').replace('.  ', '. ').replace('..', '.').replace('-.', '-').replace('- ', '-')
    return augmented_prompt






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

  bot_response = response_func(question, str(cut_history(chat_history_[-9:])).replace('{','<').replace('}','>'))
      


  response = ""
  chat_history_.append({"Question": question, "Answer": bot_response})

  for letter in ''.join(bot_response):
      response += letter + ""
      yield chat_history + [(question, response)]





with gr.Blocks() as demo:
    gr.Markdown('# Version3')
    with gr.Tab("Dr:Bassel"):

          chatbot = gr.Chatbot()
          message = gr.Textbox(placeholder='Type your message',label='Message Box')
          message.submit(chat_, [chatbot, message], chatbot)

demo.queue().launch(debug = True, share=True, server_port=8000)