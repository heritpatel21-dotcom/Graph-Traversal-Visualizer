import hashlib
import hmac
import html
import re
from typing import Tuple, Optional
import streamlit as st

MAX_GRAPH_NODES = 50
MAX_EDGE_WEIGHT = 1000000.0
MIN_EDGE_WEIGHT = -1000000.0
MAX_IDENTIFIER_LENGTH = 30

CREDENTIAL_SALT = b"graph_traversal_secure_salt_v1"
DEFAULT_ACCOUNTS = {
    "admin": hashlib.sha256(b"GraphAdmin@2026" + CREDENTIAL_SALT).hexdigest(),
    "student": hashlib.sha256(b"LearnDSA@2026" + CREDENTIAL_SALT).hexdigest(),
    "demo": hashlib.sha256(b"demo123" + CREDENTIAL_SALT).hexdigest(),
}


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8") + CREDENTIAL_SALT).hexdigest()


def verify_credentials(username: str, password: str) -> bool:
    user = str(username).strip().lower()
    if user not in DEFAULT_ACCOUNTS:
        return False
    expected_hash = DEFAULT_ACCOUNTS[user]
    given_hash = hash_password(password)
    return hmac.compare_digest(expected_hash, given_hash)


def sanitize_identifier(raw_input: Optional[str], max_length: int = MAX_IDENTIFIER_LENGTH) -> str:
    if raw_input is None:
        return ""
    cleaned = str(raw_input).strip()
    cleaned = re.sub(r"[\x00-\x1f\x7f-\x9f]", "", cleaned)
    escaped = html.escape(cleaned, quote=True)
    return escaped[:max_length]


def is_authenticated() -> bool:
    return bool(st.session_state.get("is_authenticated", False))


def login_user(username: str) -> None:
    st.session_state["is_authenticated"] = True
    st.session_state["auth_user"] = str(username).strip()


def logout_user() -> None:
    st.session_state["is_authenticated"] = False
    st.session_state["auth_user"] = None


def render_security_gate() -> bool:
    if is_authenticated():
        return True

    st.markdown(
        """
        <div style="max-width:440px; margin:40px auto 20px auto; background:#1E293B; border-radius:12px; border:1px solid #334155; padding:28px; box-shadow:0 10px 25px -5px rgba(0,0,0,0.5); text-align:center;">
            <div style="background:linear-gradient(135deg, #6366F1, #8B5CF6); width:52px; height:52px; border-radius:12px; display:inline-flex; align-items:center; justify-content:center; font-size:26px; box-shadow:0 0 16px rgba(99,102,241,0.5); margin-bottom:14px;">
                🔒
            </div>
            <div style="font-size:22px; font-weight:800; color:#F8FAFC; letter-spacing:-0.02em;">Security Authentication</div>
            <div style="font-size:13px; color:#94A3B8; margin-top:4px;">Please authenticate to access Graph Traversal Visualizer</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    col_wrap1, col_center, col_wrap2 = st.columns([1, 1.8, 1])
    with col_center:
        with st.form("security_login_form"):
            user_input = st.text_input("Username", value="admin", key="sec_user_in")
            pass_input = st.text_input("Password", type="password", value="GraphAdmin@2026", key="sec_pass_in")
            submitted = st.form_submit_button("Sign In Securely", type="primary", use_container_width=True)

            if submitted:
                if verify_credentials(user_input, pass_input):
                    login_user(user_input)
                    st.success(f"Welcome back, {user_input}!")
                    st.rerun()
                else:
                    st.error("Invalid credentials. Please verify your username and password.")

        col_demo1, col_demo2 = st.columns(2)
        with col_demo1:
            if st.button("🚀 Quick Demo Login", use_container_width=True):
                login_user("admin")
                st.rerun()
        with col_demo2:
            st.caption("Default: `admin` / `GraphAdmin@2026`")

    return False
