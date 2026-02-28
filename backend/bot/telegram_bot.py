import asyncio
from telegram import Bot, Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from core.config import settings

# One bot instance reused across all sends
bot = Bot(token=settings.telegram_bot_token)

# Telegram Application for receiving messages
application = Application.builder().token(settings.telegram_bot_token).build()


def format_morning_message(user_id: str, priorities: list[str], memory_context: str) -> str:
    memory_context_text = memory_context.strip().split(".", 1)[0] + "."
    priorities_text = "\n".join(priorities)
    message = (
        f"Good morning, {user_id} ❤️\n\n"
        f"Here are your priorities for today:\n"
        f"{priorities_text}\n\n"
        f"Lets get things done!"
    )
    return message
    
   


async def send_morning_briefing(user_id: str, priorities: list[str], memory_context: str):
    message = format_morning_message(user_id, priorities, memory_context)
    await bot.send_message(
        chat_id=settings.telegram_chat_id,
        text=message
    )


def push_morning_briefing(user_id: str, priorities: list[str], memory_context: str):
    """Sync wrapper — called by APScheduler which isn't async"""
    asyncio.run(send_morning_briefing(user_id, priorities, memory_context))


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Receives any message from the user and runs the chat graph"""
    from graph.chat_graph import chat_graph
    from memory.memory_store import get_goals

    user_message = update.message.text
    user_id = "meshari"
    print(f"\n{'='*40}")
    print(f"[Telegram] New message from {user_id}: '{user_message}'")

    initial_state = {
        "messages": [],
        "user_id": user_id,
        "run_type": "user_query",
        "goals": get_goals(user_id),
        "priorities": [],
        "tasks": [],
        "errors": [],
        "memory_context": "",
        "final_response": "",
        "user_message": user_message,
        "intent": "",
    }

    result = chat_graph.invoke(initial_state)

    print(f"[Telegram] Sending response: '{result['final_response'][:60]}...'")
    print(f"{'='*40}\n")
    await update.message.reply_text(result["final_response"])


# Register the message handler
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
