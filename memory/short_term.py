# Keep last N exchanges
history = []

def update_memory(user_input, ai_output, max_len=5):
    history.append((user_input, ai_output))
    if len(history) > max_len:
        history.pop(0)

def get_context():
    return "\n".join([f"User: {u}\nAssistant: {a}" for u, a in history])
