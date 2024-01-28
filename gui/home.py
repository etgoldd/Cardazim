import streamlit as st
from PIL import Image
import requests
import json
import io

API_URL = "http://127.0.0.1:8000"


def get_creators():
    response = requests.get(f"{API_URL}/creators/")
    creators = json.loads(response.text)
    return creators


def get_cards(creator: str) -> list[dict]:
    response = requests.get(f"{API_URL}/creators/{creator}/cards")
    cards = json.loads(response.text)
    return cards


def show_card(card: dict):
    presentable_data = card.copy()
    presentable_data.pop('path')
    st.table(presentable_data)

    image_bytes = requests.get(f"{API_URL}/creators/{card['creator']}/cards/{card['name']}/image.jpg").content
    image = Image.open(io.BytesIO(image_bytes))

    st.image(image, use_column_width=True)


def app():
    st.title("Cardazim card viewer")
    creator = st.selectbox("Choose a creator", get_creators())
    cards = {card['name']: card for card in get_cards(creator)}
    selected_card_name = st.selectbox("Choose a card", cards.keys())
    st.write(f"Viewing: {selected_card_name}")
    selected_card: dict = cards[selected_card_name]

    show_card(selected_card)





app()

