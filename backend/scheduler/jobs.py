from apscheduler.schedulers.background import BackgroundScheduler
from dotenv import load_dotenv
load_dotenv()

from graph.pos_graph import jarves_graph
from bot.telegram_bot import push_morning_briefing
from memory.memory_store import get_goals

scheduler = BackgroundScheduler()


def run_morning_briefing():
    user_id = "meshari"
    goals = get_goals(user_id)
    initial_state = {
    "messages": [],
    "user_id": user_id,
    "run_type": "morning_briefing",
    "goals": goals,
    "priorities": [],
    "tasks": [],
    "errors": [],
    "memory_context": "",
    "final_response": "",
}

    result = jarves_graph.invoke(initial_state)
    push_morning_briefing(
        user_id=initial_state["user_id"],
        priorities=result["priorities"],
        memory_context=result["memory_context"]
    )

def start_scheduler():
    # Morning briefing — every day at 8am
    scheduler.add_job(run_morning_briefing, 'cron', hour=8, minute=0)

    scheduler.start()
    print("Scheduler started — Jarves will run every morning at 8am")
