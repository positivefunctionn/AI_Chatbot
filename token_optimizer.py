
MAX_RECENT_MESSAGES = 10
MAX_SUMMARY_CHARS = 1500
MAX_MESSAGE_CHARS = 4000


def optimize_messages(messages):

    optimized = []

    for message in messages:
        content = message["content"]

        # Limit unusually long messages
        if len(content) > MAX_MESSAGE_CHARS:
            content = content[:MAX_MESSAGE_CHARS]

        optimized.append({
            "role": message["role"],
            "content": content
        })

    return optimized[-MAX_RECENT_MESSAGES:]


def optimize_summary(summary):

    return summary[:MAX_SUMMARY_CHARS]
