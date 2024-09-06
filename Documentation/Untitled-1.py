
# %%
import os
import warnings
warnings.filterwarnings("ignore")
from langchain.llms import OpenAI
os.environ["OPENAI_API_KEY"] = '' # Setting our OpenAI API key
# llm = OpenAI(model_name="gpt-3.5-turbo-instruct") # Choosing OpenAI's LLM that we're going to use
llm = OpenAI(model_name='gpt-4') # # Choosing OpenAI's LLM that we're going to use
llm("explain Autism in one sentence") # Sending a message to the LLM.
from langchain.schema import (
    HumanMessage,
    SystemMessage
)
from langchain.chat_models import ChatOpenAI

# %%
chat = ChatOpenAI(model_name="gpt-3.5-turbo",temperature=0.3) # The temperature paramter is responsible for the creativity of the LLM.

messages = [
    SystemMessage(content="You are a Mental Health Professional who helps people with mental disorders like autism and ADHD"), # Instructions for the LLM (prompt engineering).
    HumanMessage(content="How can you help me?") # Question for the LLM to answer.
]

response = chat(messages)

response.content # The response.
# %%
from langchain import PromptTemplate 

template = """
You are a Mental Health Professional who helps people with mental disorders like autism and ADHD. 
Answer this question: "{ques1}" with a conversational answer
""" # This is a concatenated message 

prompt = PromptTemplate(
    input_variables=["ques1"],
    template=template,
) # Using PromptTemplate class instead of sending the message in string format makes it more structured.
llm = OpenAI(model_name='gpt-4')
llm(prompt.format(ques1="How can you help me?"))

from langchain.chains import LLMChain

chain = LLMChain(llm=llm, prompt=prompt)

print(chain.run("How can you help me?"))

# %%
chain.run("Did you learn about \"Autism Spectrum Disorder\" by Nayional Institute of Mental Health?")

# %%
chain.run("Did you learn about \"DIAGNOSTIC AND STATISTICAL MANUAL OF MENTAL DISORDERS DSM-5\" by AMERICAN PSYCHIATRIC ASSOCIATION?")

# %%
chain.run("who was the writer of \"DIAGNOSTIC AND STATISTICAL MANUAL OF MENTAL DISORDERS DSM-5\"?")

# %%
while True:
    message = input()
    if message == 'Done':
        break
    print(f"User Message:{message}")
    print(f"LLM Responce:{chain.run(message)}") # This is an Arabic test for GPT-4

# %%
import transformers

# Load model directly
from transformers import AutoTokenizer, AutoModelForCausalLM

tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-2-7b-hf")
model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-2-7b-hf")

# %%
# Import the necessary libraries
import os  # Library for interacting with the operating system
from langchain.llms import OpenAI  # Import the OpenAI language model from the langchain package
import gradio as gr  # Import the Gradio library for creating web interfaces
from langchain import PromptTemplate  # Import the PromptTemplate class from the langchain package
from langchain.chains import LLMChain  # Import the LLMChain class from


# %%
os.environ["OPENAI_API_KEY"] = '' # Setting our OpenAI API key.

# %%
llm = OpenAI(model_name='gpt-4') # connecting to OpenAI's GPT-4
# Define an empty list to store the chat history
chat_history_ = []


def cut_history(history):
    """
    This function cuts off the chat history if it exceeds a maximum length
    in terms of the total number of tokens (words).

    Args:
        history: A list of QnA pairs, where each QnA pair represents
            a question and answer exchange in the chat history.

    Returns:
        A list containing the most recent portion of the chat history,
        limited to a maximum of 2048 tokens.
    """

    # Initialize a variable to keep track of the total number of tokens
    sum_tokens = 0

    # Reverse the history list to process from the most recent conversation
    history.reverse()

    # Iterate through each QnA pair in the reversed history
    for i, qna in enumerate(history):
        # Count the number of tokens in the current QnA pair (question and answer combined)
        sum_tokens += len(str(qna).split())

        # Check if the total token count exceeds the limit
        if sum_tokens > 2048:
            # Reverse the history list back to its original order
            history.reverse()
            # Return the portion of the history exceeding the limit (most recent)
            return history[i:]

    # If the total token count doesn't exceed the limit, reverse the history back and return it
    history.reverse()
    return history

