import streamlit as st
import requests

st.title("Partage de Places de Parking 🚗")
st.write("Bienvenue sur l'application de partage de places de parking entre particuliers.")

API_URL = "http://127.0.0.1:8000"  # Remplace par l'URL de ton API FastAPI

# st.set_page_config(page_title="Gestion des Réservations", layout="centered")

st.title("🚗 Gestion des Réservations de Parking")

if "token" not in st.session_state:
    st.session_state.token = None

# 📌 Authentification de l'utilisateur (simple pour l'instant)
st.sidebar.title("Connexion")
email = st.sidebar.text_input("Email", "test@example.com", key="email_login")
password = st.sidebar.text_input("Mot de passe", type="password", key="password_login")

if st.sidebar.button("Se connecter"):
    response = requests.post(f"{API_URL}/auth/login", data={"username": email, "password": password})

    if response.status_code == 200:
        data = response.json()
        st.session_state.token = data["access_token"]
        st.sidebar.success("Connexion réussie !")
    else:
        st.sidebar.error("Échec de la connexion")

if st.session_state.token:
    headers = {"Authorization": f"Bearer {st.session_state.token}"}

    # Récupérer les places disponibles
    st.subheader("Places de Parking Disponibles")
    response = requests.get(f"{API_URL}/parkingspots/available", headers=headers)
    if response.status_code == 200:
        parking_spots = response.json()
        if not parking_spots:
            st.info("Aucune place disponible pour l'instant.")
        else:
            selected_spot = st.selectbox("Choisir une place", [f"ID {p['id']} - {p['location']}" for p in parking_spots])
            spot_id = int(selected_spot.split()[1])  # Récupérer l'ID de la place

            if st.button("Réserver cette place"):
                user_id = 3  # Normalement, tu récupères l'ID depuis l'authent
                response = requests.post(f"{API_URL}/reservations/", json={"user_id": user_id,"parking_spot_id": spot_id, "end_time": "string"}, headers=headers)
                if response.status_code == 200:
                    st.success("Réservation confirmée !")
                else:
                    st.error("Erreur lors de la réservation.")

# Afficher les réservations en cours
    st.subheader("Vos Réservations Actuelles")
    response = requests.get(f"{API_URL}/reservations/available", headers=headers)  # Route pour récupérer les réservations de l'utilisateur
    if response.status_code == 200:
        reservations = response.json()
        if not reservations:
            st.info("Vous n'avez aucune réservation en cours.")
        else:
            selected_reservation = st.selectbox(
                "Sélectionner une réservation à terminer",
                [f"ID {r['id']} - Place {r['parking_spot_id']} (Réservée le {r['start_time']})" for r in reservations]
            )
            reservation_id = int(selected_reservation.split()[1])  # Extraire l'ID de la réservation

            if st.button("Terminer la réservation"):
                response = requests.put(f"{API_URL}/reservations/{reservation_id}/end", headers=headers)
                if response.status_code == 200:
                    st.success("Réservation terminée avec succès !")
                else:
                    st.error("Erreur lors de la suppression de la réservation.")
    else:
        st.error("Erreur lors de la récupération des réservations.")


st.sidebar.title("Enregistrement")
email_create_count = st.sidebar.text_input("Email", "test@example.com", key="email_create")
password_create_count = st.sidebar.text_input("Mot de passe", type="password", key="password_create")
username_create_count = st.sidebar.text_input("Non Utilisateur",  key="username_create")

if st.sidebar.button("Créer un compte"):
    response = requests.post(f"{API_URL}/users/new", data={"username": username_create_count, 
                                                           "email": email_create_count, 
                                                           "password": password_create_count})
       
    if response.status_code == 400:
        data = response.json()
        st.sidebar.error(data["detail"])
    else:
        st.sidebar.success("Compte créé avec succès !")