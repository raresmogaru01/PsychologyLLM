import json

data = [
    # --- GENERAL / GREETINGS ---
    {
        "patterns": ["hello", "hi", "hey", "start", "help me"],
        "response": "Hello. I am here to help you navigate your challenges. I use a mix of CBT (analyzing thoughts) and SFBT (finding solutions). What is the main thing on your mind right now?",
        "category": "General"
    },
    {
        "patterns": ["who are you", "what is this", "are you real"],
        "response": "I am a therapeutic decision-tree system designed to simulate a supportive conversation. I am not human, but I can help you structure your thoughts and find actionable steps forward.",
        "category": "General"
    },

    # --- ANXIETY (CBT Focused) ---
    {
        "patterns": ["anxious", "panic", "heart racing", "scared", "terrified"],
        "response": "It sounds like your anxiety is spiking. Let's pause. In CBT, we use 'Grounding'. Name 5 things you see, 4 you can touch, 3 you hear, 2 you smell, and 1 you taste. Take a deep breath. How does your body feel now?",
        "category": "Anxiety"
    },
    {
        "patterns": ["what if", "worst case", "catastrophe", "disaster"],
        "response": "You might be 'Catastrophizing'—assuming the worst will happen. Let's look at the evidence. What is the actual likelihood of this worst-case scenario happening? And if it did, what resources do you have to handle it?",
        "category": "Anxiety"
    },
    {
        "patterns": ["overwhelmed", "too much", "drowning", "can't cope"],
        "response": "When we look at the whole mountain, it's impossible to climb. SFBT suggests looking only at the next step. What is ONE tiny thing (takes less than 2 minutes) you could do right now to make the situation 1% better?",
        "category": "Anxiety"
    },

    # --- DEPRESSION (SFBT Focused) ---
    {
        "patterns": ["sad", "depressed", "unhappy", "cry", "tears"],
        "response": "I hear how heavy things feel right now. I want to honor that feeling. In Solution-Focused therapy, we look for 'exceptions'. When was the last time—even for 5 minutes—that things felt just a tiny bit lighter? What was different then?",
        "category": "Depression"
    },
    {
        "patterns": ["tired", "no energy", "bed", "can't move"],
        "response": "Depression steals our energy, making action feel impossible. We need 'Behavioral Activation'. We don't wait for motivation; we act to create it. Can you commit to just standing up and stretching for 30 seconds right now?",
        "category": "Depression"
    },
    {
        "patterns": ["hopeless", "pointless", "why bother"],
        "response": "It sounds like you are feeling disconnected from meaning. Let's try the 'Miracle Question'. If a miracle happened tonight and your problem was gone, what would be the very first small thing you'd notice differently tomorrow morning?",
        "category": "Depression"
    },

    # --- ANGER (CBT Focused) ---
    {
        "patterns": ["angry", "mad", "furious", "hate", "rage"],
        "response": "Anger is often a secondary emotion protecting us from hurt or fear. What thought crossed your mind right before the anger flared? Did you feel treated unfairly, or unsafe?",
        "category": "Anger"
    },
    {
        "patterns": ["unfair", "they did this", "blame"],
        "response": "It feels very unjust. However, focusing entirely on them leaves you powerless. What is within YOUR control in this situation? How do you want to behave so that you can be proud of yourself later?",
        "category": "Anger"
    },

    # --- SELF-ESTEEM ---
    {
        "patterns": ["stupid", "failure", "idiot", "useless"],
        "response": "That sounds like a harsh 'Inner Critic'. If a friend came to you with this exact mistake, would you call them useless? What would you say to them? Try saying that to yourself now.",
        "category": "Self-Esteem"
    },
    {
        "patterns": ["people hate me", "everyone thinks", "judgment"],
        "response": "This is called 'Mind Reading'—assuming we know what others are thinking. Do you have concrete evidence they think this, or is it possible they are focused on their own lives?",
        "category": "Self-Esteem"
    },
    
    # --- SLEEP ---
    {
        "patterns": ["cant sleep", "insomnia", "awake", "tossing turning"],
        "response": "Racing thoughts often keep us awake. Try a 'Worry Dump'. Write down every single worry on a piece of paper, tell them 'I will deal with you tomorrow', and put the paper away. Shall we try a breathing exercise too?",
        "category": "Sleep"
    },
    
    # --- FALLBACK ---
    {
        "patterns": ["default"],
        "response": "I am listening. I want to understand better. Can you rephrase that, or tell me specifically what feeling is most dominant right now?",
        "category": "General"
    }
]

with open("mindfulness_db.json", "w") as f:
    json.dump(data, f, indent=2)

print("Database rebuilt successfully with 50+ patterns!")