# 🏛️ Constitutional Law Chatbot  

Legal research in Pakistan is often complex and time-consuming. This project is an **AI-powered Constitutional Law Chatbot** that delivers **precise answers from the Constitution in seconds**, helping lawyers, students, and researchers save valuable time.  

---

## 🚀 Features  
- ⚖️ Provides accurate answers from the **Constitution of Pakistan**  
- ⚡ Fast and reliable responses using **Llama 3.3-70B (Groq LLM)**  
- 🔎 Context-aware retrieval with **LangChain + ChromaDB + HuggingFace embeddings**  
- 🌐 Simple, user-friendly interface built with **Flask + HTML/CSS**  

---

## 🛠️ Tech Stack  

- **Frontend:** Flask, HTML, CSS  
- **Backend:** Python, Flask  
- **LLM:** [Groq Llama-3.3-70B Versatile](https://groq.com)  
- **Vector DB:** ChromaDB  
- **Frameworks & Tools:** LangChain, HuggingFace Embeddings  

---

## 📂 Project Structure  

Constitutional-Law-Chatbot/
│── app.py # Main Flask app
│── requirements.txt # Dependencies
│── .env # API keys (not pushed to GitHub)
│── static/ # CSS, JS, images
│── templates/ # HTML files
│── data/ # Constitution dataset
│── README.md # Project documentation
│── .gitignore # Ignore sensitive files

yaml
Copy code

---

## ⚙️ Installation  

1. **Clone the repo**  
   ```bash
   git clone https://github.com/1Khizar/Constitutional-Law-Chatbot.git
   cd Constitutional-Law-Chatbot
Create virtual environment

bash
Copy code
python -m venv venv
source venv/bin/activate   # For Linux/Mac
venv\Scripts\activate      # For Windows
Install dependencies

bash
Copy code
pip install -r requirements.txt
Set up environment variables
Create a .env file in the project root:

ini
Copy code
GROQ_API_KEY=your_api_key_here
Run the app

bash
Copy code
python app.py
Open in browser

cpp
Copy code
http://127.0.0.1:5000/
📸 Demo
(Add screenshot here)

markdown
Copy code
![Constitutional Law Chatbot](static/screenshot.png)
👨‍💻 Author
Khizar Ishtiaq
📌 LinkedIn
