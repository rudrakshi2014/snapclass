import streamlit as st
from src.ui.base_layout import style_base_layout, style_background_dashboard
from src.components.header import header_dashboard
from src.components.footer import footer_dashboard
from src.database.db import check_teacher_exists, create_teacher, teacher_login, get_teacher_subjects
from src.components.dialog_create_subject import create_subject_dialog
from src.components.subject_card import subject_card
from src.components.dialog_share_subject import share_subject_dialog

def show_teacher_page():
    style_base_layout()
    style_background_dashboard()

    if "teacher_data" in st.session_state:
        teacher_dashboard()
    elif 'teacher_login_type' not in st.session_state or st.session_state.teacher_login_type == "login":
        teacher_screen_login()
    elif st.session_state.teacher_login_type == "register":
        teacher_register()

    footer_dashboard()

def teacher_dashboard():
    teacher_data = st.session_state.teacher_data
    c1, c2 = st.columns(2, vertical_alignment="center", gap="xlarge")
    with c1:
        header_dashboard()
    with c2:
        st.subheader(f"""Welcome, {teacher_data['name']} !""")
        if st.button("Logout", key="logoutbtn", type="secondary", shortcut="control+backspace"):
            st.session_state['is_logged_in'] = False
            del st.session_state.teacher_data
            st.rerun()

    st.space()

    if "current_teacher_tab" not in st.session_state:
        st.session_state.current_teacher_tab = 'take_attendance'

    tab1, tab2, tab3 = st.columns(3)
    with tab1:
        type1 = 'primary' if st.session_state.current_teacher_tab == 'take_attendance' else 'tertiary'
        if st.button('Take Attendance', type=type1, width='stretch', icon=':material/ar_on_you:'):
            st.session_state.current_teacher_tab = 'take_attendance'
            st.rerun()

    with tab2:
        type2 = 'primary' if st.session_state.current_teacher_tab == 'manage_subjects' else 'tertiary'
        if st.button('Manage Subjects', type=type2, width='stretch', icon=':material/book_ribbon:'):
            st.session_state.current_teacher_tab = 'manage_subjects'
            st.rerun()

    with tab3:
        type3 = 'primary' if st.session_state.current_teacher_tab == 'attendance_records' else 'tertiary'
        if st.button('Attendance records', type=type3, width='stretch', icon=':material/cards_stack:'):
            st.session_state.current_teacher_tab = 'attendance_records'
            st.rerun()
    st.divider()

    if st.session_state.current_teacher_tab == "take_attendance":
        teacher_tab_take_attendance()

    if st.session_state.current_teacher_tab == "manage_subjects":
        teacher_tab_manage_subjects()

    if st.session_state.current_teacher_tab == "attendance_records":
        teacher_tab_attendance_records()

def teacher_tab_take_attendance():
    st.header("Take AI Attendance")

def teacher_tab_manage_subjects():
    teacher_id = st.session_state.teacher_data['teacher_id']
    col1, col2 = st.columns(2)
    with col1:
        st.header("Manage Subjects", width='stretch')
    with col2:
        if st.button('Create New Subject', width='stretch'):
            create_subject_dialog(teacher_id)

    # LIST ALL SUBJECTS
    subjects = get_teacher_subjects(teacher_id)
    if subjects:
        for sub in subjects:
            stats = [
                ("👥", "Students", sub['total_students']),
                ("🕰", "Classes", sub['total_classes'])
            ]
            def share_btn():
                if st.button(f"Share Code: {sub['name']}", key=f"share_{sub['subject_code']}", icon=":material/share:"):
                    share_subject_dialog(sub['name'], sub['subject_code'])

                st.space()

            subject_card(
                name=sub['name'],
                code=sub['subject_code'],
                section=sub['section'],
                stats=stats,
                footer_callback=share_btn
            )
    else:
        st.info("NO SUBJECTS FOUND. CREATE ONE ABOVE!")

def teacher_tab_attendance_records():
    st.header("Attendance Records")

def login_teacher(username: str, password: str) -> bool:
    if not username or not password:
        st.error("Please enter both username and password.")
        return False
    
    teacher = teacher_login(username, password)
    if teacher:
        st.session_state.user_role = 'teacher'
        st.session_state.teacher_data = teacher
        st.session_state.is_logged_in = True
        return True
    return False
    
def teacher_screen_login():
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
            if login_teacher(teacher_username, teacher_password):
                st.toast("Welcome back!", icon="🎉")
                import time
                time.sleep(1)
                st.rerun()
            else:
                st.error("Invalid username or password. Please try again.")

    with btn2:
        if st.button("Register Instead", type="primary", icon=":material/passkey:", width="stretch"):
            st.session_state.teacher_login_type = "register"
            st.rerun()

def register_teacher(username: str, name: str, password: str, confirm_password: str) -> tuple[bool, str]:
    if not username or not name or not password or not confirm_password:
        return False, "All fields are required."

    if password != confirm_password:
        return False, "Passwords do not match."

    if check_teacher_exists(username):
        return False, "Username already exists."

    try:
        if create_teacher(username, password, name):
            return True, "Teacher registered successfully! You can now log in."
        return False, "Could not create teacher. Please try again."
    except Exception as e:
        return False, f"Error creating teacher: {str(e)}"

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
    username = st.text_input("Enter Username", placeholder="anayroy", key="teacher_register_username")
    name = st.text_input("Enter Name", placeholder="Anay Roy", key="teacher_register_name")
    password = st.text_input(
        "Enter Password",
        placeholder="Enter your password",
        type="password",
        key="teacher_register_password",
    )
    confirm_password = st.text_input(
        "Confirm Password",
        placeholder="Enter your password again",
        type="password",
        key="teacher_register_confirm_password",
    )

    st.divider()

    btn1, btn2 = st.columns(2)

    with btn1:
        if st.button("Register Now", icon=":material/passkey:", shortcut="ctrl+enter", width="stretch"):
            success, message = register_teacher(
                username=username,
                name=name,
                password=password,
                confirm_password=confirm_password,
            )
            if success:
                st.success(message)
                import time
                time.sleep(2)
                st.session_state.teacher_login_type = "login"
                st.rerun()
            else:
                st.error(message)
    with btn2:
        if st.button("Login Instead", type="primary", icon=":material/passkey:", width="stretch"):
            st.session_state.teacher_login_type = "login"
            st.rerun()