# 🤖 ChatGPT Clone App

This is a simple ChatGPT clone app built using **Langchain**, **Groq LLM (LLaMA-3)**, and **Streamlit**. It provides an interactive chatbot experience right in your browser. The app maintains chat history and can summarize your conversation using a sidebar feature.

## ✨ Features

- Chat with a powerful LLM (LLaMA-3 via Groq API)
- Clean Streamlit-based web UI
- Maintains conversation memory
- Option to generate summary of the chat
- Customisable response length
- Friendly chatbot experience

## 🧠 Technologies Used

- [Langchain](https://www.langchain.com/)
- [Groq API](https://console.groq.com/)
- [Streamlit](https://streamlit.io/)
- [streamlit-chat](https://github.com/AI-Yash/st-chat)
- [Python-dotenv](https://pypi.org/project/python-dotenv/)

## 📦 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Zoya28/ChatGPT-clone.git
   cd ChatGPT-clone
    ````

2. **Create and activate a virtual environment**

   ```bash
   python -m venv myenv
   source myenv/bin/activate  # On Windows: myenv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the app**

   ```bash
   streamlit run app.py
   ```

## 📝 Usage

* Enter your query in the input box.
* The model will respond in real time.
* Use the sidebar to:

  * Enter API key otherwise you will get an eror
  * Get a summary of your chat
* Responses are limited to \~50 words (but can be customized).

## 📁 Project Structure

```
📦 chatgpt-clone-app/
├── app.py
├── .env
├── requirements.txt
├── README.md
└── ...
```

## 👩‍💻 Made with ❤️ by Zoya Qureshi

Feel free to fork, star ⭐, and contribute!
