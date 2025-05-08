import streamlit as st
import streamlit.components.v1 as components
import pickle
import requests
import random

# Load data
movie_list = pickle.load(open("movie.pkl", "rb"))
similarity = pickle.load(open("similarity.pkl", "rb"))

st.set_page_config(layout="wide")

# --- App Title ---
st.markdown("""
    <div style='text-align: center; padding: 20px 0 40px 0;'>
        <h1 style='
            font-size: 3.5em; 
            font-weight: 900; 
            background: -webkit-linear-gradient(45deg, #ff4b1f, #1fddff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.1em;
        '>
            CouchCritic
        </h1>
        <h3 style='
            font-style: italic; 
            color: #444; 
            font-weight: 400; 
            letter-spacing: 0.5px;
        '>
            Lazy picks, smart choices 🎥🍿
        </h3>
    </div>
""", unsafe_allow_html=True)

# --- API Fetching with Error Handling ---
def fetch_movie_details(movie_id):
    try:
        response = requests.get(
            f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Failed to fetch movie details. Error: {e}")
        return {}

def fetch_poster(movie_id):
    data = fetch_movie_details(movie_id)
    if data and data.get('poster_path'):
        return "https://image.tmdb.org/t/p/w500" + data['poster_path']
    else:
        return "https://via.placeholder.com/500x750?text=No+Poster+Available"

def fetch_trailer(movie_id):
    try:
        response = requests.get(
            f"https://api.themoviedb.org/3/movie/{movie_id}/videos?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
        )
        response.raise_for_status()
        data = response.json()
        for video in data.get("results", []):
            if video["site"] == "YouTube" and video["type"] == "Trailer":
                return f"https://www.youtube.com/embed/{video['key']}"
    except Exception as e:
        st.error(f"Failed to fetch trailer. Error: {e}")
    return None

# --- Banner section ---
random_id = random.choice(movie_list['id'].tolist())
banner_data = fetch_movie_details(random_id)

if banner_data:
    banner_title = banner_data.get('title', 'Unknown Title')
    banner_rating = round(banner_data.get('vote_average', 0), 2)
    banner_overview = banner_data.get('overview', 'No description available.')[:200] + "..."
    banner_trailer_url = fetch_trailer(random_id)

    if banner_trailer_url:
        st.markdown(f"## 🎬 {banner_title} (IMDb: {banner_rating} ⭐)")
        st.markdown(f"**{banner_overview}**")
        components.html(f"""
            <iframe width="100%" height="500" 
                    src="{banner_trailer_url}?autoplay=0&mute=1&controls=1" 
                    frameborder="0" 
                    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
                    allowfullscreen>
            </iframe>
        """, height=500)
    else:
        st.warning("Trailer not found for this movie.")
else:
    st.warning("Unable to load banner content.")

# --- Movie selector ---
st.markdown("## 🎯 Select a Movie to Get Recommendations")
selected_movie = st.selectbox("Choose a movie", movie_list['title'].values)

# --- Session state management ---
if "show_recommendations" not in st.session_state:
    st.session_state.show_recommendations = False

if "trailer_to_play" not in st.session_state:
    st.session_state.trailer_to_play = None

# --- Button to trigger recommendations ---
if st.button("Get Recommendations 🎯"):
    st.session_state.show_recommendations = True
    st.session_state.trailer_to_play = None

# --- Recommend function ---
def recommend(movie):
    index = movie_list[movie_list['title'] == movie].index[0]
    distances = similarity[index]
    recommended = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    titles, posters, ids = [], [], []
    for i in recommended:
        movie_id = movie_list.iloc[i[0]].id
        titles.append(movie_list.iloc[i[0]].title)
        posters.append(fetch_poster(movie_id))
        ids.append(movie_id)

    return titles, posters, ids

# --- Show recommendations only if requested ---
if st.session_state.show_recommendations:
    names, images, movie_ids = recommend(selected_movie)
    st.markdown("### 🍿 You Might Also Like")
    cols = st.columns(len(names))

    for i in range(len(names)):
        with cols[i]:
            st.image(images[i], use_container_width=True)
            st.caption(names[i])
            with st.form(f"form_{i}"):
                play_button = st.form_submit_button("▶ Watch Trailer")
                if play_button:
                    st.session_state.trailer_to_play = movie_ids[i]

    # --- Show trailer for clicked recommendation ---
    if st.session_state.trailer_to_play:
        trailer_url = fetch_trailer(st.session_state.trailer_to_play)
        if trailer_url:
            st.markdown("### 🎞️ Trailer Preview")
            components.html(f"""
                <iframe width="100%" height="400"
                        src="{trailer_url}?autoplay=1&mute=0&controls=1" 
                        frameborder="0"
                        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
                        allowfullscreen>
                </iframe>
            """, height=400)
        else:
            st.warning("Trailer not found for the selected movie.")