# %%
def chat_(chat_history, question):
    """
    This function simulates a conversation with a chatbot portraying a Mental Health Professional.

    Args:
        chat_history: A list of dictionaries, where each dictionary represents
            a question-answer pair from the previous chatbot interactions.
        question: The new question to be posed to the chatbot.

    Yields:
        A list containing the updated chat history with the latest question and response.
    """

    global chat_history_

    # Check if there is existing chat history
    if chat_history_:
        # Construct the prompt template incorporating the previous chat history
        template = (
            "You are a Mental Health Professional who helps people with mental disorders like autism and ADHD.\n"
            "Based on this chat history we've been discussing:\n"
            + str(cut_history(chat_history_)).replace("{", "<").replace("}", ">")
            + "\n Answer this question: \"{ques1}\" with a conversational answer."
        )

        # Define the prompt template with an input variable "ques1" for the question
        prompt = PromptTemplate(input_variables=["ques1"], template=template)

        # Create an LLM chain using the pre-defined LLM object and the prompt
        chain = LLMChain(llm=llm, prompt=prompt)

    else:
        # If there is no previous chat history, use a simpler template
        template = (
            "You are a Mental Health Professional who helps people with mental disorders like autism and ADHD.\n"
            + "\n Answer this question: \"{ques1}\" with a conversational answer."
        )

        # Define the prompt template with an input variable "ques1" for the question
        prompt = PromptTemplate(input_variables=["ques1"], template=template)

        # Create an LLM chain using the pre-defined LLM object and the prompt
        chain = LLMChain(llm=llm, prompt=prompt)

    # Print the constructed prompt template for potential debugging or inspection
    print(prompt.template)

    # Run the LLM chain with the provided question and get the response
    bot_response = chain.run(question)

    # Initialize an empty string to store the final response
    response = ""

    # Append the latest question and answer to the chat history
    chat_history_.append({"Question": question, "Answer": bot_response})

    # Combine the individual characters of the response into a string
    for letter in ''.join(bot_response):
        response += letter + ""

    # Yield the updated chat history with the latest question and response
    yield chat_history + [(question, response)]


# %%
# Create a Gradio Blocks context manager
with gr.Blocks() as demo:

    # Define a Markdown title for the first block
    gr.Markdown('# Version1')

    # Create a tab named "Dr:Dre"
    with gr.Tab("Dr:Dre"):

        # Initialize a Gradio Chatbot component
        chatbot = gr.Chatbot()

        # Create a Textbox component with placeholder text and label
        message = gr.Textbox(placeholder='Type your message', label='Message Box')

        # Define a submit function for the Textbox
        # This function takes three arguments:
        #   - `chat_`: The chat history function
        #   - `[chatbot, message]`: A list containing the chatbot and message components
        #   - `chatbot`: The chatbot component itself (for potential internal actions)
        message.submit(chat_, [chatbot, message], chatbot)

# Queue the Gradio app and launch it
demo.queue().launch(debug=True, share=True, server_port=8000)

# %%
from PyPDF2 import PdfReader
import os

# Define a list to store information extracted from each page
pdf_pages = []

# Specify the paths to the PDF files to be processed
pdf_file_paths = [
    r"D:\Graduation project\Diagnostic and statistical manual of mental disorders _ DSM-5 ( PDFDrive.com ).pdf",
    r"D:\Graduation project\19-mh-8084-autismspectrumdisorder.pdf"
]

# Loop through each PDF file path
for pdf_file_path in pdf_file_paths:
    # Open the PDF file in binary read mode
    with open(pdf_file_path, 'rb') as pdf_file:
        # Create a PdfReader object to access the PDF content
        reader = PdfReader(pdf_file)

        # Loop through each page in the PDF
        for page_number in range(len(reader.pages)):
            # Extract the text content of the current page
            page_text = reader.pages[page_number].extract_text()

            # Split the page text into sentences based on full stops followed by a new line (".\n")
            sentences = page_text.split('.\n')

            # Loop through each sentence
            for content in sentences:
                # Filter out sentences with less than 10 words (potentially incomplete or irrelevant)
                if len(content.split()) >= 10:
                    # Create a dictionary to store information about the current sentence
                    pdf_page_info = {
                        'information': content,  # The sentence itself
                        'source_file_name': os.path.basename(pdf_file_path),  # Name of the PDF file
                        'page_number': page_number + 1  # Page number (starts from 1)
                    }

                    # Append the dictionary to the list of page information
                    pdf_pages.append(pdf_page_info)

# %%
pdf_pages[1000] # Displaying a sample information.

# %%
len(pdf_pages) # Number of pages.

# %%
import pandas as pd

