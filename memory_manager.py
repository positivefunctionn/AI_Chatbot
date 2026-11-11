
class MemoryManager:

    def __init__(self):
        self.conversations = {}

    def get_history(self, session_id):
        if session_id not in self.conversations:
            self.conversations[session_id] = {
                "summary": "",
                "messages": []
            }

        return self.conversations[session_id]

    def add_message(self, session_id, role, content):
        history = self.get_history(session_id)

        history["messages"].append({
            "role": role,
            "content": content
        })

    def get_context(self, session_id):
        history = self.get_history(session_id)

        context = []

        if history["summary"]:
            context.append({
                "role": "system",
                "content": (
                    "Previous conversation summary: "
                    + history["summary"]
                )
            })

        context.extend(history["messages"])

        return context

    def update_summary(self, session_id, summary):
        history = self.get_history(session_id)
        history["summary"] = summary

    def clear_memory(self, session_id):
        self.conversations[session_id] = {
            "summary": "",
            "messages": []
        }
