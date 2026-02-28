from langgraph.graph import StateGraph, START, END
from core.state import JarvesState
from agents.context_agent import context_agent
from agents.priority_agent import priority_agent



graph_builder = StateGraph(JarvesState)


graph_builder.add_node("context", context_agent)
graph_builder.add_node("priority", priority_agent)

graph_builder.add_edge(START, "context")
graph_builder.add_edge("context", "priority")
graph_builder.add_edge("priority", END)

jarves_graph = graph_builder.compile()
