from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from core.state import JarvesState
from core.config import settings

llm = ChatOpenAI(
    model="mistralai/mistral-small-3.1-24b-instruct:free",
    openai_api_key=settings.openrouter_api_key,
    openai_api_base="https://openrouter.ai/api/v1"
)


def intent_agent(state: JarvesState) -> dict:
    user_message = state["user_message"]

    

    system_msg = SystemMessage(content="""
        You are an intent classification agent. Your job is to classify the USER'S message into EXACTLY ONE of the following intents:

        new_goal
        new_memory
        complete_goal
        get_priorities
        chat

        You MUST return ONLY one of these four words.
        Do NOT add explanations, punctuation, extra text, or formatting.
        Output must be a single word only.

        --------------------------------
        INTENT DEFINITIONS

        1) new_goal
        The user expresses a desire, plan, intention, or wish about something they want to do in the future.
        This includes personal, social, romantic, professional, or learning goals, and can be short-term or long-term.

        Examples:
        - "I want to learn system design"
        - "I plan to start studying Rust"
        - "I want to build a multi-agent AI app"

        Return: new_goal

        2) new_memory
        The user shares something that already happened, an update about progress, or information they want remembered about themselves.
        Usually past or completed actions, status updates, or personal facts.
        IMPORTANT: If the user is saying they finished or completed something that was previously a GOAL, use complete_goal instead — NOT new_memory.

        Examples:
        - "I got 8 hours of sleep last night"
        - "I moved my project to production"
        - "I read 20 pages today"

        Return: new_memory

        3) complete_goal
        The user says they finished or completed a goal they previously set.
        This automatically saves it to memory AND removes it from their goals list — so use this whenever the user is marking a goal as done.
        Key signals: "i did this goal", "done with this goal", "finished this goal", "mark as done", "complete this goal" — often followed by the goal text.

        Examples:
        - "i did this goal Create a portfolio entry..."
        - "okay i reviewed the documents and first successful run finish it"
        - "I finished that goal"
        - "mark that goal as done"
        - "done with this goal: learn system design"

        Return: complete_goal

        4) get_priorities
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
        - Future-intention phrasing like "I want to...", "I plan to...", "I intend to...", or "I would like to..."
          should usually be classified as: new_goal (unless it clearly describes a past event).
        - If unsure, default to: chat.
        - NEVER output anything except one of the four intent words.
        - No sentences, no punctuation, no extra tokens.

        Return ONLY:
        new_goal OR new_memory OR complete_goal OR get_priorities OR chat
        """)
    human_msg = HumanMessage(content=user_message)

    print(f"\n[Intent Agent] Message received: '{user_message}'")
    intent = llm.invoke([system_msg, human_msg]).content.strip().lower()
    print(f"[Intent Agent] Raw LLM output: '{intent}'")

    # Safety fallback — if model returns something unexpected
    valid_intents = {"new_goal", "new_memory", "complete_goal", "get_priorities", "chat"}
    if intent not in valid_intents:
        print(f"[Intent Agent] Unknown intent '{intent}' — falling back to 'chat'")
        intent = "chat"

    print(f"[Intent Agent] Final intent: '{intent}'")
    return {"intent": intent}
