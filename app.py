from langchain_groq import ChatGroq
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
import streamlit as st

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = InMemoryChatMessageHistory()
if 'messages' not in st.session_state:
    st.session_state["messages"] = []
if 'api_key' not in st.session_state:
    st.session_state["api_key"] = ""
if 'chain' not in st.session_state:
    st.session_state['chain'] = None

# UI Configuration
st.set_page_config(
    page_title="ChatGPT Clone App",
    page_icon="🤖",
    layout="wide"
)

st.markdown(
    "<h1 style='text-align: center; color: white;'>How can I help you today?</h1>",
    unsafe_allow_html=True
)

# Sidebar
st.sidebar.title("Welcome!")

# API Key input
api_key_input = st.sidebar.text_input(
    "Enter your Groq API key",
    type="password",
    help="Get your API key from https://console.groq.com",
    value=st.session_state["api_key"]
)

# Update API key and reset chain if key changes
if api_key_input != st.session_state["api_key"]:
    st.session_state["api_key"] = api_key_input.strip()  # Strip whitespace
    st.session_state['chain'] = None  # Reset chain when API key changes

# Clear chat button
if st.sidebar.button("Clear Chat History"):
    st.session_state['chat_history'].clear()
    st.session_state["messages"] = []
    st.rerun()

# Show conversation summary
if st.sidebar.button("Show Chat Summary"):
    if st.session_state['chat_history'].messages:
        st.sidebar.markdown("**Chat Summary:**")
        message_count = len(st.session_state['chat_history'].messages)
        st.sidebar.write(f"Total messages: {message_count}")
        st.sidebar.write(f"User messages: {message_count // 2}")
        st.sidebar.write(f"Assistant messages: {message_count // 2}")
    else:
        st.sidebar.write("No chat history yet.")

# Display API key status
if st.session_state["api_key"]:
    st.sidebar.success("API Key entered")
else:
    st.sidebar.warning("Please enter your API key")


# Backend Logic
def get_chat_chain(api_key):
    """Create a chat chain with message history"""
    try:
        llm = ChatGroq(
            model="llama-3.1-8b-instant",
            temperature=0.6,
            max_tokens=150,
            top_p=0.8,
            groq_api_key=api_key,
        )

        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful AI assistant. Provide clear and concise responses."),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{input}")
        ])

        chain = prompt | llm | StrOutputParser()

        chain_with_history = RunnableWithMessageHistory(
            chain,
            lambda session_id: st.session_state['chat_history'],
            input_messages_key="input",
            history_messages_key="history"
        )

        return chain_with_history
    except Exception as e:
        st.error(f"Failed to initialize chat chain: {str(e)}")
        return None


def get_response(user_input, api_key):
    """Generate response using Groq API and LangChain"""
    if not api_key or api_key.strip() == "":
        return "Please enter your Groq API key in the sidebar."

    try:
        if st.session_state['chain'] is None:
            st.session_state['chain'] = get_chat_chain(api_key)

        if st.session_state['chain'] is None:
            return "Failed to initialize chat. Please check your API key."

        response = st.session_state['chain'].invoke(
            {"input": user_input},
            config={"configurable": {"session_id": "default"}}
        )

        return response

    except Exception as e:
        error_msg = str(e)
        if "401" in error_msg or "invalid_api_key" in error_msg:
            return "Invalid API key. Please check your Groq API key and try again."
        elif "429" in error_msg:
            return "Rate limit reached. Please wait a moment and try again."
        else:
            return f"Error: {error_msg}"


# Chat Interface
st.markdown("---")

# Display chat history
chat_container = st.container()
with chat_container:
    for i in range(len(st.session_state["messages"])):
        if (i % 2) == 0:
            # User message
            with st.chat_message("user"):
                st.write(st.session_state["messages"][i])
        else:
            # Bot message
            with st.chat_message("assistant"):
                st.write(st.session_state["messages"][i])

# Chat input
user_input = st.chat_input("Type your message here...")

if user_input:
    if not st.session_state["api_key"]:
        st.error("Please enter your Groq API key in the sidebar first.")
    else:
        # Add user message to history
        st.session_state["messages"].append(user_input)

        # Get bot response
        with st.spinner("Thinking..."):
            model_response = get_response(user_input, st.session_state["api_key"])

        # Add bot response to history
        st.session_state["messages"].append(model_response)

        # Rerun to display new messages
        st.rerun()