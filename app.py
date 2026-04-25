import streamlit as st
import requests

# --- CONFIGURARE ---
st.set_page_config(page_title="CineRating Premium", page_icon="🎬", layout="wide")

API_TOKEN = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJkYjJlN2RlODZhMWY0ODZjZTI0NDhiZTE5NzE2MzU3YyIsIm5iZiI6MTc3NzExMDc4OS4yMjgsInN1YiI6IjY5ZWM4ZjA1ZmU1NDgyZGVkMDAyOGM5MSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.VbqbAT0WX4fauybz-6wLuGjbgV5x1enui76EnmPyVQU"

# --- DESIGN PREMIUM CU FONT ROTUNJIT ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;800&display=swap');
    
    html, body, [class*="st-"] {
        font-family: 'Nunito', sans-serif;
        background-color: #f9fbff;
    }

    .main-card {
        background: white;
        padding: 35px;
        border-radius: 30px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.05);
        border: 1px solid #edf2f7;
    }

    .movie-title {
        font-size: 3rem;
        font-weight: 800;
        color: #1a202c;
        line-height: 1.1;
        margin-bottom: 10px;
    }

    .rating-pill {
        background: #ffffff;
        border: 2px solid #e2e8f0;
        border-radius: 18px;
        padding: 12px;
        text-align: center;
        transition: all 0.3s ease;
    }

    .rating-pill:hover {
        border-color: #4299e1;
        transform: translateY(-3px);
        box-shadow: 0 4px 12px rgba(66, 153, 225, 0.15);
    }

    .rating-val {
        font-size: 1.6rem;
        font-weight: 800;
        color: #2d3748;
        display: block;
    }

    .cnc-btn {
        background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);
        color: white !important;
        padding: 14px 28px;
        border-radius: 15px;
        text-decoration: none;
        font-weight: 600;
        display: inline-block;
        box-shadow: 0 4px 14px rgba(72, 187, 120, 0.3);
    }

    .legend-item {
        margin-bottom: 8px;
        font-size: 0.95rem;
    }
    </style>
    """, unsafe_allow_html=True)

def get_data(query):
    headers = {"Authorization": f"Bearer {API_TOKEN.strip()}"}
    res = requests.get(f"https://api.themoviedb.org/3/search/multi?query={query}&language=ro-RO", headers=headers).json()
    if res.get('results'):
        best = sorted(res['results'], key=lambda x: x.get('popularity', 0), reverse=True)[0]
        m_id = best['id']
        m_type = best['media_type']
        return requests.get(f"https://api.themoviedb.org/3/{m_type}/{m_id}?append_to_response=release_dates,content_ratings,credits&language=ro-RO", headers=headers).json(), m_type
    return None, None

# --- UI ---
st.markdown("<h1 style='text-align: center; font-weight: 800; color: #2d3748;'>🎬 CineRating Intelligence</h1>", unsafe_allow_html=True)
query = st.text_input("", placeholder="Caută un film sau serial...", key="search_input")

if query:
    data, m_type = get_data(query)
    if data:
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        col_img, col_txt = st.columns([1, 2.2])
        
        with col_img:
            st.image(f"https://image.tmdb.org/t/p/w500{data.get('poster_path')}", use_container_width=True)
            # Link CNC actualizat (HTTPS)
            st.markdown(f'<center><a href="https://cnc.gov.ro/clasificare-filme/" target="_blank" class="cnc-btn">🔍 Verifică la CNC România</a></center>', unsafe_allow_html=True)

        with col_txt:
            st.markdown(f"<div class='movie-title'>{data.get('title', data.get('name'))}</div>", unsafe_allow_html=True)
            an = (data.get('release_date') or data.get('first_air_date', '----'))[:4]
            durata = f"{data.get('runtime')} min" if m_type == 'movie' else f"{data.get('number_of_seasons')} Sezoane"
            regizor = "N/A"
            if 'credits' in data:
                regizor = ", ".join([c['name'] for c in data['credits']['crew'] if c['job'] in ['Director', 'Executive Producer']][:1])
            
            st.markdown(f"<p style='color: #718096; font-size: 1.1rem;'>🗓️ {an}  •  ⏱️ {durata}  •  🎬 Regia: {regizor}</p>", unsafe_allow_html=True)
            st.write(data.get('overview'))
            
            st.markdown("<h4 style='margin-top: 30px;'>🌍 Clasificări pe țări</h4>", unsafe_allow_html=True)
            tari = {'RO': '🇷🇴 RO', 'US': '🇺🇸 USA', 'GB': '🇬🇧 UK', 'FR': '🇫🇷 FR', 'DE': '🇩🇪 DE', 'IT': '🇮🇹 IT', 'ES': '🇪🇸 ES', 'CA': '🇨🇦 CA', 'AU': '🇦🇺 AU', 'JP': '🇯🇵 JP'}
            
            ratings = {}
            if m_type == 'movie':
                for r in data.get('release_dates', {}).get('results', []):
                    if r['iso_3166_1'] in tari: ratings[r['iso_3166_1']] = r['release_dates'][0]['certification']
            else:
                for r in data.get('content_ratings', {}).get('results', []):
                    if r['iso_3166_1'] in tari: ratings[r['iso_3166_1']] = r['rating']

            r_cols = st.columns(5)
            codes = list(tari.keys())
            for i in range(10):
                with r_cols[i % 5]:
                    c_code = codes[i]
                    val = ratings.get(c_code, "N/A")
                    st.markdown(f"""
                        <div class="rating-pill">
                            <span style="font-size: 0.75rem; color: #718096; font-weight: 600;">{tari[c_code]}</span>
                            <span class="rating-val">{val if val else 'N/A'}</span>
                        </div>
                    """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # --- LEGENDA ÎMBUNĂTĂȚITĂ ---
        with st.expander("📖 Legenda Clasificărilor (Semnificație simboluri)"):
            l1, l2, l3 = st.columns(3)
            with l1:
                st.markdown("### 🇷🇴 România")
                st.markdown("**AG**: Toate vârstele<br>**AP-12**: Acordul părinților sub 12 ani<br>**N-15**: Nerecomandat sub 15 ani<br>**18**: Interzis minorilor", unsafe_allow_html=True)
                st.markdown("### 🇺🇸 USA / 🇨🇦 CA")
                st.markdown("**G**: General<br>**PG**: Parental Guidance<br>**PG-13**: Peste 13 ani<br>**R**: Restricționat<br>**NC-17**: Adult", unsafe_allow_html=True)
            with l2:
                st.markdown("### 🇪🇺 Europa (IT, ES, FR, DE)")
                st.markdown("**T / A / U**: Toate vârstele<br>**6 / 7**: Peste 6-7 ani<br>**12 / 14**: Peste 12-14 ani<br>**16 / 18**: Peste 16-18 ani", unsafe_allow_html=True)
                st.markdown("### 🇬🇧 Marea Britanie")
                st.markdown("**U**: Universal<br>**PG**: Parental Guidance<br>**12A**: Peste 12 ani (însoțit)<br>**15 / 18**: Peste 15/18 ani", unsafe_allow_html=True)
            with l3:
                st.markdown("### 🌏 Asia & Australia")
                st.markdown("**G**: General<br>**PG / PG12**: Peste 12 recomandat<br>**M / R15+**: Peste 15 recomandat<br>**MA15+ / R18+**: Adult", unsafe_allow_html=True)
    else:
        st.error("Film negăsit. Încearcă un alt nume.")
