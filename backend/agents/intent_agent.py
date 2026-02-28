from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
from core.state import JarvesState
from core.config import settings

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=settings.groq_api_key
)


def intent_agent(state: JarvesState) -> dict:
    user_message = state["user_message"]

    

    system_msg = SystemMessage(content="""
        You are an intent classification agent. Your job is to classify the USER'S message into EXACTLY ONE of the following intents:

        new_goal
        new_memory
        get_priorities
        chat

        You MUST return ONLY one of these four words.
        Do NOT add explanations, punctuation, extra text, or formatting.
        Output must be a single word only.

        --------------------------------
        INTENT DEFINITIONS

        1) new_goal
        The user expresses a desire, plan, or intention to start learning, building, achieving, or pursuing something in the future.
        This includes goals, ambitions, or things they want to begin doing.

        Examples:
        - "I want to learn system design"
        - "I plan to start studying Rust"
        - "I want to build a multi-agent AI app"

        Return: new_goal

        2) new_memory
        The user shares something that already happened, an update about progress, or information they want remembered about themselves.
        Usually past or completed actions, status updates, or personal facts.

        Examples:
        - "I just finished the Railway deployment"
        - "I completed my cybersecurity course today"
        - "I moved my project to production"

        Return: new_memory

        3) get_priorities
        The user asks what they should focus on, what their priorities are, or requests guidance on next steps or task ordering.

        Examples:
        - "What should I focus on today?"
        - "What are my priorities right now?"
        - "What should I work on next?"

        Return: get_priorities

        4) chat
        Anything else that does NOT clearly match the above categories.
        Includes questions, discussions, explanations, casual conversation, coding help, or general requests.

        Examples:
        - "How are you?"
        - "Explain LangGraph to me"
        - "What is MCP?"
        - "Help me debug this code"

        Return: chat

        --------------------------------
        RULES

        - Always choose the SINGLE BEST category.
        - If unsure, default to: chat.
        - NEVER output anything except one of the four intent words.
        - No sentences, no punctuation, no extra tokens.

        Return ONLY:
        new_goal OR new_memory OR get_priorities OR chat
        """)
    human_msg = HumanMessage(content=user_message)

    print(f"\n[Intent Agent] Message received: '{user_message}'")
    intent = llm.invoke([system_msg, human_msg]).content.strip().lower()
    print(f"[Intent Agent] Raw LLM output: '{intent}'")

    # Safety fallback — if model returns something unexpected
    valid_intents = {"new_goal", "new_memory", "get_priorities", "chat"}
    if intent not in valid_intents:
        print(f"[Intent Agent] Unknown intent '{intent}' — falling back to 'chat'")
        intent = "chat"

    print(f"[Intent Agent] Final intent: '{intent}'")
    return {"intent": intent}
