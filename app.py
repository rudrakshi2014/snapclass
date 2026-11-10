import streamlit as st
from src.screens.student import show_student_page
from src.screens.teacher import show_teacher_page
from src.screens.home import show_home_page
from src.components.dialog_auto_enroll import auto_enroll_dialog

from flask import Flask

# Vercel looks specifically for "app" or "application"
app = Flask(__name__)

@app.route("/")
def home():
    return "Hello from Vercel!"

def main():
    st.set_page_config(
        page_title="Attendifly - Making Attendance smarter and faster using AI",
        page_icon="https://i.ibb.co/YTYGn5qV/logo.png"
    )
    if 'login_type' not in st.session_state:
        st.session_state['login_type'] = None

    match st.session_state['login_type']:
        case 'teacher':
            show_teacher_page()
        case 'student':
            show_student_page()
        case None:
            show_home_page()

    join_code = st.query_params.get("join-code")
    if join_code:
        if st.session_state.login_type != 'student':
            st.session_state.login_type = 'student'
            st.rerun()

        if st.session_state.get('is_logged_in') and st.session_state.get('user_role') == 'student':
            auto_enroll_dialog(join_code)

main()