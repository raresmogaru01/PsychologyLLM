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
