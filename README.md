# 🦙 Text to Math Problem Solver And Data Search Assistant


### Deployed on Streamlit : https://text-to-math-problem-solver-assistant-jczeef826zby6p8wbpqzzc.streamlit.app/
This is a **Streamlit-based web application** that uses **LangChain** and **Groq's Google Gemma 2 model** to assist users with solving mathematical problems and searching data from Wikipedia.

## 🚀 Features

- 🧠 **Math Reasoning Tool**: Solve math questions with step-by-step logic and explanations.
- 📚 **Wikipedia Search**: Retrieve and display relevant Wikipedia data.
- 🧮 **Calculator**: Perform complex calculations using LangChain's math chain.
- 💬 **Chat UI**: Maintain conversation context using a Streamlit chat interface.

## 🛠️ Built With

- [Streamlit](https://streamlit.io/)
- [LangChain](https://www.langchain.com/)
- [Groq API](https://console.groq.com/)
- Google Gemma2 9B Instruct Model
- Wikipedia API Wrapper

## 📦 Installation

1. **Clone the Repository**

```bash
git clone https://github.com/yourusername/your-repo-name.git
cd your-repo-name
```

2. **Install Dependencies**

```bash
pip install -r requirements.txt
```

3. **Run the App**

```bash
streamlit run app.py
```

> 🔐 You'll need a **Groq API Key** to run this app. You can input it in the sidebar when the app starts.

## 📥 Usage

1. Start the Streamlit server.
2. Enter your **Groq API key** in the sidebar.
3. Type a math question or general query in the text box.
4. Click **"find my answer"**.
5. Get an intelligent, step-by-step answer or relevant Wikipedia results!

## 📁 Project Structure

```
├── app.py              # Main Streamlit application
├── README.md           # This file
├── requirements.txt    # Python dependencies
```

## 🧠 Example Questions

- "What is the sum of 2 and 3?"
- "Explain the Pythagorean theorem."
- "Who is Albert Einstein?"