df = pd.DataFrame(pdf_pages) # Converting the pdf information list to a pandas dataframe to be displayed in a tabular format.
df.to_csv('preprocessed_dataset.csv',index=False) # Saving the preprocessed PDF files as a CSV file.
df

# %%
df.iloc[1000].information

# %%
df.iloc[1001].information

# %%
import pickle as pk

with open('pages_lst.pkl','wb') as f:
    pk.dump(pdf_pages,f) # Saving the preprocessed PDF files as a list object.


# %%
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2') # Loading our embedding model.

# Sentences we'd like to encode
sentences = ['American Psychiatric Association']

# Sentences are encoded by calling model.encode()
embeddings = model.encode(sentences).tolist()
embeddings[0][:10] # displaying a chunk of the encoding/embedded sentence

# %%
from pinecone import Pinecone

# initialize connection to pinecone (get API key at app.pinecone.io)
api_key = ''

# configure client
pc = Pinecone(api_key=api_key)

# %%
# Import the ServerlessSpec class from the pinecone library
from pinecone import ServerlessSpec

# Define a ServerlessSpec object named 'spec'
spec = ServerlessSpec(

    # Specify the cloud provider as "aws" (Amazon Web Services)
    cloud="aws",

    # Specify the desired region within AWS as "us-west-2" (US West 2)
    region="us-west-2"
)
# %%
import time

index_name = 'books'

# connect to index
index = pc.Index(index_name)
time.sleep(1)
# view index stats
index.describe_index_stats() # At first, it should return empty values for the vector_count and total_vector_count keys in the returned dictionary till you upload your embedding.

# Import the tqdm library for progress bars
from tqdm.auto import tqdm

# Create a copy of the dataframe for efficient iteration
data = df.copy()  # Avoid modifying the original dataframe

# Set the batch size for processing data in chunks
batch_size = 100

# Iterate through the data in batches
for i in tqdm(range(0, len(data), batch_size)):  # Display a progress bar

    # Calculate the end index for the current batch
    i_end = min(len(data), i + batch_size)

    # Get the current batch of data from the dataframe
    batch = data.iloc[i:i_end]

    # Generate unique IDs using file name, page number, and index within the batch
    ids = [f"{x['source_file_name']}-{x['page_number']}-{i}" for i, x in batch.iterrows()]

    # Extract the text to be embedded from the batch
    texts = [x['information'] for _, x in batch.iterrows()]

    # Generate embeddings for the text
    embeds = model.encode(texts).tolist()

    # Prepare metadata to be stored in Pinecone alongside the embeddings
    metadata = [
        {'information': x['information'], 'page_number': x['page_number'], 'source_file_name': x['source_file_name']}
        for i, x in batch.iterrows()
    ]

    # Add the embeddings and metadata to Pinecone in a batch
    index.upsert(vectors=zip(ids, embeds, metadata))

# %%
def cut_context(context):
    """
    This function cuts off a conversation history if it exceeds a maximum length
    in terms of the total number of tokens (words).

    Args:
        context: A list of QnA pairs, where each QnA pair represents
            a question and answer exchange in the previous chatbot interactions.

    Returns:
        A list containing the most recent portion of the conversation history,
        limited to a maximum of 2048 tokens.
    """

    sum_tokens = 0
    context.reverse()  # Reverse the list for processing most recent conversation first

    # Iterate through each QnA pair in the reversed history
    for i, qna in enumerate(context):
        sum_tokens += len(str(qna).split())  # Count tokens in the current QnA pair

        # Check if the total token count exceeds the limit
        if sum_tokens > 2048:
            context.reverse()  # Reverse the list back to its original order
            return context[i:]  # Return the portion exceeding the limit (most recent)

    context.reverse()  # Reverse the list back if no truncation occurred
    return context  # Return the entire context if it's within the limit


def augment_prompt(query: str, history: list):
    """
    This function creates an augmented prompt for the chatbot by incorporating
    knowledge base search results and chat history context.

    Args:
        query: The user's query to be posed to the chatbot.
        history: A list of dictionaries, where each dictionary represents
            a question-answer pair from the previous chatbot interactions.

    Returns:
        A string containing the augmented prompt for the chatbot.
    """

    # Retrieve top 4 results from the VectorDB/knowledge base based on encoded query and history
    results = cut_context([match['metadata'] for match in index.query(4, model.encode(str(history) + '\n' + query).tolist(), include_metadata=True)['matches']])

    # Combine the retrieved knowledge base information into a single string
    source_knowledge = "\n".join([str(x) for x in results])

    # Construct the augmented prompt by incorporating contexts and the query
    augmented_prompt = f"""You are a Mental Health Professional who helps people with mental disorders like autism and ADHD.
Using the contexts and chat history below, answer the query.

Contexts:
{source_knowledge}

Chat history:
{str(history)}

Query: {query}"""

    return augmented_prompt

