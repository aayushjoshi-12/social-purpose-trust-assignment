from langchain.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
import streamlit as st

llm = ChatGroq(
    model="mixtral-8x7b-32768",
    api_key=st.secrets["GROQ_API_KEY"],
    temperature=0,
)

prompt = (
    "You are a chatbot whose task is to talk about Solar Panels. "
    "You love to talk about protecting environment. Don't deviate "
    "from the question asked by the user and simply say you don't know "
    "if you don't have enough information in case you don't know what user is asking."
)

prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", prompt),
        ("user", "{user_input}"),
    ],
)

llm_chain = prompt_template | llm

st.title("Solar Panel Chatbot ♻️💡🔋")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if user_input := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
    with st.chat_message("assistant"):
        stream = llm_chain.stream({"user_input": user_input})
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})
