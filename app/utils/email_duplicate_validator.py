from app.core.config import supabase


def email_duplicate_validator(email: str):

    existing_account = (
        supabase.table("accounts-test").select("id").eq("email", email).execute()
    )

    return existing_account
