import streamlit as st
from src.ui.base_layout import style_base_layout, style_background_dashboard
from src.components.header import header_dashboard
from src.components.footer import footer_dashboard

def show_teacher_page():
    style_base_layout()
    style_background_dashboard()

    if 'teacher_login_type' not in st.session_state or st.session_state.teacher_login_type == "login":
        teacher_login()
    elif st.session_state.teacher_login_type == "register":
        teacher_register()

    footer_dashboard()
    
def teacher_login():
    c1, c2 = st.columns(2, vertical_alignment="center", gap="xlarge")
    with c1:
        header_dashboard()

    with c2:
        if st.button("Go back to Home", key="loginbackbtn", type="secondary", shortcut="control+backspace"):
            st.session_state['login_type'] = None
            st.rerun()

    st.header("Login using password", text_alignment="center")

    st.space()
    st.space()
    teacher_username = st.text_input("Enter Username", placeholder="anayroy", key="teacher_username")
    teacher_password = st.text_input("Enter Password", placeholder="Enter your password", type="password", key="teacher_password")

    st.divider()

    btn1, btn2 = st.columns(2)

    with btn1:
        if st.button("Login", icon=":material/passkey:", shortcut="ctrl+enter", width="stretch"):
            st.session_state['login_type'] = 'teacher'
            st.rerun()

    with btn2:
        if st.button("Register Instead", type="primary", icon=":material/passkey:", width="stretch"):
            st.session_state.teacher_login_type = "register"
            st.rerun()

def teacher_register():
    c1, c2 = st.columns(2, vertical_alignment="center", gap="xlarge")
    with c1:
        header_dashboard()

    with c2:
        if st.button("Go back to Home", key="loginbackbtn", type="secondary", shortcut="ctrl+backspace"):
            st.session_state['login_type'] = None
            st.rerun()

    st.header("Register your teacher profile")

    st.space()
    st.space()
    teacher_username = st.text_input("Enter Username", placeholder="anayroy")
    teacher_name = st.text_input("Enter Name", placeholder="Anay Roy")
    teacher_password = st.text_input("Enter Password", placeholder="Enter your password", type="password")
    teacher_confirm_password = st.text_input("Confirm Password", placeholder="Enter your password again", type="password")

    st.divider()

    btn1, btn2 = st.columns(2)

    with btn1:
        if st.button("Register Now", icon=":material/passkey:", shortcut="ctrl+enter", width="stretch"):
            st.session_state['login_type'] = 'teacher'
            st.rerun()

    with btn2:
        if st.button("Login Instead", type="primary", icon=":material/passkey:", width="stretch"):
            st.session_state.teacher_login_type = "login"
            st.rerun()