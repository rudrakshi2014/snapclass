import streamlit as st

def main():
    st.header("Welcome to My Streamlit App")
    name = st.text_input("Enter your name:", key="name")


    col1, col2 = st.columns(2)
    with col1:
        if st.button("Hello!", type="primary", key="btn1", width="stretch"):
            st.write(f"Hello, {name}!")
    
    with col2:
        if st.button("Bye!", type="secondary", key="btn2", width="stretch"):
            st.write(f"Goodbye, {name}!")

    st.markdown("""
        <div style="margin-top: 20px;">
            <img src="https://i.ibb.co/YTYGn5qV/logo.png">
            <h1 style="text-align: center;">My Streamlit App</h1>
        </div>
    """, unsafe_allow_html=True)

main()