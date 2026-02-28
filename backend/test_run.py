import sys
sys.path.insert(0, ".")

from dotenv import load_dotenv
load_dotenv()  # must be before ANY langchain imports

from graph.pos_graph import jarves_graph

# Simulate a morning briefing run
initial_state = {
    "messages": [],
    "user_id": "meshari",
    "run_type": "morning_briefing",
    "goals": [
        "Become a backend AI engineer",
        "Ship Jarves by end of March",
        "Build a strong portfolio",
    ],
    "priorities": [],
    "tasks": [],
    "errors": [],
    "memory_context": "",
    "final_response": "",
}

print("Running Jarves graph...\n")
result = jarves_graph.invoke(initial_state)

print("=== MEMORY CONTEXT ===")
print(result["memory_context"])

print("\n=== TODAY'S PRIORITIES ===")
for p in result["priorities"]:
    print(p)

# Send to Telegram
from bot.telegram_bot import push_morning_briefing
print("\nSending to Telegram...")
push_morning_briefing(
    user_id=initial_state["user_id"],
    priorities=result["priorities"],
    memory_context=result["memory_context"]
)
print("Sent!")
