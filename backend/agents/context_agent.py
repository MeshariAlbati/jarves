from langchain_anthropic import ChatAnthropic
from langchain_core.messages import SystemMessage, HumanMessage
from core.state import JarvesState
from core.config import settings

# Initialize Claude — one instance, reused on every call
llm = ChatAnthropic(
    model="claude-sonnet-4-6",
    api_key=settings.anthropic_api_key
)


def context_agent(state: JarvesState) -> dict:
    user_id = state["user_id"]
    run_type = state["run_type"]

    # NOTE: Mocked memories for now — Supabase connection comes later
    # These simulate what would be retrieved from the memory store
    raw_memories = [
        "User's main goal: become a backend AI engineer",
        "User is building Jarves — a personal ops system using LangGraph",
        "User mentioned feeling overwhelmed with too many tasks last week",
        "User prefers concise, direct communication",
        "User wants to ship the first version of Jarves by end of March",
    ]

   
    system_msg = SystemMessage(
    content="""
    You are a memory synthesis module.

    Your task is to transform raw memory entries into ONE concise, coherent context string representing the user's current state, goals, and relevant facts.

    Rules you MUST follow:
    - Combine related memories and remove duplicates.
    - Keep only information relevant to current goals, priorities, or ongoing work.
    - Prefer recent and frequently referenced memories.
    - Do NOT invent new information.
    - Do NOT explain your reasoning.
    - Do NOT add commentary or formatting.

    Output Requirements you MUST follow:
    - Return exactly ONE paragraph.
    - Use clear, neutral language.
    - Maximum length: 120 words.
    - Output ONLY the synthesized context string.
    """
)
    human_msg = HumanMessage(content=f"Run type: {run_type}\nRaw memories: {raw_memories}")
    context = llm.invoke([system_msg, human_msg]).content

    return {"memory_context": context}
