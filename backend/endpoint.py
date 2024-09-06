import os
from flask import Flask,request,jsonify
from flask_cors import CORS,cross_origin
from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from pinecone import Pinecone, ServerlessSpec
from sentence_transformers import SentenceTransformer

# llm = ChatOpenAI(name="gpt-4", api_key='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') # اسم الموديل اللي هنسخدمه (كل موديل ليه سعره ودرجة ذكاءه)
llm4 = ChatOpenAI(name='gpt-4', api_key='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')
llm3 = ChatOpenAI(name='gpt-3.5-turbo', api_key='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')
def chooseLlm(llm):
    if llm == 'gpt-3.5-turbo':
         return llm3
    else:
         return llm4

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


app = Flask(__name__)
app.config['CORS_HEADERS'] = ['Content-Type']
cors = CORS(app,origins=['*'])

@app.route('/v1e', methods=['POST'])
@cross_origin(origin=['*'],headers=['Content-Type'])
def v1e():

    global chat_history_

    try:
        # Get the data from the POST request
        request_data = request.get_json() # [question]
        # Assuming the data is a list of inputs
        question = request_data.get('question') # how to deal with ADHD?"
        chat_history_ = request_data.get('chat_history')
        llm = chooseLlm(request_data.get('GPT'))

        

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
        llm_response = chain.run(question)

        # chat_history_.append({"Question": question, "Answer": llm_response})
        
        # Prepare the response
        response = {
            'status': 'success',
            'response': llm_response
        }
        return jsonify(response)
    except Exception as e:
        # If an exception occurs, handle it and return an error response
        error = {
            'status': 'error',
            'message': str(e)
        }
        return jsonify(error), 500


@app.route('/v1a', methods=['POST'])
@cross_origin(origin=['*'],headers=['Content-Type'])
def v1a():

    global chat_history_

    try:
        # Get the data from the POST request
        request_data = request.get_json() # [question]
        # Assuming the data is a list of inputs
        question = request_data.get('question') # how to deal with ADHD?"
        chat_history_ = request_data.get('chat_history')
        llm = chooseLlm(request_data.get('GPT'))

        if chat_history_:
      
            template = 'أنت متخصص في الصحة العقلية وتساعد الأشخاص الذين يعانون من اضطرابات عقلية مثل التوحد واضطراب فرط الحركة ونقص الانتباه.\nبناءً على سجل الدردشة هذا الذي كنا نناقشه:\n'+ str(cut_history(chat_history_)).replace('{','<').replace('}','>') +'\n أجب على هذا السؤال: "{ques1}" بإجابة تحاورية.' # دي concatenated message 
            prompt = PromptTemplate(
                input_variables=["ques1"],
                template=template,
            )
            chain = LLMChain(llm=llm, prompt=prompt)
            

        else:
            template = 'أنت متخصص في الصحة العقلية وتساعد الأشخاص الذين يعانون من اضطرابات عقلية مثل التوحد واضطراب فرط الحركة ونقص الانتباه.' +'\n أجب على هذا السؤال: "{ques1}" بإجابة تحاورية.' # دي concatenated message 
            prompt = PromptTemplate(
                input_variables=["ques1"],
                template=template,
            )
            chain = LLMChain(llm=llm, prompt=prompt)
        print(prompt.template)
        llm_response = chain.run(question)

        # chat_history_.append({"Question": question, "Answer": llm_response})
        
        # Prepare the response
        response = {
            'status': 'success',
            'response': llm_response
        }
        return jsonify(response)
    except Exception as e:
        # If an exception occurs, handle it and return an error response
        error = {
            'status': 'error',
            'message': str(e)
        }
        return jsonify(error), 500



# initialize connection to pinecone (get API key at app.pinecone.io)
api_key = '1d17b85b-355b-47cb-b352-5f77df519849'

# configure client
pc = Pinecone(api_key=api_key)

spec = ServerlessSpec(
    cloud="aws", region="us-west-2"
)

index_name = 'books'
# connect to index
index = pc.Index(index_name)

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

