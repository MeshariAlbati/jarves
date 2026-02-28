from supabase import create_client, Client
from core.config import settings

# One Supabase client reused across all calls
supabase: Client = create_client(settings.supabase_url, settings.supabase_key)


def get_user(user_id: str) -> dict:
    result = supabase.table("users").select("*").eq("id", user_id).single().execute()
    return result.data


def get_user_name(user_id: str) -> str | None:
    result = supabase.table("users").select("name").eq("id", user_id).execute()
    if result.data:
        return result.data[0].get("name")
    return None


def save_user_name(user_id: str, name: str) -> None:
    supabase.table("users").upsert({"id": user_id, "name": name}).execute()


def get_goals(user_id: str) -> list[str]:
    result = supabase.table("goals").select("goal").eq("user_id", user_id).execute()
    return [row["goal"] for row in result.data]


def get_memories(user_id: str, limit: int = 10) -> list[str]:
    response = (
        supabase
        .table("memories")
        .select("content")
        .eq("user_id", user_id)
        .order("created_at", desc=True)
        .limit(limit)
        .execute()
    )

    # response.data is a list of rows (dicts)
    memories = [row["content"] for row in response.data or []]
    return memories


def save_goal(user_id: str, goal: str) -> None:
    supabase.table("goals").insert({
        "user_id": user_id,
        "goal": goal
    }).execute()


def save_memory(user_id: str, content: str) -> None:
    supabase.table("memories").insert({
        "user_id": user_id,
        "content": content
    }).execute()


def delete_goal(user_id: str, goal: str) -> None:
    supabase.table("goals").delete().eq("user_id", user_id).eq("goal", goal).execute()
