import streamlit as st
import time
from src.database.db import enroll_student_to_subject
from src.database.config import supabase
from PIL import Image

@st.dialog("Capture or Upload Photos")
def add_photos_dialog():
    st.write("Add classroom photos to scan for attendance")

    if 'photo_tab' not in st.session_state:
        st.session_state.photo_tab = 'camera'

    tab1, tab2 = st.columns(2)

    with tab1:
        type_camera = 'primary' if st.session_state.photo_tab == 'camera' else 'tertiary'
        if st.button('Camera', type=type_camera, width='stretch'):
            st.session_state.photo_tab = 'camera'

    with tab2:
        type_upload = 'primary' if st.session_state.photo_tab == 'upload' else 'tertiary'
        if st.button('Upload Photos', type=type_upload, width='stretch'):
            st.session_state.photo_tab = 'upload'

    if st.session_state.photo_tab == 'camera':
        cam_photo = st.camera_input("Take Snapshot", key="dialog_cam")
        if cam_photo:
            st.session_state.attendance_images.append(Image.open(cam_photo))
            st.toast("Photo captured!")
            st.rerun()

    if st.session_state.photo_tab == 'upload':
        uploaded_files = st.file_uploader("choose image files", type=["png", "jpg", "jpeg"], accept_multiple_files=True, key="dialog_upload")
        if uploaded_files:
            for photo in uploaded_files:
                st.session_state.attendance_images.append(Image.open(photo))
            st.toast(f"{len(uploaded_files)} photo(s) uploaded successfully!")
            st.rerun()

    st.divider()
    if st.button("Done", type='primary', width='stretch'):
        st.rerun()