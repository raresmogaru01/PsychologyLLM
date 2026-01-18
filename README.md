# PsychologyLLM

🧠 Private AI Therapist (Local RAG & Generative AI)
A privacy-focused, offline therapeutic chatbot designed to simulate supportive conversations using Cognitive Behavioral Therapy (CBT) and Solution-Focused Brief Therapy (SFBT) frameworks.

Unlike standard chatbots that send your personal data to the cloud, this project runs 100% locally on your CPU using Retrieval-Augmented Generation (RAG). It combines a curated database of therapeutic knowledge with a local Large Language Model (LLM) to generate empathetic, context-aware responses.

🚀 Key Features
🔒 100% Privacy: No data leaves your machine. No OpenAI API keys required.

🧠 Local RAG Architecture: Uses semantic search (Sentence-Transformers) to find relevant therapeutic techniques from a local database.

🤖 Generative AI: Uses Google Flan-T5 to rewrite retrieved advice into natural, empathetic responses.

🛡️ Safety Guardrails: Built-in "Safety Layer" that detects crisis keywords (self-harm, suicide) and intervenes immediately with emergency resources.

⚡ Hybrid Logic: Prevents "hallucination loops" by using hardcoded logic for greetings and high-confidence retrieval for complex problems.

🛠️ Tech Stack
Language: Python 3.9+

Interface: Streamlit

LLM (Generative): google/flan-t5-base (via Hugging Face Transformers)

Embeddings (Retrieval): all-MiniLM-L6-v2 (via Sentence-Transformers)

Data Source: Hugging Face Datasets (Amod/mental_health_counseling_conversations)


1. Clone the Repository

2. Install Dependencies
Note: If you are using Python 3.13, you may need to use Python 3.11 if PyTorch is not yet supported.

Bash
# Windows
python -m pip install -r requirements.txt -r req.txt


Plaintext
streamlit
torch
transformers
sentence-transformers
datasets
scikit-learn

3. Build the Knowledge Base
Run the import script to download real therapeutic conversations from Hugging Face and create your local JSON database.

Bash
python import_data.py
Output: This will generate a file named mindfulness_db.json (~2-5MB).

4. Run the Application
Start the Streamlit server. We use python -m to avoid path issues on Windows.

Bash
python -m streamlit run therapy_bot.py
The app will open automatically in your browser at http://localhost:8501.

🧩 How It Works (The Logic)
Input: User types "I feel anxious about my job."

Safety Scan: The system checks for crisis keywords. If found, it blocks execution and shows emergency numbers.

Retrieval (The "Memory"):

The system converts the user's text into a mathematical vector.

It searches mindfulness_db.json for the most similar therapeutic advice using Cosine Similarity.

Generation (The "Voice"):

The Flan-T5 model receives a prompt: "Rewrite this advice to be kind: [Retrieved Advice]"

It generates a fresh, unique response to avoid sounding robotic.

Anti-Looping: Post-processing logic ensures the AI doesn't repeat itself or get stuck in a loop.

🔧 Customization
Change the Model: Open therapy_bot.py and change MODEL_NAME.

Faster: "google/flan-t5-small"

Smarter (Recommended): "google/flan-t5-base"

Expert (Requires 16GB RAM): "google/flan-t5-large"

Edit the Database: You can manually open mindfulness_db.json and add your own Q&A pairs to teach the bot specific techniques.

⚠️ Troubleshooting
1. pip is not recognized Use python -m pip install ... instead of just pip install ....

2. UnicodeDecodeError when running the bot Ensure your therapy_bot.py loads the JSON file with UTF-8 encoding: with open(self.db_file, 'r', encoding='utf-8') as f:

3. The bot repeats "I'm sorry" or "I am a therapist" Ensure you are using the updated code with repetition_penalty=2.5 inside the generate_reply function.

⚕️ Medical Disclaimer
This software is for educational and experimental purposes only.

It is not a replacement for professional medical advice, diagnosis, or treatment.

The AI can hallucinate or provide incorrect information.

If you or someone you know is in crisis, please call emergency services (911 in US, 999 in UK, 112 in EU) or contact a suicide prevention hotline (988 in the US).