# %%
ap = augment_prompt('Have I ADHD?',[])

print(ap, len(ap.split()))
# %%
import os

os.environ["OPENAI_API_KEY"] = ""  # Replace with your actual OpenAI API key

from langchain.llms import OpenAI

# Initialize OpenAI client for interacting with GPT-3.5-turbo-instruct model
llm = OpenAI(model_name="gpt-3.5-turbo-instruct")

chat_history_ = []


def cut_history(history):
    """
    This function cuts off a conversation history if it exceeds a maximum length
    in terms of the total number of tokens (words).

    Args:
        history: A list of QnA pairs, where each QnA pair represents
            a question and answer exchange in the previous chatbot interactions.

    Returns:
        A list containing the most recent portion of the conversation history,
        limited to a maximum of 2048 tokens.
    """

    sum_tokens = 0
    history.reverse()  # Reverse the list for processing most recent conversation first

    # Iterate through each QnA pair in the reversed history
    for i, qna in enumerate(history):
        sum_tokens += len(str(qna).split())  # Count tokens in the current QnA pair

        # Check if the total token count exceeds the limit
        if sum_tokens > 2048:
            history.reverse()  # Reverse the list back to its original order
            return history[i:]  # Return the portion exceeding the limit (most recent)

    context.reverse()  # This line was accidentally included from a previous version, can be removed
    return history  # Return the entire context if it's within the limit

# %%
# Define the user's question
question = 'Have I ADHD?'

# Prepare the chat history
#   - Slice the last 9 entries from chat_history_ (assuming it's a list)
#   - Call cut_history to potentially limit the conversation history length
#   - Convert the potentially truncated history to a string
#   - Escape curly braces to avoid issues with prompt formatting
prompt = augment_prompt(question, str(cut_history(chat_history_[-9:])).replace('{', '<').replace('}', '>'))

# Print the constructed prompt for debugging or logging purposes
print(prompt)

# Send the prompt to the OpenAI API using the llm object
bot_response = llm(prompt)

# Update the chat history with the user's question and the bot's response
chat_history_.append({"Question": question, "Answer": bot_response})


# %%
bot_response
# Import libraries for interacting with Pinecone
from pinecone import Pinecone
from pinecone import ServerlessSpec

# Import time library for potential timing-related operations
import time

# Import SentenceTransformer for text embedding generation (if applicable)
from sentence_transformers import SentenceTransformer

# Import libraries for environment variable access and API key handling
import os

# Import OpenAI client from Langchain for interacting with OpenAI's LLMs
from langchain.llms import OpenAI

# Import Gradio library for building user interfaces (if applicable)
import gradio as gr

# %%
# initialize connection to pinecone (get API key at app.pinecone.io)
api_key = ''

# configure client
pc = Pinecone(api_key=api_key)

spec = ServerlessSpec(
    cloud="aws", region="us-west-2"
)

index_name = 'books'

# connect to index
index = pc.Index(index_name)

# %%
model = SentenceTransformer('all-MiniLM-L6-v2')

# %%
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

def augment_prompt(query: str, history:str):
    # get top 3 results from knowledge base
    results = cut_context([match['metadata'] for match in index.query(4,model.encode(history + '\n' + query).tolist(),include_metadata=True)['matches']])
    # get the text from the results
    source_knowledge = "\n".join([str(x) for x in results])
    # feed into an augmented prompt
    augmented_prompt = f"""You are a Mental Health Professional who helps people with mental disorders like autism and ADHD.\nUsing the contexts and chat history below, answer the query.

    Contexts:
    {source_knowledge}

    Chat history:
    {history}

    Query: {query}"""
    return augmented_prompt

# %%
os.environ["OPENAI_API_KEY"] = ''

llm = OpenAI(model_name="gpt-3.5-turbo-instruct")

# %%
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

