import streamlit as st


# ------------------------------
# Demo Users
# ------------------------------

USERS = {
    "admin@techhire.com": "admin123",
    "hr@company.com": "hr123",
    "kaushal@gmail.com": "kaushal123"
}


# ------------------------------
# Login Screen
# ------------------------------

def login():

    st.markdown("""
    <div style="
    text-align:center;
    padding:20px;
    ">
    <h1>🤖 TechHire AI</h1>
    <h3>AI Resume Screening Platform</h3>
    </div>
    """, unsafe_allow_html=True)

    email = st.text_input("📧 Email")

    password = st.text_input(
        "🔒 Password",
        type="password"
    )

    login_button = st.button(
        "Login",
        use_container_width=True
    )

    if login_button:

        if email in USERS and USERS[email] == password:

            st.session_state["logged_in"] = True

            st.session_state["user"] = email

            st.success("Login Successful!")

            st.rerun()

        else:

            st.error("Invalid Email or Password")


# ------------------------------
# Logout
# ------------------------------

def logout():

    if st.sidebar.button("🚪 Logout"):

        st.session_state["logged_in"] = False

        st.rerun()