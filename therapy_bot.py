import streamlit as st
import json
import torch
import re
import random
from sentence_transformers import SentenceTransformer, util
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

PAGE_TITLE = "NeuroTherapy AI: Ultimate Edition"
PAGE_ICON = "🧠"
DATABASE_FILE = "mindfulness_db.json"
MODEL_NAME = "google/flan-t5-base"

#DATA SANITIZATION LAYER
class DataSanitizer:
    @staticmethod
    def clean(text):
        if not text: return ""
        # Remove URLs
        text = re.sub(r'http\S+|www\.\S+', '', text)
        # Remove emails
        text = re.sub(r'\S+@\S+', '', text)
        # Genericize names
        text = re.sub(r'(?i)\b(dr\.|mr\.|mrs\.|ms\.)\s+[A-Z][a-z]+', 'the therapist', text)
        # Remove office locations
        text = re.sub(r'(?i)(serving|located in|office in)\s+[A-Z][a-z]+', '', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text[:1000]


# SAFETY SYSTEM
class SafetySystem:
    def __init__(self):
        self.crisis_keywords = [
            "suicide", "kill myself", "want to die", "end it all", "shoot myself",
            "self-harm", "cutting", "overdose", "hurt myself", "kill", "killing"
        ]


    def scan(self, text):
        if any(word in text.lower() for word in self.crisis_keywords):
            return "🚨 **CRITICAL ALERT:** Please contact emergency services (988) immediately."
        return None

# --- 3. NEURAL ENGINE ---
class NeuralEngine:
    def __init__(self):
        self.tokenizer = None
        self.model = None
        self.retriever = None
        self.corpus_embeddings = None
        self.db_data = []
        self._initialize_models()

    def _initialize_models(self):
        with st.status("Initializing Neural Core...", expanded=True) as status:
            st.write("📂 Loading Knowledge Graph...")
            try:
                with open(DATABASE_FILE, 'r', encoding='utf-8') as f:
                    self.db_data = json.load(f)
            except Exception:
                self.db_data = []
            
            st.write("🔎 Loading Semantic Search...")
            self.retriever = SentenceTransformer('all-MiniLM-L6-v2')
            self._vectorize_database()

            st.write(f"🤖 Loading Generator ({MODEL_NAME})...")
            self.tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
            self.model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)
            
            status.update(label="System Online", state="complete", expanded=False)

    def _vectorize_database(self):
        corpus_text = []
        self.responses = []
        for entry in self.db_data:
            pat_list = entry.get('patterns', [])
            if isinstance(pat_list, str): pat_list = [pat_list]
            corpus_text.append(" ".join(pat_list))
            self.responses.append(entry.get('response', ""))
            
        if corpus_text:
            self.corpus_embeddings = self.retriever.encode(corpus_text, convert_to_tensor=True)

    def analyze_tokens(self, text):
        """Debug function for Sidebar Tokenization"""
        tokens = self.tokenizer.tokenize(text)
        ids = self.tokenizer.encode(text)
        # Zip them for display
        return list(zip(tokens, ids))

    def retrieve(self, query):
        if self.corpus_embeddings is None: return None, 0.0
        query_vec = self.retriever.encode(query, convert_to_tensor=True)
        scores = util.cos_sim(query_vec, self.corpus_embeddings)[0]
        best_idx = scores.argmax().item()
        return self.responses[best_idx], scores[best_idx].item()

    def generate_response(self, user_input, db_advice):
        clean_advice = DataSanitizer.clean(db_advice)
        
        # PROMPT: Force "Supportive" persona and remove locations
        input_text = (
            f"Task: You are a helpful AI counselor. \n"
            f"User says: '{user_input}'. \n"
            f"Reference Advice: {clean_advice}\n\n"
            f"Instructions:\n"
            f"1. Answer the user using the Advice.\n"
            f"2. REMOVE any specific locations (like 'Houston'), office hours, or doctor names.\n"
            f"3. Expand with an example if possible."
        )
        
        input_ids = self.tokenizer(input_text, return_tensors="pt").input_ids

        for attempt in range(2):
            outputs = self.model.generate(
                input_ids,
                max_length=350,
                min_length=50,
                do_sample=True,
                temperature=0.7,
                repetition_penalty=2.5,
                no_repeat_ngram_size=3
            )
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Clean artifacts
            response = response.replace("Instructions:", "").replace("Reference Advice:", "").strip()
            
            if self._verify_quality(response):
                return response, clean_advice

        return "I hear you. Could you tell me more about how this is affecting your daily life?", clean_advice

    def _verify_quality(self, text):
        lower = text.lower()
        if "instruction" in lower: return False
        if "houston" in lower or "office" in lower: return False 
        if len(text) < 20: return False
        return True

# UI SETUP
st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON, layout="wide")

# CSS: Ensure readability
st.markdown("""
<style>
    .stChatMessage { border-radius: 10px; padding: 10px; }
    .stStatus { border: 1px solid #4CAF50; }
    .reportview-container { background: #f0f2f6; }
</style>
""", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hello. I am here to listen. How are you feeling?"}]
if "engine" not in st.session_state:
    st.session_state.engine = NeuralEngine()
if "safety" not in st.session_state:
    st.session_state.safety = SafetySystem()

#SIDEBAR tokenization
with st.sidebar:
    st.header("🛠️ Neuro-Debugger")
    st.info("Visualizing how the AI reads your input.")
    token_expander = st.expander("🔠 Live Tokenization", expanded=True)

st.title(f"{PAGE_ICON} {PAGE_TITLE}")
st.caption("Features: New Kaggle Database + Live Tokenization + RAG")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if "meta" in msg:
            with st.expander("See Source Context"):
                st.write(msg["meta"])

if prompt := st.chat_input("Type here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    if alert := st.session_state.safety.scan(prompt):
        with st.chat_message("assistant"): st.error(alert)
        st.stop()

    engine = st.session_state.engine
    
    # VISUALIZE TOKENS (SIDEBAR)
    tokens = engine.analyze_tokens(prompt)
    with token_expander:
        st.write(f"**Tokens ({len(tokens)}):**")
        st.code(tokens)

    #  CONTEXT CONSTRUCTION
    # Combine previous bot answer + current user input for better search
    search_query = prompt
    if len(st.session_state.messages) > 2:
        prev_bot = st.session_state.messages[-2]["content"]
        search_query = f"{prev_bot[-60:]} {prompt}"

    with st.chat_message("assistant"):
        with st.status("🧠 Processing...", expanded=True) as status:
            
            st.write(f"🔍 Searching DB for: '{search_query[:50]}...'")
            raw_advice, score = engine.retrieve(search_query)
            
            if score < 0.20:
                status.update(label="⚠️ Low Confidence", state="error")
                final_response = "I'm listening. Could you clarify that a little bit?"
                clean_context = "None"
            else:
                st.write(f"✅ Context Found (Score: {score:.2f})")
                st.write("✍️ Generating & Filtering...")
                final_response, clean_context = engine.generate_response(prompt, raw_advice)
                status.update(label="Response Ready", state="complete", expanded=False)

            meta = {"context_used": clean_context[:100] + "..."}

        st.markdown(final_response)
        st.session_state.messages.append({"role": "assistant", "content": final_response, "meta": meta})