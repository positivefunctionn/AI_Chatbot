
# ==================================================
# 1. FIX CREWAI CACHE BREAKPOINT ISSUE WITH GROQ
# ==================================================

import sys
import types

import crewai.llms.cache as crewai_cache


def disable_cache_breakpoint(message):
    """Prevent unsupported cache_breakpoint metadata."""
    if isinstance(message, dict):
        message.pop("cache_breakpoint", None)

    return message


# Patch the original function
crewai_cache.mark_cache_breakpoint = disable_cache_breakpoint


# Import CrewAI after patching its cache module
from crewai import Agent, Task, Crew, LLM
from groq import Groq

from config import GROQ_API_KEY, GROQ_MODEL

from memory_manager import MemoryManager

from token_optimizer import (
    optimize_messages,
    optimize_summary
)


# Patch any CrewAI modules that imported the original function
for module_name, module in list(sys.modules.items()):

    if (
        module_name.startswith("crewai.")
        and isinstance(module, types.ModuleType)
        and hasattr(module, "mark_cache_breakpoint")
    ):

        setattr(
            module,
            "mark_cache_breakpoint",
            disable_cache_breakpoint
        )


# ==================================================
# 2. CHATBOT ENGINE
# ==================================================

class ChatbotEngine:

    def __init__(self):

        # Initialize conversation memory
        self.memory = MemoryManager()

        # Initialize Groq API client
        self.groq_client = Groq(
            api_key=GROQ_API_KEY
        )

        # Initialize CrewAI language model
        self.llm = LLM(
            model=f"groq/{GROQ_MODEL}",
            api_key=GROQ_API_KEY,
            temperature=0.5,
            max_tokens=1024
        )

        # Create CrewAI agent
        self.agent = Agent(

            role="AI Chatbot Assistant",

            goal=(
                "Provide accurate, useful and friendly "
                "answers while maintaining conversation context."
            ),

            backstory=(
                "You are an intelligent AI assistant who "
                "understands conversation history, remembers "
                "important details and communicates clearly."
            ),

            llm=self.llm,

            verbose=False,

            allow_delegation=False
        )

        print("Chatbot Engine Initialized Successfully!")

    # ==================================================
    # 3. CONVERSATION SUMMARIZATION
    # ==================================================

    def summarize_old_messages(self, session_id):

        history = self.memory.get_history(session_id)

        messages = history["messages"]

        # Summarize when conversation exceeds 12 messages
        if len(messages) <= 12:
            return

        # Select older messages
        old_messages = messages[:-6]

        conversation_text = "\n".join(
            f"{message['role']}: {message['content']}"
            for message in old_messages
        )

        previous_summary = history.get("summary", "")

        try:

            # Use Groq to summarize older messages
            response = self.groq_client.chat.completions.create(

                model=GROQ_MODEL,

                messages=[
                    {
                        "role": "system",
                        "content": (
                            "Summarize the conversation briefly. "
                            "Preserve important facts, preferences, "
                            "decisions and unresolved questions. "
                            "Remove repetition and unnecessary details."
                        )
                    },

                    {
                        "role": "user",
                        "content": (
                            f"Previous summary:\n{previous_summary}\n\n"
                            f"New conversation:\n{conversation_text}"
                        )
                    }
                ],

                temperature=0.2,

                max_tokens=300
            )

            summary = (
                response.choices[0].message.content or ""
            )

            # Optimize generated summary
            optimized_summary = optimize_summary(summary)

            # Update conversation summary
            self.memory.update_summary(
                session_id,
                optimized_summary
            )

            # Retain latest six messages
            history["messages"] = messages[-6:]

            print("Conversation summarized successfully!")

        except Exception as error:

            print("Summarization Error:", str(error))

    # ==================================================
    # 4. GENERATE AI RESPONSE
    # ==================================================

    def get_response(self, session_id, user_message):

        try:

            # Store user message
            self.memory.add_message(
                session_id,
                "user",
                user_message
            )

            # Summarize older messages if required
            self.summarize_old_messages(session_id)

            # Retrieve conversation history
            history = self.memory.get_history(session_id)

            # Retrieve conversation context
            context = self.memory.get_context(session_id)

            # Optimize conversation messages
            context = optimize_messages(context)

            # Convert context into text
            context_text = "\n".join(
                f"{message['role']}: {message['content']}"
                for message in context
            )

            # Include previous conversation summary
            summary = history.get("summary", "")

            if summary:

                context_text = (
                    "PREVIOUS CONVERSATION SUMMARY:\n"
                    + summary
                    + "\n\nRECENT CONVERSATION:\n"
                    + context_text
                )

            # Create CrewAI task
            task = Task(

                description=(
                    "Answer the user's latest question using "
                    "the conversation context below.\n\n"

                    "CONVERSATION CONTEXT:\n"
                    "{conversation_context}\n\n"

                    "LATEST USER QUESTION:\n"
                    "{question}\n\n"

                    "Instructions:\n"
                    "1. Maintain conversation continuity.\n"
                    "2. Use previous information when relevant.\n"
                    "3. Do not invent personal facts.\n"
                    "4. Avoid unnecessary repetition.\n"
                    "5. Give clear and helpful answers."
                ),

                expected_output=(
                    "A relevant, natural and context-aware "
                    "answer to the user's latest question."
                ),

                agent=self.agent
            )

            # Create Crew
            crew = Crew(

                agents=[self.agent],

                tasks=[task],

                verbose=False
            )

            # Execute CrewAI task
            result = crew.kickoff(

                inputs={
                    "question": user_message,
                    "conversation_context": context_text
                }
            )

            answer = str(result).strip()

            if not answer:
                raise ValueError(
                    "The AI returned an empty response."
                )

            # Store assistant response
            self.memory.add_message(
                session_id,
                "assistant",
                answer
            )

            return answer

        except Exception as error:

            print("\n========== CHATBOT ERROR ==========")

            print("Error Type:", type(error).__name__)

            print("Error Details:", str(error))

            print("===================================\n")

            raise

    # ==================================================
    # 5. CLEAR CONVERSATION
    # ==================================================

    def clear_conversation(self, session_id):

        self.memory.clear_memory(session_id)

        print("Conversation memory cleared successfully!")
