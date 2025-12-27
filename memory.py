from collections import defaultdict, deque

MAX_HISTORY = 10
memory = defaultdict(lambda: deque(maxlen=MAX_HISTORY))

def add(channel_id, role, content):
    memory[channel_id].append({
        "role": role,
        "content": content
    })

def get(channel_id):
    return list(memory[channel_id])