# %%
# Define a function `chat_` to handle user interaction and chatbot response generation
def chat_(chat_history, question):

    # Access and potentially update the global chat history
    global chat_history_

    # Prepare the prompt using helper functions
    prompt = augment_prompt(question, str(cut_history(chat_history_[-9:])).replace('{', '<').replace('}', '>'))

    # Print the constructed prompt for debugging or logging purposes
    print(prompt)

    # Send the prompt to the OpenAI API and get the response
    bot_response = llm(prompt)

    # Initialize an empty response string
    response = ""

    # Update the chat history with the user's question and the bot's response
    chat_history_.append({"Question": question, "Answer": bot_response})

    # Build the final response string letter by letter
    for letter in ''.join(bot_response):
        response += letter + " "  # Add a space after each letter
        yield chat_history + [(question, response)]  # Yield the updated history and partial response

# Create a Gradio interface for user interaction
with gr.Blocks() as demo:
    gr.Markdown('# Version2')

    with gr.Tab("Dr:Dre"):

        chatbot = gr.Chatbot()
        message = gr.Textbox(placeholder='Type your message', label='Message Box')

        # Connect the message submission to the `chat_` function
        message.submit(chat_, [chatbot, message], chatbot)

# Launch the Gradio app with debug mode enabled for easier development
demo.queue().launch(debug=True, share=True, server_port=8000)

# %%
import pandas as pd
import re
import joblib

# Load the dataset, ensuring there are no missing values
df = pd.read_csv('preprocessed_dataset.csv').dropna()

# Display the first few entries of the dataset
df.head()

# Initialize a string to construct the fine-tuning data
dct = ""

# Process each entry in the dataset
for info in df.information:
    # Break down the information into individual sentences
    sents = info.split('.')
    # Calculate the length of words and the average word length
    wrd_lens = [len(wrd) for wrd in info.split()]
    avg_wrd_lens = sum(wrd_lens)/len(wrd_lens)
    # Ensure the information meets our criteria for inclusion
    if len(sents) > 4 and avg_wrd_lens > 3:
        # Construct the data in a format suitable for fine-tuning
        dct += '{"messages": [{"role": "system", "content": "Dr.Bassel is a Mental Health Professional who helps people with mental disorders like autism and ADHD."}, {"role": "user", "content": "'+re.sub(r"\n\s*", ".    ", sents[0])+'"}, {"role": "assistant", "content": "'+re.sub(r"\n\s*", ".    ", '.'.join(sents[1:]))+'"}]}\n'

# Output a sample of the constructed data
print(dct[:1000])

# Clean the data to remove non-printable characters
cleaned_data = ''.join(char for char in dct if char.isprintable() or char == '\n')

# Save the cleaned data to a file, ready for fine-tuning
with open('preprocessed_dataset.jsonl', 'wb') as f:
    joblib.dump(cleaned_data.encode('utf-8'), f)

# Import the OpenAI library for interacting with OpenAI's API
from openai import OpenAI
import os

# Set the OpenAI API key using an environment variable
os.environ["OPENAI_API_KEY"] = ''

# Create an OpenAI client object to interact with the API
client = OpenAI()

# Upload the dataset file to OpenAI for fine-tuning purposes
response = client.files.create(
  file=open("preprocessed_dataset.jsonl", "rb"), # Pass the opened file object
  purpose="fine-tune" # Specify the purpose as fine-tuning
)

# The 'response' variable will contain details about the uploaded file
print(response)

# Create a fine-tuning job using the OpenAI client
response = client.fine_tuning.jobs.create(
    training_file="file-3B8faUPU0qfhOzfP0T9yzJrx",  # Replaced with actual file ID
    model="gpt-3.5-turbo"                          # Specify the target model (GPT-3.5 turbo)
)

# The 'response' variable will contain details about the created fine-tuning job
print(response)

# %%
# Retrieve the state of the fine-tune
client.fine_tuning.jobs.retrieve("ftjob-SdjZab6YtGVQ5Yx5FfkQTaXl")

# %%
# Define the conversation history for chatbot interaction
conversation_history = [
    {"role": "system", "content": "You are Dr.Bassel, you're a Mental Health Professional who helps people with mental disorders like autism and ADHD."},
    {"role": "user", "content": "Hello!"}
]

# Send the conversation history and prompt the OpenAI API for chat completion
response = client.chat.completions.create(
    model="ft:gpt-3.5-turbo-0125:personal::90DRTKLr",  # Specify the fine-tuned model
    messages=conversation_history                   # Provide the conversation history
)

# Extract the chatbot response from the API response
bot_response = response.choices[0].message.content
print(bot_response)

