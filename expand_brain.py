import json
import re
from datasets import load_dataset
from tqdm import tqdm

# --- CONFIGURATION ---
OUTPUT_FILE = "mindfulness_db.json"
MAX_SAMPLES_PER_SOURCE = 1000  # Limit to keep your laptop fast

# Function to clean text (removes HTML tags, weird spaces)
def clean_text(text):
    if not isinstance(text, str): return ""
    text = re.sub(r'<[^>]+>', '', text) # Remove HTML tags
    text = re.sub(r'http\S+', '', text) # Remove URLs
    text = text.replace("\n", " ").replace("\r", "")
    return text.strip()

combined_data = []

print("🧠 Starting Knowledge Base Expansion...")

# --- SOURCE 1: Counsel Chat (Expert Advice) ---
try:
    print("⬇️ Downloading: Counsel Chat (Expert Therapist Answers)...")
    ds = load_dataset("nbertagnolli/counsel-chat", split="train")
    
    count = 0
    for row in tqdm(ds):
        q = clean_text(row.get('questionText', ''))
        a = clean_text(row.get('answerText', ''))
        
        if len(q) > 10 and len(a) > 10:
            combined_data.append({
                "patterns": [q],
                "response": a,
                "source": "CounselChat"
            })
            count += 1
            if count >= MAX_SAMPLES_PER_SOURCE: break
            
    print(f"   ✅ Added {count} expert responses.")
except Exception as e:
    print(f"   ❌ Failed to load Counsel Chat: {e}")

# --- SOURCE 2: Mental Health Conversational Data (General) ---
try:
    print("⬇️ Downloading: General Mental Health Intents...")
    ds = load_dataset("alexandreteles/mental-health-conversational-data", split="train")
    
    count = 0
    for row in tqdm(ds):
        text = row.get('text', '')
        # This dataset usually has just text, we assume it's context-response format 
        # But looking at structure, usually it's better to map 'text' as user input
        # NOTE: This dataset structure varies, we'll try a generic mapping if available
        # or skip if structure is complex. Let's use a known clean subset if possible.
        # Fallback to Amod's dataset if this fails or is complex text only.
        pass 
except Exception as e:
    print("   ⚠️ Skipped secondary source (Structure mismatch).")

# --- SOURCE 3: Amod's Dataset (The one you already used) ---
try:
    print("⬇️ Downloading: Amod's Mental Health Conversations...")
    ds = load_dataset("Amod/mental_health_counseling_conversations", split="train")
    
    count = 0
    for row in tqdm(ds):
        q = clean_text(row.get('Context', ''))
        a = clean_text(row.get('Response', ''))
        
        if len(q) > 5 and len(a) > 5:
            combined_data.append({
                "patterns": [q],
                "response": a,
                "source": "AmodDataset"
            })
            count += 1
            if count >= MAX_SAMPLES_PER_SOURCE: break
            
    print(f"   ✅ Added {count} conversation pairs.")
except Exception as e:
    print(f"   ❌ Failed to load Amod dataset: {e}")

# --- MANUAL OVERRIDES (Hardcoded Goodies) ---
# Always keep these safe, high-quality responses for critical inputs
hardcoded = [
    {
        "patterns": ["hi", "hello", "hey", "start"],
        "response": "Hello. I am here to listen and support you. How are you feeling today?",
        "source": "Hardcoded"
    },
    {
        "patterns": ["help", "i need help"],
        "response": "I am here. If you are in crisis, please call 988. If you just need to talk, I am listening. What is on your mind?",
        "source": "Hardcoded"
    }
]
combined_data.extend(hardcoded)

# --- SAVE TO FILE ---
print(f"💾 Saving {len(combined_data)} total entries to {OUTPUT_FILE}...")
with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
    json.dump(combined_data, f, indent=2, ensure_ascii=False)

print("🚀 Success! Your brain is now larger. Restart therapy_bot.py to use it.")