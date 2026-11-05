import streamlit as st
import time
from src.database.db import enroll_student_to_subject
from src.database.config import supabase

@st.dialog("QUick Enrollment")
def auto_enroll_dialog(subject_code):
    student_id = st.session_state.student_data['student_id']
    res = supabase.table('subjects').select('subject_id, name, subject_code').eq('subject_code', subject_code).execute()
    
    if not res.data:
        st.error("Subject code not found!")
        if st.button("Close"):
            st.query_params.clear()
            st.rerun()
        return
    
    subject = res.data[0]
    check = supabase.table('subject_students').select('*').eq('subject_id', subject['subject_id']).eq('student_id', student_id).execute()
    if check.data:
        st.info('You are already enrolled in this subject!')
        if st.button("Got it!"):
            st.query_params.clear()
            st.rerun()
        return

    st.markdown('Would you like to enroll in the subject **{}**?'.format(subject['name']))
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("No thanks!"):
            st.query_params.clear()
            st.rerun()

    with col2:
        if st.button("Yes Enroll Now", type='primary', width='stretch'):
            enroll_student_to_subject(student_id, subject['subject_id'])
            st.success(f'Successfully enrolled in {subject["name"]}!')
            time.sleep(2)
            st.query_params.clear()
            st.rerun()