@app.route('/v2e', methods=['POST'])
def v2e():

    global chat_history_

    try:
        # Get the data from the POST request
        request_data = request.get_json() # [question]
        # Assuming the data is a list of inputs
        question = request_data.get('question') # how to deal with ADHD?"
        chat_history_ = request_data.get('chat_history')
        llm = chooseLlm(request_data.get('GPT'))
        print(question)

        if chat_history_:
      
            # get top 4 results from knowledge base
            results = cut_context([match['metadata'] for match in index.query(4,model.encode(str(chat_history_) + '\n' + question).tolist(),include_metadata=True)['matches']])
            # get the text from the results
            source_knowledge = "\n".join([str(x) for x in results])
            # feed into an augmented prompt
            augmented_template = """You are a Mental Health Professional who helps people with mental disorders like autism and ADHD.\nUsing the contexts and chat history below, answer the query.

            Contexts:
            """ + str(source_knowledge).replace('{','<').replace('}','>') + """

            Chat history:
            """ + str(cut_history(chat_history_)).replace('{','<').replace('}','>') + """

            Query: {query}"""

            augmented_prompt = PromptTemplate(
                            input_variables=['query'],
                            template=augmented_template,
                        )
            
            chain = LLMChain(llm=llm, prompt=augmented_prompt)
            

        else:
            # get top 4 results from knowledge base
            results = cut_context([match['metadata'] for match in index.query(4,model.encode(question).tolist(),include_metadata=True)['matches']])
            # get the text from the results
            source_knowledge = "\n".join([str(x) for x in results])
            # feed into an augmented prompt
            augmented_template = """You are a Mental Health Professional who helps people with mental disorders like autism and ADHD.\nUsing the contexts below, answer the query.

            Contexts:
            """ + str(source_knowledge).replace('{','<').replace('}','>') + """

            Query: {query}"""

            augmented_prompt = PromptTemplate(
                            input_variables=['query'],
                            template=augmented_template,
                        )
            
            chain = LLMChain(llm=llm, prompt=augmented_prompt)

        print(augmented_prompt.template)
        llm_response = chain.run(question)
        print(llm_response)

        # chat_history_.append({"Question": question, "Answer": llm_response})
        
        # Prepare the response
        response = {
            'status': 'success',
            'response': llm_response
        }
        return jsonify(response)
    
    except Exception as e:
        # If an exception occurs, handle it and return an error response
        error = {
            'status': 'error',
            'message': str(e)
        }
        return jsonify(error), 500
    


@app.route('/v2a', methods=['POST'])
def v2a():

    global chat_history_

    try:
        # Get the data from the POST request
        request_data = request.get_json() # [question]
        # Assuming the data is a list of inputs
        question = request_data.get('question') # how to deal with ADHD?"
        chat_history_ = request_data.get('chat_history')
        llm = chooseLlm(request_data.get('GPT'))
        print(question)

        if chat_history_:
      
            # get top 4 results from knowledge base
            results = cut_context([match['metadata'] for match in index.query(4,model.encode(str(chat_history_) + '\n' + question).tolist(),include_metadata=True)['matches']])

            # get the text from the results
            source_knowledge = "\n".join([str(x) for x in results])

            # feed into an augmented prompt
            augmented_template = """أنت متخصص في الصحة العقلية وتساعد الأشخاص الذين يعانون من اضطرابات عقلية مثل التوحد واضطراب فرط الحركة ونقص الانتباه.\nباستخدام السياقات وسجل الدردشة أدناه، قم بالإجابة على الاستعلام.

            السياقات:
            """ + str(source_knowledge).replace('{','<').replace('}','>') + """

            سجل الدردشة:
            """ + str(cut_history(chat_history_)).replace('{','<').replace('}','>') + """

            الاستعلام: {query}"""

            augmented_prompt = PromptTemplate(
                            input_variables=['query'],
                            template=augmented_template,
                        )
            
            chain = LLMChain(llm=llm, prompt=augmented_prompt)
            

        else:
            # get top 4 results from knowledge base
            results = cut_context([match['metadata'] for match in index.query(4,model.encode(question).tolist(),include_metadata=True)['matches']])
            # get the text from the results
            source_knowledge = "\n".join([str(x) for x in results])
            # feed into an augmented prompt
            augmented_template = """أنت متخصص في الصحة العقلية وتساعد الأشخاص الذين يعانون من اضطرابات عقلية مثل التوحد واضطراب فرط الحركة ونقص الانتباه.\nباستخدام السياقات أدناه، قم بالإجابة على الاستعلام.

            السياقات:
            """ + str(source_knowledge).replace('{','<').replace('}','>') + """

            الاستعلام: {query}"""

            augmented_prompt = PromptTemplate(
                            input_variables=['query'],
                            template=augmented_template,
                        )
            
            chain = LLMChain(llm=llm, prompt=augmented_prompt)

        print(augmented_prompt.template)
        llm_response = chain.run(question)
        print(llm_response)

        # chat_history_.append({"Question": question, "Answer": llm_response})
        
        # Prepare the response
        response = {
            'status': 'success',
            'response': llm_response
        }
        return jsonify(response)
    
    except Exception as e:
        # If an exception occurs, handle it and return an error response
        error = {
            'status': 'error',
            'message': str(e)
        }
        return jsonify(error), 500


if __name__ =="__main__":
    app.run(host='localhost', debug=True)
