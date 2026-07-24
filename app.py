"""
NurAuto - AI YouTube Video Studio
Asosiy fayl
"""
import streamlit as st
from datetime import datetime

# Sahifa sozlamalari
st.set_page_config(
    page_title="NurAuto - AI Video Studio",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS - Purple + Qora dizayn
st.markdown("""
<style>
    .main {
        background: linear-gradient(180deg, #0F0F1E 0%, #1A1A2E 100%);
    }
    h1, h2, h3 {
        color: #FFFFFF !important;
        font-weight: 700;
    }
    .stButton>button {
        background: linear-gradient(135deg, #8B5CF6 0%, #6D28D9 100%);
        color: white;
        border: none;
        padding: 12px 30px;
        border-radius: 10px;
        font-weight: bold;
        font-size: 16px;
        transition: all 0.3s;
        width: 100%;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(139, 92, 246, 0.5);
    }
    section[data-testid="stSidebar"] {
        background: #0A0A15;
    }
    .metric-card {
        background: linear-gradient(135deg, #1A1A2E 0%, #2D1B47 100%);
        padding: 25px;
        border-radius: 15px;
        border: 1px solid #8B5CF6;
        text-align: center;
        margin-bottom: 20px;
    }
    .logo-text {
        font-size: 48px;
        font-weight: 900;
        background: linear-gradient(135deg, #8B5CF6 0%, #EC4899 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        margin: 20px 0;
    }
    .login-container {
        max-width: 500px;
        margin: 50px auto;
        padding: 40px;
        background: linear-gradient(135deg, #1A1A2E 0%, #2D1B47 100%);
        border-radius: 20px;
        border: 1px solid #8B5CF6;
        text-align: center;
    }
    .stTextInput>div>div>input {
        background-color: #1A1A2E;
        color: white;
        border: 1px solid #8B5CF6;
        border-radius: 10px;
        padding: 10px;
    }
    .success-box {
        background: linear-gradient(135deg, #059669 0%, #10B981 100%);
        padding: 15px;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)


# Session State
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_email' not in st.session_state:
    st.session_state.user_email = None
if 'user_name' not in st.session_state:
    st.session_state.user_name = None


# LOGIN SAHIFA
def show_login():
    st.markdown("""
    <div class='logo-text'>🎬 NurAuto</div>
    <h3 style='text-align: center; color: #A78BFA;'>
        AI YouTube Video Studio
    </h3>
    <p style='text-align: center; color: #CBD5E1; margin-bottom: 40px;'>
        Sun'iy intellekt yordamida YouTube uchun<br>
        professional videolarni avtomatik yarating!
    </p>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("### 🔐 Tizimga kirish")
        
        email = st.text_input(
            "📧 Email",
            placeholder="sizning@gmail.com"
        )
        
        password = st.text_input(
            "🔒 Parol",
            type="password",
            placeholder="••••••••"
        )
        
        col_a, col_b = st.columns(2)
        
        with col_a:
            if st.button("🚀 Kirish"):
                if email and password:
                    st.session_state.logged_in = True
                    st.session_state.user_email = email
                    st.session_state.user_name = email.split('@')[0]
                    st.success("✅ Muvaffaqiyatli!")
                    st.rerun()
                else:
                    st.error("❌ Email va parol kiriting!")
        
        with col_b:
            if st.button("📝 Ro'yxatdan o'tish"):
                st.info("Tez kunda!")
        
        st.markdown("---")
        st.markdown("### ✨ Xususiyatlar:")
        st.markdown("""
        - 🔍 **Kanal Tahlili** - AI orqali
        - 🎬 **Smart Video** - Avtomatik yaratish
        - 🎙️ **AI Ovoz** - Turli tillarda
        - 📤 **YouTube Upload** - Bir tugma bilan
        - 📊 **Statistika** - To'liq analitika
        """)


# DASHBOARD
def show_dashboard():
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown("""
        <div class='logo-text' style='font-size: 32px; text-align: left;'>
            🎬 NurAuto
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style='text-align: right; padding-top: 20px;'>
            👤 {st.session_state.user_name}<br>
            <small style='color: #8B5CF6;'>{st.session_state.user_email}</small>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown(f"## Xush kelibsiz, {st.session_state.user_name}! 👋")
    st.markdown("### Bugun qanday video yaratamiz?")
    
    st.markdown("### 📊 Sizning statistikangiz")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class='metric-card'>
            <h1 style='color: #8B5CF6; margin: 0;'>0</h1>
            <p style='color: #CBD5E1;'>📹 Videolar</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='metric-card'>
            <h1 style='color: #EC4899; margin: 0;'>0</h1>
            <p style='color: #CBD5E1;'>📅 Bugun</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class='metric-card'>
            <h1 style='color: #F59E0B; margin: 0;'>0</h1>
            <p style='color: #CBD5E1;'>👁️ Ko'rishlar</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class='metric-card'>
            <h1 style='color: #10B981; margin: 0;'>0</h1>
            <p style='color: #CBD5E1;'>💰 Daromad</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("### 🚀 Tez harakatlar")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class='metric-card' style='padding: 40px;'>
            <h2>🔍</h2>
            <h3>Kanalni Tahlil Qil</h3>
            <p style='color: #CBD5E1;'>
                YouTube kanalingizni AI orqali tahlil qiling
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔍 Kanalni Tahlil Qilish"):
            st.info("⚡ Tez kunda qo'shiladi!")
    
    with col2:
        st.markdown("""
        <div class='metric-card' style='padding: 40px;'>
            <h2>🎬</h2>
            <h3>Yangi Video Yaratish</h3>
            <p style='color: #CBD5E1;'>
                AI yordamida professional video yarating
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🎬 Video Yaratish"):
            st.info("⚡ Tez kunda qo'shiladi!")
    
    st.markdown("---")
    
    st.markdown("### 📹 So'nggi videolar")
    st.info("Hali video yaratilmagan. Birinchi videoingizni yarating! 🚀")
    
    # Sidebar
    with st.sidebar:
        st.markdown("""
        <div class='logo-text' style='font-size: 28px;'>
            🎬 NurAuto
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        st.markdown(f"👤 **{st.session_state.user_name}**")
        st.markdown(f"📧 {st.session_state.user_email}")
        
        st.markdown("---")
        
        st.markdown("### 📊 Statistika")
        st.markdown("- Videolar: **0**")
        st.markdown("- Bugun: **0**")
        st.markdown("- Kvota: **500/500**")
        
        st.markdown("---")
        
        if st.button("🚪 Chiqish"):
            st.session_state.logged_in = False
            st.session_state.user_email = None
            st.session_state.user_name = None
            st.rerun()


# ASOSIY
def main():
    if st.session_state.logged_in:
        show_dashboard()
    else:
        show_login()


if __name__ == "__main__":
    main()
