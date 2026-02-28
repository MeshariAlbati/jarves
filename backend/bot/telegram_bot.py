import asyncio
from telegram import Bot
from core.config import settings

# One bot instance reused across all sends
bot = Bot(token=settings.telegram_bot_token)


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
