from langchain_groq import ChatGroq
from langchain.memory import ConversationSummaryMemory 
from langchain.chains import ConversationChain
import streamlit as st
from streamlit_chat import message 
# from dotenv import load_dotenv

# load_dotenv()

if 'container' not in st.session_state:
    st.session_state['container'] = None
if 'messages' not in st.session_state:
    st.session_state["messages"] = []
if 'api_key' not in st.session_state:
    st.session_state["api_key"] = ""


# UI starts here
st.set_page_config(page_title="ChatGPT clone app", page_icon=":robot:", layout = "wide")
st.markdown("<h1 style='text-align: center; color: black;'>How can I help you today?</h1>", unsafe_allow_html=True)

st.sidebar.title("Welcome!")
st.session_state["api_key"] = st.sidebar.text_input(
    "Enter your Hugging Face API key", type="password"
)
summary = st.sidebar.button("Get Summary", key=
"summary")
if summary:
    summary_placeholder = st.sidebar.write(
        "Summary:\n\n" + st.session_state["container"].memory.buffer
    )


# backend starts here
def getResponse(user_input, api_key):
    if st.session_state['container'] is None:
        llm = ChatGroq(
            model_name="llama-3.1-8b-instant",
            temperature=.6,
            max_tokens= 50,
            top_p=0.8,
            api_key=api_key,
        )

        st.session_state["container"] = ConversationChain(
            llm=llm, verbose=True, memory=ConversationSummaryMemory(llm = llm)
        )
    response = st.session_state["container"](
        f"{user_input} (Please respond in under 50 words)"
    )
    print(st.session_state["container"].memory.buffer)
    return response['response']

# container for chatting
response_container = st.container()
# container for text input
container = st.container()

with container:
    with st.form(key="my_form", clear_on_submit=True):
        user_input = st.text_input("Write your query here! ", placeholder="Type your message here...", key="input")
        submit_button = st.form_submit_button(label="Send")

        if submit_button and user_input:
            st.session_state["messages"].append(user_input)
            model_response = getResponse(user_input, st.session_state["api_key"])
            st.session_state["messages"].append(model_response)
            # st.write(st.session_state["messages"])
            with response_container:
                for i in range(len(st.session_state["messages"])):
                    if (i%2) == 0:
                        message(st.session_state["messages"][i], is_user=True, key=str(i)+'_user')
                    else:
                        message(st.session_state["messages"][i], is_user=False, key=str(i)+'_bot')
