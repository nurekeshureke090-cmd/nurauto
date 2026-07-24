"""
NurAuto - Sozlamalar sahifasi
YouTube kanal ulash va sozlamalar
"""

import streamlit as st

# Sahifa sozlamalari
st.set_page_config(
    page_title="Sozlamalar - NurAuto",
    page_icon="⚙️",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        background: linear-gradient(180deg, #0F0F1E 0%, #1A1A2E 100%);
    }
    h1, h2, h3 {
        color: #FFFFFF !important;
    }
    .stButton>button {
        background: linear-gradient(135deg, #8B5CF6 0%, #6D28D9 100%);
        color: white;
        border: none;
        padding: 12px 30px;
        border-radius: 10px;
        font-weight: bold;
        width: 100%;
    }
    .setting-card {
        background: linear-gradient(135deg, #1A1A2E 0%, #2D1B47 100%);
        padding: 25px;
        border-radius: 15px;
        border: 1px solid #8B5CF6;
        margin-bottom: 20px;
    }
    .success-msg {
        background: linear-gradient(135deg, #059669 0%, #10B981 100%);
        padding: 15px;
        border-radius: 10px;
        color: white;
        margin: 10px 0;
    }
    .info-msg {
        background: linear-gradient(135deg, #3B82F6 0%, #2563EB 100%);
        padding: 15px;
        border-radius: 10px;
        color: white;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)


# Login tekshirish
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.warning("⚠️ Avval tizimga kiring!")
    st.markdown("[🏠 Bosh sahifaga qaytish](/)")
    st.stop()


# Session state
if 'youtube_channel_url' not in st.session_state:
    st.session_state.youtube_channel_url = ""
if 'youtube_channel_name' not in st.session_state:
    st.session_state.youtube_channel_name = ""
if 'preferred_language' not in st.session_state:
    st.session_state.preferred_language = "O'zbek"
if 'default_niche' not in st.session_state:
    st.session_state.default_niche = "horror_en"


# Sahifa sarlavhasi
st.markdown("""
<div style='text-align: center; padding: 20px;'>
    <h1 style='background: linear-gradient(135deg, #8B5CF6 0%, #EC4899 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                font-size: 48px;
                margin: 0;'>
        ⚙️ Sozlamalar
    </h1>
    <p style='color: #CBD5E1; margin-top: 10px;'>
        YouTube kanalingizni ulang va sozlamalarni boshqaring
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")


# ============================================
# 1. YOUTUBE KANAL ULASH
# ============================================
st.markdown("### 📺 YouTube Kanal Ulash")

st.markdown("""
<div class='setting-card'>
    <h4 style='color: #A78BFA;'>Kanalingiz linkini kiriting:</h4>
    <p style='color: #CBD5E1;'>
        YouTube kanalingizning to'liq manzilini yozing.<br>
        Masalan: <code>https://youtube.com/@YourChannel</code>
    </p>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([3, 1])

with col1:
    channel_url = st.text_input(
        "YouTube Kanal Linki",
        value=st.session_state.youtube_channel_url,
        placeholder="https://youtube.com/@YourChannel",
        label_visibility="collapsed"
    )

with col2:
    if st.button("💾 Saqlash", key="save_channel"):
        if channel_url:
            # URL tekshirish
            if "youtube.com" in channel_url or "youtu.be" in channel_url:
                st.session_state.youtube_channel_url = channel_url
                
                # Kanal nomini ajratish
                if "@" in channel_url:
                    channel_name = channel_url.split("@")[-1].split("/")[0]
                    st.session_state.youtube_channel_name = channel_name
                else:
                    st.session_state.youtube_channel_name = "Kanal"
                
                st.success("✅ Kanal muvaffaqiyatli ulandi!")
                st.rerun()
            else:
                st.error("❌ Noto'g'ri YouTube link! youtube.com bo'lishi kerak")
        else:
            st.error("❌ Kanal linkini kiriting!")


# Ulangan kanal ko'rsatish
if st.session_state.youtube_channel_url:
    st.markdown(f"""
    <div class='success-msg'>
        <h3 style='margin: 0;'>✅ Kanal ulangan!</h3>
        <p style='margin: 5px 0;'>
            📺 Kanal: <strong>@{st.session_state.youtube_channel_name}</strong><br>
            🔗 Link: <a href='{st.session_state.youtube_channel_url}' target='_blank' 
                       style='color: white;'>{st.session_state.youtube_channel_url}</a>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("🔍 Kanalni Tahlil Qilish"):
            st.info("⚡ Kanal Analiz sahifasi tez kunda qo'shiladi!")
    
    with col_b:
        if st.button("🗑️ Kanalni O'chirish"):
            st.session_state.youtube_channel_url = ""
            st.session_state.youtube_channel_name = ""
            st.success("✅ Kanal o'chirildi")
            st.rerun()
else:
    st.markdown("""
    <div class='info-msg'>
        <h4 style='margin: 0;'>ℹ️ Kanal hali ulanmagan</h4>
        <p style='margin: 5px 0;'>
            YouTube kanal linkini kiriting va "Saqlash" tugmasini bosing.
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")


# ============================================
# 2. GOOGLE OAUTH (YouTube Upload uchun)
# ============================================
st.markdown("### 🔐 Google Akkount Ulash")

st.markdown("""
<div class='setting-card'>
    <h4 style='color: #A78BFA;'>YouTube'ga avtomatik yuklash uchun:</h4>
    <p style='color: #CBD5E1;'>
        Google akkountingizni ulasangiz, videolar avtomatik YouTube'ga yuklanadi.
    </p>
</div>
""", unsafe_allow_html=True)

if st.button("🔗 Google Akkount Bilan Ulash"):
    st.info("⚡ Bu funksiya keyingi versiyada qo'shiladi!")


st.markdown("---")


# ============================================
# 3. VIDEO SOZLAMALARI
# ============================================
st.markdown("### 🎬 Video Sozlamalari")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class='setting-card'>
        <h4 style='color: #A78BFA;'>Standart Niche</h4>
    </div>
    """, unsafe_allow_html=True)
    
    niche_options = {
        "horror_en": "🇺🇸 Horror English (Mr. Nightmare)",
        "horror_es": "🇪🇸 Horror Spanish",
        "history_en": "📜 History English",
        "war_ru": "🇷🇺 War Russian (СМЕРШ)"
    }
    
    selected_niche = st.selectbox(
        "Video niche'ini tanlang:",
        options=list(niche_options.keys()),
        format_func=lambda x: niche_options[x],
        index=list(niche_options.keys()).index(st.session_state.default_niche)
    )
    
    if st.button("💾 Niche Saqlash"):
        st.session_state.default_niche = selected_niche
        st.success(f"✅ Standart niche: {niche_options[selected_niche]}")

with col2:
    st.markdown("""
    <div class='setting-card'>
        <h4 style='color: #A78BFA;'>Til</h4>
    </div>
    """, unsafe_allow_html=True)
    
    language = st.selectbox(
        "Sayt tili:",
        options=["O'zbek", "English", "Русский"],
        index=["O'zbek", "English", "Русский"].index(st.session_state.preferred_language)
    )
    
    if st.button("💾 Til Saqlash"):
        st.session_state.preferred_language = language
        st.success(f"✅ Til o'zgartirildi: {language}")


st.markdown("---")


# ============================================
# 4. PROFIL MA'LUMOTLARI
# ============================================
st.markdown("### 👤 Profil Ma'lumotlari")

st.markdown(f"""
<div class='setting-card'>
    <p style='color: #CBD5E1;'>
        <strong>📧 Email:</strong> {st.session_state.get('user_email', 'Kirilmagan')}<br>
        <strong>👤 Foydalanuvchi:</strong> {st.session_state.get('user_name', 'Kirilmagan')}<br>
        <strong>📺 YouTube Kanal:</strong> {'@' + st.session_state.youtube_channel_name if st.session_state.youtube_channel_name else 'Ulanmagan'}<br>
        <strong>🎬 Standart Niche:</strong> {niche_options.get(st.session_state.default_niche, 'Tanlanmagan')}<br>
        <strong>🌐 Til:</strong> {st.session_state.preferred_language}
    </p>
</div>
""", unsafe_allow_html=True)


st.markdown("---")


# ============================================
# 5. XAVFLI ZONA
# ============================================
st.markdown("### ⚠️ Xavfli Zona")

col1, col2 = st.columns(2)

with col1:
    if st.button("🚪 Chiqish", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.user_email = None
        st.session_state.user_name = None
        st.success("✅ Tizimdan chiqildi")
        st.markdown("[🏠 Bosh sahifaga qaytish](/)")
        st.rerun()

with col2:
    if st.button("🗑️ Barcha ma'lumotlarni tozalash", use_container_width=True):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.success("✅ Barcha ma'lumotlar tozalandi")
        st.rerun()


# Sidebar
with st.sidebar:
    st.markdown("""
    <div style='text-align: center; padding: 20px;'>
        <h2 style='background: linear-gradient(135deg, #8B5CF6 0%, #EC4899 100%);
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                    background-clip: text;'>
            🎬 NurAuto
        </h2>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    if st.session_state.youtube_channel_url:
        st.success(f"✅ Kanal: @{st.session_state.youtube_channel_name}")
    else:
        st.warning("⚠️ Kanal ulanmagan")
    
    st.markdown("---")
    
    st.markdown("### 📊 Statistika")
    st.markdown("- Videolar: **0**")
    st.markdown("- Bugun: **0**")
    st.markdown("- Kvota: **500/500**")
