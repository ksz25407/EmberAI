import random

def analyze_tone(reply: str) -> str:
    reply_lower = reply.lower()
    score = {
        "energy": 0,
        "sarcasm": 0,
        "frustration": 0
    }
    
    # Energy
    if reply.count('!') > 0 or any(word in reply_lower for word in ['great', 'awesome', 'brilliant', 'fantastic']):
        score["energy"] += 8
    if any(word in reply_lower for word in ['okay', 'fine', 'sure']):
        score["energy"] += 4
    
    # Sarcasm / Mischief
    if any(word in reply_lower for word in ['really', 'sure', 'oh', 'wow', 'buddy', 'pal']):
        score["sarcasm"] += 7
    if reply_lower.endswith('?') or reply.count('...') > 0:
        score["sarcasm"] += 6
    if any(word in reply_lower for word in ['joke', 'pun', 'genius', 'cmon']):
        score["sarcasm"] += 9
    
    # Frustration / Annoyance
    if any(word in reply_lower for word in ['error', 'fail', 'watch it', 'careful', 'damn']):
        score["frustration"] += 8
    if any(word in reply_lower for word in ['sorry', 'oops']):
        score["frustration"] += 5
    
    # Decide emotion
    top_emotion = max(score, key=score.get)
    top_score = score[top_emotion]
    
    if top_score < 5:
        return "neutral"
    
    if top_emotion == "energy":
        return "happy"
    elif top_emotion == "sarcasm":
        return random.choice(["mischievous", "playful"])
    elif top_emotion == "frustration":
        return "angry"
    else:
        return "neutral"
