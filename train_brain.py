import json
import os
import glob
import pandas as pd
import kagglehub

OUTPUT_FILE = "mindfulness_db.json"

def train_brain():
    print("⬇️  Downloading dataset from Kaggle...")
    try:
        path = kagglehub.dataset_download("birdy654/human-and-llm-mental-health-conversations")
        print(f"✅ Downloaded to: {path}")
    except Exception as e:
        print(f"❌ Error downloading: {e}")
        return

    # find the CSV file in the download folder
    csv_files = glob.glob(os.path.join(path, "*.csv"))
    if not csv_files:
        print("❌ No CSV found in the downloaded folder.")
        return
    
    csv_path = csv_files[0]
    print(f"📂 Processing: {csv_path}")

    df = pd.read_csv(csv_path)
    
    new_entries = []
    

    print(f"   Columns found: {list(df.columns)}")
    
   
    col_map = {
        'question': ['Context', 'Instruction', 'User', 'text', 'prompt'],
        'answer': ['Response', 'Output', 'Assistant', 'response', 'completion']
    }
    
    q_col = next((c for c in df.columns if c in col_map['question']), None)
    a_col = next((c for c in df.columns if c in col_map['answer']), None)

    if not q_col or not a_col:
        print("❌ Could not automatically identify Question/Answer columns.")
        print(f"   Please open the CSV and check headers: {df.columns}")
        return

    print(f"   Mapping: Question='{q_col}' -> Answer='{a_col}'")

    for _, row in df.iterrows():
        q_text = str(row[q_col]).strip()
        a_text = str(row[a_col]).strip()
        
        if len(q_text) > 5 and len(a_text) > 10:
            new_entries.append({
                "patterns": [q_text],
                "response": a_text,
                "source": "kaggle_birdy654"
            })

    print(f"💾 Saving {len(new_entries)} new conversational pairs...")
    
    if os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE, 'r', encoding='utf-8') as f:
            existing = json.load(f)
        combined = existing + new_entries
    else:
        combined = new_entries
        
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(combined, f, indent=2, ensure_ascii=False)
        
    print(f"🚀 Success! Database now has {len(combined)} entries.")

if __name__ == "__main__":
    train_brain()