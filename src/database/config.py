import os

import streamlit as st
from supabase import create_client, Client


def get_setting(name: str) -> str:
    value = os.environ.get(name)
    if value:
        return value
    return st.secrets[name]


supabase_url = get_setting("SUPABASE_URL")
supabase_key = get_setting("SUPABASE_SECRET_KEY")

supabase: Client = create_client(supabase_url, supabase_key)