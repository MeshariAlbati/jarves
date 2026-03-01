from apscheduler.schedulers.background import BackgroundScheduler
from dotenv import load_dotenv
load_dotenv()

from graph.pos_graph import jarves_graph
from bot.telegram_bot import push_morning_briefing
from memory.memory_store import get_goals, save_memory
from datetime import date

scheduler = BackgroundScheduler()


def run_morning_briefing():
    from memory.memory_store import get_user_name
    user_id = "meshari"
    name = get_user_name(user_id) or user_id
    goals = get_goals(user_id)
    initial_state = {
        "messages": [],
        "user_id": user_id,
        "user_name": name,
        "run_type": "morning_briefing",
        "goals": goals,
        "priorities": [],
        "tasks": [],
        "errors": [],
        "memory_context": "",
        "final_response": "",
        "user_message": "",
        "intent": "",
    }

    result = jarves_graph.invoke(initial_state)
    push_morning_briefing(
        user_id=user_id,
        name=name,
        priorities=result["priorities"],
        memory_context=result["memory_context"]
    )
    save_memory(user_id, result["memory_context"])

def start_scheduler():
    # Morning briefing — every day at 8am
    scheduler.add_job(run_morning_briefing, 'cron', hour=8, minute=0)

    scheduler.start()
    print("Scheduler started — Jarves will run every morning at 8am")
