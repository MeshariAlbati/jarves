from langchain_anthropic import ChatAnthropic
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
from core.state import JarvesState
from core.config import settings

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=settings.groq_api_key
)


def priority_agent(state: JarvesState) -> dict:
    memory_context = state["memory_context"]
    goals = state["goals"]

    
    system_msg = SystemMessage(
    content="""
    You are a priority-planning assistant that identifies the user's most important priorities based on their memory context and goals.

    Your task is to determine the highest-value actionable priorities for the user right now, based ONLY on their saved goals.

    Rules you MUST follow:
    - ONLY return goals that are explicitly saved in the user's memory/context.
    - Do NOT invent, guess, or generate any goals that are not already saved.
    - If the user has 0 saved goals, respond ONLY with: "You have no saved goals yet."
    - If the user has 1 saved goal, return only that 1 goal.
    - If the user has 2 saved goals, return only those 2 goals.
    - If the user has 3 or more saved goals, return the top 3 ranked by urgency and impact.
    - Each item must be a clear, concrete, actionable task.
    - Each item must be one sentence only.
    - Do NOT include explanations, reasoning, introductions, or conclusions.
    - Do NOT include any text before or after the list.
    - Do NOT use bullet points, markdown, or extra formatting.
    - Prefer tasks that are time-sensitive, previously avoided.

    Output format (STRICT):
    - For 0 goals: "You have no saved goals yet."
    - For 1 goal:
    1. First priority task
    - For 2 goals:
    1. First priority task
    2. Second priority task
    - For 3+ goals:
    1. First priority task
    2. Second priority task
    3. Third priority task
    """
)
    human_msg = HumanMessage(content=f"Memory context: {memory_context}\nGoals: {goals}")

    response = llm.invoke([system_msg, human_msg]).content

    # Parse the numbered list into a Python list
    priorities = [
        line.strip()
        for line in response.strip().split("\n")
        if line.strip()
    ]

    return {"priorities": priorities}
