from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
from core.state import JarvesState
from core.config import settings
from memory.memory_store import get_memories


llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    groq_api_key=settings.groq_api_key
)


def context_agent(state: JarvesState) -> dict:
    user_id = state["user_id"]
    run_type = state["run_type"]

    # Fetch real memories from Supabase
    raw_memories = get_memories(user_id)

    # First run fallback — no memories yet
    if not raw_memories:
        return {"memory_context": "No memories yet. This is the first run."}

   
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
