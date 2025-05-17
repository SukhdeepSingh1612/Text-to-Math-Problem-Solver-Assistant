import streamlit as st
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, LLMMathChain
from langchain.agents import initialize_agent, Tool
from langchain.agents.agent_types import AgentType
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.callbacks import StreamlitCallbackHandler

## Setup the streamlit app
st.set_page_config(
    page_title="Text to Math Problem Solver And Data search Assistant",
    page_icon="🦙",
    layout="wide",
)

st.title("Text to Math Problem Solver And Data search Assistant using Google Gemma2")

groq_api_key = st.sidebar.text_input(label="Enter your Groq API Key", type="password")

if not groq_api_key:
    st.info("Please enter your Groq API Key to use the app.")
    st.stop()


llm = ChatGroq(model = "gemma2-9b-it", groq_api_key=groq_api_key)

## initialize the tools
wikipedia_wrapper = WikipediaAPIWrapper()
wikipedia_wrapper = Tool(
    name="Wikipedia",
    func=wikipedia_wrapper.run,
    description="A tool to search Wikipedia for information.",
)

math_chain = LLMMathChain.from_llm(llm=llm)
calculator = Tool(
    name="Calculator",
    func=math_chain.run,
    description="A tool to perform calculations.",
)

prompt = """
You are a agent tasked for solving users mathematical questions. Logically arrive at the solution and provide a detailed explaination
and display it point wise for the question below.
Question: {question}
Answer: 
"""


prompt_template = PromptTemplate(
    input_variables=["question"],
    template=prompt
)



## combine all tools into chain - MathsProblem tool

chain = LLMChain(llm=llm, prompt=prompt_template)

reasoning_tool = Tool(
    name="Reasoning tool",
    func=chain.run,
    description="A tool to solve mathematical problems and provide detailed explanations.",
)

## initialize the agent

assistant_agent  =  initialize_agent(
    tools=[wikipedia_wrapper, calculator, reasoning_tool],
    llm=llm,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=False,
    handle_parsing_errors=True
)

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hello! I am your math problem solver and data search assistant. How can I help you today?",
        }
    ]


for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

## function to generate response

def generate_response(user_question):
     response = assistant_agent.invoke({'input': user_question})
     return response


## Lets start the interaction

question = st.text_input("Enter your question here", "What is the sum of 2 and 3?")

if st.button("find my answer"):
    if question:
            with st.spinner("Generating response..."):
                 st.session_state.messages.append({"role": "user", "content": question})
                 st.chat_message("user").write(question)
                 st_cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts =False)
                 response = assistant_agent.run(st.session_state.messages, callbacks=[st_cb])

                 st.session_state.messages.append({"role": "assistant", "content": response})
                 st.write('### Response')
                 st.success(response)
    else: 
         st.warning("Please enter a question to get a response.")
     










