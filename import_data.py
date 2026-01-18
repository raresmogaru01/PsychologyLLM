import json
from datasets import load_dataset
import tqdm # Progress bar


DATASET_NAME = "Amod/mental_health_counseling_conversations"
OUTPUT_FILE = "mindfulness_db.json"
LIMIT = 500  # Start with 500 to keep the bot fast. Set to None for all data.

def build_database():
    print(f"📥 Downloading dataset '{DATASET_NAME}'...")
    
    # Load the dataset (split='train' is usually where the data is)
    try:
        ds = load_dataset(DATASET_NAME, split="train")
    except Exception as e:
        print(f"❌ Error downloading: {e}")
        print("Tip: You might need to run `huggingface-cli login` in terminal first if the dataset is gated.")
        return

    print(f"✅ Download complete. Found {len(ds)} conversations.")
    
    formatted_data = []
    
    # iterate through the dataset and transform it
    count = 0
    for row in ds:
        user_text = row.get('Context', '')
        bot_text = row.get('Response', '')
        
        if not user_text or not bot_text:
            continue
            
        entry = {
            "patterns": [user_text],  # the user's problem acts as the "pattern"
            "response": bot_text,     # the dataset's answer
            "category": "General Counseling"
        }
        
        formatted_data.append(entry)
        count += 1
        
        if LIMIT and count >= LIMIT:
            break
    
    # save to JSON
    print(f"💾 Saving {len(formatted_data)} entries to {OUTPUT_FILE}...")
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(formatted_data, f, indent=2, ensure_ascii=False)
        
    print("🚀 Done! You can now run 'python -m streamlit run therapy_bot.py'")

if __name__ == "__main__":
    build_database()