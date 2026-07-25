"""
NurAuto - Sozlamalar (YouTube OAuth)
"""
import streamlit as st
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

# Sahifa sozlamalari
st.set_page_config(
    page_title="Sozlamalar - NurAuto",
    page_icon="⚙️",
    layout="wide"
)

# CSS
st.markdown("""
<style>
    .main {
        background: linear-gradient(180deg, #0F0F1E 0%, #1A1A2E 100%);
    }
    h1, h2, h3 {color: #FFFFFF !important;}
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
    .channel-card {
        background: linear-gradient(135deg, #1E1B4B 0%, #4C1D95 100%);
        padding: 30px;
        border-radius: 20px;
        border: 2px solid #8B5CF6;
        text-align: center;
        margin: 20px 0;
    }
    .youtube-btn {
        background: linear-gradient(135deg, #FF0000 0%, #CC0000 100%) !important;
    }
</style>
""", unsafe_allow_html=True)


# Login tekshirish
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.warning("⚠️ Avval tizimga kiring!")
    st.stop()


# OAuth scopes - HAMMA kerakli ruxsatlar
YT_SCOPES = [
    'https://www.googleapis.com/auth/youtube.readonly',
    'https://www.googleapis.com/auth/youtube.upload',
    'https://www.googleapis.com/auth/yt-analytics.readonly',
    'openid',
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile'
]


# Session state
if 'youtube_credentials' not in st.session_state:
    st.session_state.youtube_credentials = None
if 'youtube_channel_info' not in st.session_state:
    st.session_state.youtube_channel_info = None


# Sarlavha
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
        YouTube kanalingizni ulang va boshqaring
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")


# ============================================
# YOUTUBE KANAL ULASH (OAuth)
# ============================================
st.markdown("### 📺 YouTube Kanal Ulash")

