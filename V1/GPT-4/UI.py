import os
os.environ["OPENAI_API_KEY"] = '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' # ال OpenAI API key اللي هندفع بيه لOpenAI

from langchain.llms import OpenAI

llm = OpenAI(model_name='gpt-4') # اسم الموديل اللي هنسخدمه (كل موديل ليه سعره ودرجة ذكاءه)


import gradio as gr
from langchain import PromptTemplate

template = """
You are a Mental Health Professional who helps people with mental disorders like autism and ADHD. 
Answer this question: "{ques1}" with a conversational answer
""" # دي concatenated message 

prompt = PromptTemplate(
    input_variables=["ques1"],
    template=template,
)


from langchain.chains import LLMChain
chain = LLMChain(llm=llm, prompt=prompt) # الchain هتسهل الكود اكتر


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

  if chat_history_:
      
        template = 'You are a Mental Health Professional who helps people with mental disorders like autism and ADHD.\nBased on this chat history we\'ve been discussing:\n'+ str(cut_history(chat_history_)).replace('{','<').replace('}','>') +'\n Answer this question: "{ques1}" with a conversational answer.' # دي concatenated message 
        prompt = PromptTemplate(
            input_variables=["ques1"],
            template=template,
        )
        chain = LLMChain(llm=llm, prompt=prompt)
        

  else:
        template = 'You are a Mental Health Professional who helps people with mental disorders like autism and ADHD.' +'\n Answer this question: "{ques1}" with a conversational answer.' # دي concatenated message 
        prompt = PromptTemplate(
            input_variables=["ques1"],
            template=template,
        )
        chain = LLMChain(llm=llm, prompt=prompt)
  print(prompt.template)
  bot_response = chain.run(question)
      


  response = ""
  chat_history_.append({"Question": question, "Answer": bot_response})

  for letter in ''.join(bot_response):
      response += letter + ""
      yield chat_history + [(question, response)]




with gr.Blocks() as demo:
    gr.Markdown('# Version1')
    with gr.Tab("Dr:Dre"):

          chatbot = gr.Chatbot()
          message = gr.Textbox(placeholder='Type your message',label='Message Box')
          message.submit(chat_, [chatbot, message], chatbot)

demo.queue().launch(debug = True, share=True, server_port=8000)