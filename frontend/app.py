import streamlit as st
import requests

GAME_SERVICE = "http://game-service:8001"
RECOMMENDER_SERVICE = "http://recommender-service:8002"

st.set_page_config(page_title="Game Recommender", page_icon="")
st.title(" Game Recommender")

# ── TABS ──
tab1, tab2, tab3 = st.tabs(["Mi Biblioteca", "Añadir Juego", "Recomendaciones"])

# ── TAB 1: biblioteca ──
with tab1:
    st.subheader("Mis juegos")

    col1, col2 = st.columns(2)
    with col1:
        status_filter = st.selectbox("Filtrar por estado", ["todos", "jugando", "completado", "pendiente", "abandonado"])
    with col2:
        genre_filter = st.text_input("Filtrar por género")

    params = {}
    if status_filter != "todos":
        params["status"] = status_filter
    if genre_filter:
        params["genre"] = genre_filter

    response = requests.get(f"{GAME_SERVICE}/games/", params=params)
    games = response.json()

    if not games:
        st.info("No tienes juegos aún. ¡Añade alguno!")
    else:
        for game in games:
            with st.expander(f" {game['title']} — {game['status']}"):
                st.write(f"**Género:** {game['genre']}")
                st.write(f"**Plataforma:** {game['platform']}")
                st.write(f"**Puntuación:** {game['rating'] or 'Sin puntuar'}")

                # Cambiar estado
                new_status = st.selectbox(
                    "Cambiar estado",
                    ["jugando", "completado", "pendiente", "abandonado"],
                    key=f"status_{game['id']}"
                )
                if st.button("Actualizar", key=f"btn_{game['id']}"):
                    requests.patch(
                        f"{GAME_SERVICE}/games/{game['id']}",
                        json={"status": new_status}
                    )
                    st.success("¡Actualizado!")
                    st.rerun()

# ── TAB 2: añadir juego ──
with tab2:
    st.subheader("Añadir juego")

    title = st.text_input("Título")
    genre = st.selectbox("Género", ["RPG", "FPS", "MOBA", "Aventura", "Deportes", "Lucha", "Plataformas", "Puzzles", "Carreras"])
    platform = st.selectbox("Plataforma", ["PC", "PS5", "Xbox", "Nintendo Switch", "Mobile"])
    status = st.selectbox("Estado", ["pendiente", "jugando", "completado", "abandonado"])
    rating = st.slider("Puntuación", 1.0, 10.0, 5.0, step=0.5) if status == "completado" else None

    if st.button("Añadir juego"):
        if not title:
            st.error("El título es obligatorio")
        else:
            payload = {
                "title": title,
                "genre": genre,
                "platform": platform,
                "status": status,
                "rating": rating
            }
            response = requests.post(f"{GAME_SERVICE}/games/", json=payload)
            if response.status_code == 201:
                st.success(f" {title} añadido correctamente")
                st.rerun()
            else:
                st.error("Error al añadir el juego")

# ── TAB 3: recomendaciones ──
with tab3:
    st.subheader("Recomendaciones personalizadas")

    genre_rec = st.selectbox(
        "Género para recomendar",
        ["automático", "RPG", "FPS", "MOBA", "Aventura", "Deportes", "Lucha", "Plataformas", "Puzzles", "Carreras"]
    )

    if st.button("Buscar recomendaciones"):
        params = {}
        if genre_rec != "automático":
            params["genre"] = genre_rec

        response = requests.get(f"{RECOMMENDER_SERVICE}/recommendations/", params=params)
        data = response.json()

        if not data["recommendations"]:
            st.warning(data.get("message", "No hay recomendaciones disponibles"))
        else:
            st.write(f"**Basado en:** {', '.join(data['based_on_genres'])}")
            for game in data["recommendations"]:
                with st.expander(f" {game['title']} — {game['rating']}"):
                    st.write(f"**Géneros:** {', '.join(game['genres'])}")