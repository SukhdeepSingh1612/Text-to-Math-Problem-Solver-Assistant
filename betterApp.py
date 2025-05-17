import streamlit as st
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, LLMMathChain
from langchain.agents import initialize_agent, Tool
from langchain.agents.agent_types import AgentType
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.callbacks import StreamlitCallbackHandler

# Page configuration
st.set_page_config(
    page_title="🧠 Math Solver & Data Assistant",
    page_icon="🧮",
    layout="wide",
)

# Title and Header
st.markdown("""
    <h1 style='text-align: center;'>🧠 Text to Math Problem Solver & Data Search Assistant</h1>
    <p style='text-align: center; font-size: 18px;'>Powered by Google Gemma 2 and LangChain</p>
    <hr>
""", unsafe_allow_html=True)

# Sidebar for API Key
with st.sidebar:
    st.header("🔐 Authentication")
    groq_api_key = st.text_input("Enter your Groq API Key", type="password")
    st.markdown("Get your API key from [groq.com](https://console.groq.com/)")

if not groq_api_key:
    st.info("Please enter your Groq API Key to use the app.")
    st.stop()

# Initialize the LLM
llm = ChatGroq(model="gemma2-9b-it", groq_api_key=groq_api_key)

# Tools
wiki_tool = Tool(
    name="Wikipedia",
    func=WikipediaAPIWrapper().run,
    description="A tool to search Wikipedia for information.",
)

math_chain = LLMMathChain.from_llm(llm=llm)
calculator_tool = Tool(
    name="Calculator",
    func=math_chain.run,
    description="A tool to perform calculations.",
)

prompt_template = PromptTemplate(
    input_variables=["question"],
    template="""
You are an agent tasked with solving users' mathematical questions. Logically arrive at the solution and provide a detailed explanation, displayed point-wise.
Question: {question}
Answer: 
""",
)

reasoning_tool = Tool(
    name="Reasoning Tool",
    func=LLMChain(llm=llm, prompt=prompt_template).run,
    description="A tool to solve mathematical problems with detailed steps.",
)

# Initialize agent
agent = initialize_agent(
    tools=[wiki_tool, calculator_tool, reasoning_tool],
    llm=llm,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=False,
    handle_parsing_errors=True
)

# Session state for chat
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "👋 Hello! I am your math and data assistant. Ask me anything!",
        }
    ]

# Display chat history
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# Main interaction
st.markdown("## 🤔 Ask a Question")

col1, col2 = st.columns([3, 1])
with col1:
    user_question = st.text_input("Type your question:", placeholder="e.g. What is 25 * 13 or Who discovered gravity?")

with col2:
    ask_button = st.button("🔍 Find Answer")

# Response generation
if ask_button and user_question:
    st.session_state.messages.append({"role": "user", "content": user_question})
    st.chat_message("user").write(user_question)

    with st.spinner("🤖 Thinking..."):
        st_cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts=False)
        try:
            response = agent.run(user_question, callbacks=[st_cb])
        except Exception as e:
            response = f"⚠️ Error: {str(e)}"
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.chat_message("assistant").write(response)

# Footer
st.markdown("---")
st.markdown(
    "<p style='text-align: center;'>Made with ❤️ using Streamlit, LangChain, and Groq's Gemma2</p>",
    unsafe_allow_html=True
)
