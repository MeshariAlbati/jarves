import sys
sys.path.insert(0, ".")

from dotenv import load_dotenv
load_dotenv()

from memory.memory_store import supabase

OLD_ID = "meshari"

print(f"Deleting all data for user: '{OLD_ID}'")
supabase.table("goals").delete().eq("user_id", OLD_ID).execute()
supabase.table("memories").delete().eq("user_id", OLD_ID).execute()
supabase.table("users").delete().eq("id", OLD_ID).execute()
print("Done — you can now start fresh.")