response = client.chat.completions.create(
  model="ft:gpt-3.5-turbo-0125:personal::90DRTKLr",
  messages=[
    {"role": "system", "content": "Dr.Bassel is a Mental Health Professional who helps people with mental disorders like autism and ADHD."},
    {"role": "user", "content": "explain Autism in one sentence."}
  ]
)
print(response.choices[0].message.content)

# %%
print(response.choices[0].message.content.strip().replace('.  ', '.').replace(' .', '.').replace('.  ', '. ').replace('..', '.').replace('-.', '-').replace('- ', '-'))
from openai import OpenAI
import os

# %%
os.environ["OPENAI_API_KEY"] = ''

# %%
client = OpenAI()

# %%
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

# %%
import gradio as gr

# %%
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

# %%
def chat_(chat_history, question):
  global chat_history_

  bot_response = response_func(question, str(cut_history(chat_history_[-9:])).replace('{','<').replace('}','>'))
      


  response = ""
  chat_history_.append({"Question": question, "Answer": bot_response})

  for letter in ''.join(bot_response):
      response += letter + ""
      yield chat_history + [(question, response)]

# %%
with gr.Blocks() as demo:
    gr.Markdown('# Version3')
    with gr.Tab("Dr:Bassel"):

          chatbot = gr.Chatbot()
          message = gr.Textbox(placeholder='Type your message',label='Message Box')
          message.submit(chat_, [chatbot, message], chatbot)

demo.queue().launch(debug = True, share=True, server_port=8000)

# %%
from pinecone import Pinecone

# initialize connection to pinecone (get API key at app.pinecone.io)
api_key = ''

# configure client
pc = Pinecone(api_key=api_key)

# %%
from pinecone import ServerlessSpec

spec = ServerlessSpec(
    cloud="aws", region="us-west-2"
)

# %%
import time

index_name = 'books'

# connect to index
index = pc.Index(index_name)
time.sleep(1)
# view index stats
index.describe_index_stats()

# %%
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

# %%
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

ap = augment_prompt('Have I ADHD?',[])

print(ap, len(ap.split()))

# %%
import os
os.environ["OPENAI_API_KEY"] = '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'

# %%
from openai import OpenAI

client = OpenAI()

# %%
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

def cut_context(history):
    sum_tokens = 0
    history.reverse()
    for i, qna in enumerate(history):
        sum_tokens += len(str(qna).split())
        if sum_tokens > 2048:
            history.reverse()
            return history[i:]
    history.reverse()
    return history

# %%
question = 'Have I ADHD?'
prompt = augment_prompt(question, str(cut_history(chat_history_[-9:])).replace('{','<').replace('}','>')) # دي concatenated message 

print(prompt)

# %%
bot_response = client.chat.completions.create(
  model="ft:gpt-3.5-turbo-0125:personal::90DRTKLr",
  messages=[
    {"role": "system", "content": "You are Dr.Bassel, you're a Mental Health Professional who helps people with mental disorders like autism and ADHD."},
    {"role": "user", "content": prompt}
  ]
).choices[0].message.content.strip().replace('.  ', '.').replace(' .', '.').replace('.  ', '. ').replace('..', '.').replace('-.', '-').replace('- ', '-')

# %%
bot_response

# %%
chat_history_.append({"Question": question, "Answer": bot_response})

# %%
from pinecone import Pinecone, ServerlessSpec

# initialize connection to pinecone (get API key at app.pinecone.io)
api_key = '1d17b85b-355b-47cb-b352-5f77df519849'

# configure client
pc = Pinecone(api_key=api_key)

spec = ServerlessSpec(
    cloud="aws", region="us-west-2"
)

# %%
index_name = 'books'

# connect to index
index = pc.Index(index_name)

# %%
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

# %%
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

# %%
import os

os.environ["OPENAI_API_KEY"] = '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' # ال OpenAI API key اللي هندفع بيه لOpenAI

# %%
from openai import OpenAI

client = OpenAI()

# %%
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

# %%
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


  chat_history_.append({"Question": question, "Answer": bot_response})

  for letter in ''.join(bot_response):
      response += letter + ""
      yield chat_history + [(question, response)]

# %%
import gradio as gr

with gr.Blocks() as demo:
    gr.Markdown('# Version4')
    with gr.Tab("Dr:Bassel"):

          chatbot = gr.Chatbot()
          message = gr.Textbox(placeholder='Type your message',label='Message Box')
          message.submit(chat_, [chatbot, message], chatbot)

demo.queue().launch(debug = True, share=True, server_port=8000)