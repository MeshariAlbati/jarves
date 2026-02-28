from langgraph.graph import StateGraph, START, END
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
from core.state import JarvesState
from core.config import settings
from agents.intent_agent import intent_agent
from agents.context_agent import context_agent
from agents.priority_agent import priority_agent
from memory.memory_store import save_memory, save_goal

llm = ChatGroq(model="llama-3.3-70b-versatile", api_key=settings.groq_api_key)


#Action Nodes 

def handle_new_goal(state: JarvesState) -> dict:
    print(f"[handle_new_goal] Saving goal: '{state['user_message']}'")
    save_goal(state["user_id"], state["user_message"])
    return {"final_response": f"Got it! I've added that as a new goal 🎯\n\"{state['user_message']}\""}


def handle_new_memory(state: JarvesState) -> dict:
    print(f"[handle_new_memory] Saving memory: '{state['user_message']}'")
    save_memory(state["user_id"], state["user_message"])
    return {"final_response": f"Noted and remembered 💾\n\"{state['user_message']}\""}


def handle_get_priorities(state: JarvesState) -> dict:
    print(f"[handle_get_priorities] Formatting {len(state['priorities'])} priorities")
    priorities = state["priorities"]
    response = "Here are your priorities right now:\n\n" + "\n".join(priorities)
    return {"final_response": response}


def handle_chat(state: JarvesState) -> dict:
    print(f"[handle_chat] Responding to: '{state['user_message']}'")
    system_msg = SystemMessage(content="""
    You are Jarves, a personal AI ops system. You are concise, direct, and helpful.
    You know the user's goals and context. Keep responses short — max 3-4 sentences.
    """)
    human_msg = HumanMessage(content=state["user_message"])
    response = llm.invoke([system_msg, human_msg]).content
    return {"final_response": response}


# Conditional Router 

def route_by_intent(state: JarvesState) -> str:
    intent = state["intent"]
    print(f"[Router] Routing intent '{intent}' to handler")
    if intent == "new_goal":
        return "handle_new_goal"
    elif intent == "new_memory":
        return "handle_new_memory"
    elif intent == "get_priorities":
        return "context"
    else:
        return "handle_chat"


# Build the Graph 

graph_builder = StateGraph(JarvesState)

graph_builder.add_node("intent", intent_agent)
graph_builder.add_node("context", context_agent)
graph_builder.add_node("priority", priority_agent)
graph_builder.add_node("handle_new_goal", handle_new_goal)
graph_builder.add_node("handle_new_memory", handle_new_memory)
graph_builder.add_node("handle_get_priorities", handle_get_priorities)
graph_builder.add_node("handle_chat", handle_chat)

graph_builder.add_edge(START, "intent")

graph_builder.add_conditional_edges("intent", route_by_intent)

graph_builder.add_edge("context", "priority")
graph_builder.add_edge("priority", "handle_get_priorities")

graph_builder.add_edge("handle_new_goal", END)
graph_builder.add_edge("handle_new_memory", END)
graph_builder.add_edge("handle_get_priorities", END)
graph_builder.add_edge("handle_chat", END)

chat_graph = graph_builder.compile()
