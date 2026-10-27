import streamlit as st
from supabase import create_client, Client

supabase_url = st.secrets["SUPABASE_URL"]
supabase_key = st.secrets["SUPABASE_SECRET_KEY"]

supabase: Client = create_client(supabase_url, supabase_key)