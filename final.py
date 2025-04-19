import os
import json
import streamlit as st
import PyPDF2
from langchain.output_parsers import *
import speech_recognition as sr
from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq

# ========== PAGE CONFIGURATION ==========
st.set_page_config(page_title="Personalized Learning Assistant", page_icon="📚", layout="wide")

# ========== LOAD ENV VARIABLES ==========
load_dotenv(dotenv_path=".env")

# Load environment variables safely
groq_api_key = os.getenv("GROQ_API")
langchain_api_key = os.getenv("LANGCHAIN_API_KEY")

if not langchain_api_key:
    st.error("LANGCHAIN_API_KEY is not set in the environment file.")
    st.stop()

os.environ["LANGCHAIN_API_KEY"] = langchain_api_key
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGSMITH_TRACING"] = "true"
os.environ["LANGSMITH_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGSMITH_API_KEY"] = os.getenv("LANGSMITH_API_KEY", "")
os.environ["LANGSMITH_PROJECT"] = os.getenv("LANGSMITH_PROJECT", "")
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY", "")

# ========== SESSION STATE INIT ==========
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []
    st.session_state.generated_text = ""

# ========== CUSTOM CSS ==========
def add_custom_css():
    st.markdown("""
        <style>
        h1 {color: #4CAF50; text-align: center; font-family: 'Courier New';}
        h2, h3 {color: #3a7ca5;}
        .stTextInput>div>div>input {
            border: 2px solid #4CAF50;
            color: #3a7ca5;
        }
        div.stButton>button {
            background-color: #4CAF50;
            color: white;
            border-radius: 12px;
            padding: 10px;
            font-size: 18px;
        }
        .css-1d391kg {background-color: #e8f4fa;}
        footer {visibility: hidden;}
        </style>
    """, unsafe_allow_html=True)

def render_symbols(symbol):
    st.markdown(f"<h1 style='text-align: center;'>{symbol}</h1>", unsafe_allow_html=True)

# ========== LOAD LLM ==========
@st.cache_resource
def load_model():
    return ChatGroq(
        model="llama3-8b-8192",
        groq_api_key=groq_api_key,
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2
    )

# ========== PROMPT TEMPLATE ==========
def get_prompt():
    return ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant. Please respond to the user's queries."),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}")
    ])

# ========== PDF EXTRACTION ==========
def extract_text_from_pdf(uploaded_file):
    reader = PyPDF2.PdfReader(uploaded_file)
    return ''.join(page.extract_text() or '' for page in reader.pages)

# ========== VOICE INPUT ==========
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎤 Listening...")
        audio = recognizer.listen(source)

    try:
        st.info("🔍 Recognizing...")
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        st.error("Could not understand audio.")
    except sr.RequestError:
        st.error("Speech recognition service error.")
    return ""

# ========== SAVE JSON ==========
def save_to_json_file(filename, data):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

# ========== UI ELEMENTS ==========
add_custom_css()
render_symbols("📚")
st.title('Your Personalized Learning Assistant 🧠')
st.subheader("Ask questions or upload a PDF for AI assistance.")

with st.sidebar:
    st.header("🛠 Options")
    uploaded_file = st.file_uploader("📄 Upload PDF", type="pdf")
    use_voice_input = st.checkbox("🎙 Use Voice Input")
    generate_mcqs = st.checkbox("📝 Generate MCQs")

st.markdown("### Ask your question")
st.write("Type or speak your query below.")

# ========== PROCESSING ==========
pdf_text = extract_text_from_pdf(uploaded_file) if uploaded_file else ""

if uploaded_file:
    st.success("✅ PDF uploaded and processed!")
    with st.expander("🔎 View Extracted PDF Text"):
        st.write(pdf_text)

input_text = st.text_input("Enter your question:")

if use_voice_input and st.button("🎤 Record"):
    input_text = recognize_speech()
    st.text_input("Voice Input Result:", value=input_text, disabled=True)

llm = load_model()

if input_text:
    if pdf_text and input_text.lower() in pdf_text.lower():
        st.markdown("### 📚 Found in PDF:")
        st.write(f"Query: '{input_text}' found in PDF content.")
        st.session_state.generated_text = pdf_text
    else:
        prompt = get_prompt()
        messages = prompt.format_messages(
            history=st.session_state.conversation_history,
            input=input_text
        )
        response = llm.invoke(messages)

        # Update history
        st.session_state.conversation_history.extend([
            {"role": "human", "content": input_text},
            {"role": "assistant", "content": response.content}
        ])
        st.session_state.generated_text = response.content

    # Show conversation
    st.markdown("### 🗣 Conversation History")
    with st.expander("📜 View Chat"):
        for msg in st.session_state.conversation_history:
            role = "You" if msg["role"] == "human" else "Assistant"
            icon = "🤔" if msg["role"] == "human" else "💬"
            st.markdown(f"**{role}:** {msg['content']} {icon}")
            st.markdown("---")

# ========== MCQ GENERATION ==========
if generate_mcqs and st.session_state.generated_text:
    with st.spinner("🧠 Generating MCQs..."):
        mcq_prompt = f"""
        You are an expert quiz maker. Create 10 multiple-choice questions (MCQs) on the topic below:
        
        Topic:
        {st.session_state.generated_text}
        
        Format as HTML with:
        - <h2> for each question
        - <ul><li> for options
        - No explanations
        """

        chain = ChatPromptTemplate.from_messages([("user", mcq_prompt)]) | llm | StrOutputParser()
        mcq_html = chain.invoke({"input": mcq_prompt})

        # Save & download
        with open("generated_mcqs.html", "w") as f:
            f.write(mcq_html)

        st.success("MCQs generated successfully! 🎉")
        st.download_button("📥 Download MCQs", data=mcq_html, file_name="generated_mcqs.html", mime="text/html")
