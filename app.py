import streamlit as st
from src.screens.student import show_student_page
from src.screens.teacher import show_teacher_page
from src.screens.home import show_home_page

def main():

    if 'login_type' not in st.session_state:
        st.session_state['login_type'] = None

    match st.session_state['login_type']:
        case 'teacher':
            show_teacher_page()
        case 'student':
            show_student_page()
        case None:
            show_home_page()

main()