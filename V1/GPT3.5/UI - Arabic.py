import os
os.environ["OPENAI_API_KEY"] = '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' # ال OpenAI API key اللي هندفع بيه لOpenAI

from langchain.llms import OpenAI

llm = OpenAI(model_name="gpt-3.5-turbo-instruct") # اسم الموديل اللي هنسخدمه (كل موديل ليه سعره ودرجة ذكاءه)


import gradio as gr
from langchain import PromptTemplate


from langchain.chains import LLMChain


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
      
        template = 'انت خبير في الصحة العقلية يساعد من يمتلكون بعض الامراض العقلية او النفسية نثل التوحد والADHD.\nبناءاً لهذه المحادثة الدائرة بيننا:\n'+ str(cut_history(chat_history_)).replace('{','<').replace('}','>') +'\n اجب عن هذا السؤال: "{ques1}" بإجابة تفاعلية.' # دي concatenated message 
        prompt = PromptTemplate(
            input_variables=["ques1"],
            template=template,
        )
        chain = LLMChain(llm=llm, prompt=prompt)
        

  else:
        template = 'انت خبير في الصحة العقلية يساعد من يمتلكون بعض الامراض العقلية او النفسية نثل التوحد والADHD.' +'\n اجب عن هذا السؤال: "{ques1}" بإجابة تفاعلية.' # دي concatenated message 
        prompt = PromptTemplate(
            input_variables=["ques1"],
            template=template,
        )
        chain = LLMChain(llm=llm, prompt=prompt)
  print(prompt.template)
  bot_response = chain.run(question)
      


  response = ""
  chat_history_.append({"السؤال": question, "الإجابة": bot_response})

  for letter in ''.join(bot_response):
      response += letter + ""
      yield chat_history + [(question, response)]




with gr.Blocks() as demo:
    gr.Markdown('# الاصدار الاول')
    with gr.Tab("دكتر باسل"):

          chatbot = gr.Chatbot()
          message = gr.Textbox(placeholder='اكتب سؤالك هنا',label='صندوق الرسالة')
          message.submit(chat_, [chatbot, message], chatbot)

demo.queue().launch(debug = True, share=True, server_port=8000)