# Kanal ulangan bo'lsa
if st.session_state.youtube_channel_info:
    ch = st.session_state.youtube_channel_info
    
    subs = int(ch.get('subscriber_count', 0))
    videos = int(ch.get('video_count', 0))
    views = int(ch.get('view_count', 0))
    
    st.markdown(f"""
    <div class='channel-card'>
        <img src='{ch.get("thumbnail", "")}' 
             style='width: 120px; height: 120px; border-radius: 50%; 
                    border: 4px solid #8B5CF6; margin-bottom: 15px;
                    box-shadow: 0 10px 30px rgba(139, 92, 246, 0.5);'>
        <h2 style='color: white; margin: 10px 0;'>
            ✅ {ch.get('title', 'Kanal')}
        </h2>
        <p style='color: #CBD5E1; margin: 5px 0; font-size: 16px;'>
            {'@' + ch.get('custom_url') if ch.get('custom_url') else ch.get('title', '')}
        </p>
        <div style='display: flex; justify-content: space-around; 
                    margin-top: 25px; padding-top: 20px; 
                    border-top: 2px solid #4C1D95;'>
            <div>
                <h2 style='color: #8B5CF6; margin: 0;'>{subs:,}</h2>
                <p style='color: #CBD5E1; margin: 0;'>👥 Obunachilar</p>
            </div>
            <div>
                <h2 style='color: #EC4899; margin: 0;'>{videos}</h2>
                <p style='color: #CBD5E1; margin: 0;'>📹 Videolar</p>
            </div>
            <div>
                <h2 style='color: #F59E0B; margin: 0;'>{views:,}</h2>
                <p style='color: #CBD5E1; margin: 0;'>👁️ Ko'rishlar</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔍 Kanalni Chuqur Tahlil Qilish"):
            st.info("⚡ Kanal Analiz sahifasi tez kunda!")
    
    with col2:
        if st.button("🗑️ Kanalni Uzish"):
            st.session_state.youtube_credentials = None
            st.session_state.youtube_channel_info = None
            st.success("✅ Kanal uzildi")
            st.rerun()

else:
    # Kanal ulanmagan - ulash tugmasi
    st.markdown("""
    <div class='setting-card'>
        <h4 style='color: #A78BFA;'>📺 YouTube kanalingizni ulang</h4>
        <p style='color: #CBD5E1;'>
            Ulash orqali quyidagilarga ruxsat berasiz:<br>
            ✅ Kanal statistikasini olish<br>
            ✅ Video yuklash<br>
            ✅ Analitika (audience, views, revenue)<br>
            ✅ AI tahlil qilish
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # OAuth flow
    try:
        client_id = st.secrets["GOOGLE_OAUTH_CLIENT_ID"]
        client_secret = st.secrets["GOOGLE_OAUTH_CLIENT_SECRET"]
        redirect_uri = st.secrets.get("REDIRECT_URI", "https://nurauto.streamlit.app")
        
        # OAuth Flow yaratish
        flow = Flow.from_client_config(
            {
                "web": {
                    "client_id": client_id,
                    "client_secret": client_secret,
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "redirect_uris": [redirect_uri]
                }
            },
            scopes=YT_SCOPES,
            redirect_uri=redirect_uri
        )
        
        # URL parametridan code olish
        query_params = st.query_params
        
        if "code" in query_params:
            # Code bor - token olamiz
            try:
                with st.spinner("🔄 Kanal ulanmoqda..."):
                    code = query_params["code"]
                    flow.fetch_token(code=code)
                    credentials = flow.credentials
                    
                    # Credentials saqlash
                    st.session_state.youtube_credentials = {
                        'token': credentials.token,
                        'refresh_token': credentials.refresh_token,
                        'token_uri': credentials.token_uri,
                        'client_id': credentials.client_id,
                        'client_secret': credentials.client_secret,
                        'scopes': credentials.scopes
                    }
                    
                    # Kanal ma'lumotlarini olish
                    youtube = build('youtube', 'v3', credentials=credentials)
                    response = youtube.channels().list(
                        part='snippet,statistics',
                        mine=True
                    ).execute()
                    
                    if response.get('items'):
                        channel = response['items'][0]
                        snippet = channel['snippet']
                        stats = channel['statistics']
                        
                        st.session_state.youtube_channel_info = {
                            'id': channel['id'],
                            'title': snippet['title'],
                            'description': snippet.get('description', ''),
                            'custom_url': snippet.get('customUrl', ''),
                            'thumbnail': snippet['thumbnails']['high']['url'],
                            'subscriber_count': stats.get('subscriberCount', 0),
                            'video_count': stats.get('videoCount', 0),
                            'view_count': stats.get('viewCount', 0),
                        }
                        
                        # URL'dan code tozalash
                        st.query_params.clear()
                        st.success("✅ Kanal muvaffaqiyatli ulandi!")
                        st.balloons()
                        st.rerun()
                    else:
                        st.error("❌ Bu akkountda YouTube kanal topilmadi")
                        st.info("💡 Google akkountingizda YouTube kanal borligiga ishonch hosil qiling")
            
            except Exception as e:
                st.error(f"❌ Xato: {str(e)[:200]}")
                st.info("💡 Qayta urinib ko'ring")
                if st.button("🔄 Qayta urinish"):
                    st.query_params.clear()
                    st.rerun()
        
        else:
            # Code yo'q - ulash tugmasini ko'rsatamiz
            auth_url, _ = flow.authorization_url(
                access_type='offline',
                prompt='consent',
                include_granted_scopes='true'
            )
            
            st.markdown(f"""
            <div style='text-align: center; margin-top: 20px;'>
                <a href='{auth_url}' target='_self' 
                   style='text-decoration: none;'>
                    <button style='
                        background: linear-gradient(135deg, #FF0000 0%, #CC0000 100%);
                        color: white;
                        border: none;
                        padding: 18px 40px;
                        border-radius: 12px;
                        font-weight: bold;
                        font-size: 20px;
                        cursor: pointer;
                        width: 100%;
                        max-width: 400px;
                        box-shadow: 0 8px 25px rgba(255, 0, 0, 0.4);
                        transition: all 0.3s;
                    '>
                        🔗 YouTube Bilan Ulash
                    </button>
                </a>
            </div>
            """, unsafe_allow_html=True)
            
            st.info("💡 Tugmani bosgach, Google login sahifasi ochiladi. Kanalingizni tanlab, ruxsat bering.")
    
    except KeyError as e:
        st.error(f"❌ API kalit topilmadi: {e}")
        st.info("💡 Streamlit Secrets'da GOOGLE_OAUTH_CLIENT_ID va GOOGLE_OAUTH_CLIENT_SECRET qo'shilganligini tekshiring")
    
    except Exception as e:
        st.error(f"❌ Xato: {str(e)}")


st.markdown("---")


# ============================================
# PROFIL MA'LUMOTLARI
# ============================================
st.markdown("### 👤 Profil Ma'lumotlari")

profile_youtube = "❌ Ulanmagan"
if st.session_state.youtube_channel_info:
    profile_youtube = f"✅ {st.session_state.youtube_channel_info['title']}"

st.markdown(f"""
<div class='setting-card'>
    <p style='color: #CBD5E1; font-size: 16px; line-height: 1.8;'>
        <strong>📧 Email:</strong> {st.session_state.get('user_email', 'Kirilmagan')}<br>
        <strong>👤 Foydalanuvchi:</strong> {st.session_state.get('user_name', 'Kirilmagan')}<br>
        <strong>📺 YouTube:</strong> {profile_youtube}
    </p>
</div>
""", unsafe_allow_html=True)


st.markdown("---")


# Chiqish
col1, col2 = st.columns(2)
with col1:
    if st.button("🚪 Chiqish"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

with col2:
    st.markdown("[🏠 Bosh sahifaga qaytish](/)")


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
    
    if st.session_state.youtube_channel_info:
        ch = st.session_state.youtube_channel_info
        subs = int(ch.get('subscriber_count', 0))
        st.success(f"✅ {ch['title'][:20]}")
        st.markdown(f"👥 {subs:,} obunachilar")
    else:
        st.warning("⚠️ Kanal ulanmagan")
    
    st.markdown("---")
    st.markdown("### 📊 Statistika")
    st.markdown("- Videolar: **0**")
    st.markdown("- Bugun: **0**")
