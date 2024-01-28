from starlette.responses import StreamingResponse
from fastapi import FastAPI
import json
import io

from backend.data_management.saver import Saver

app = FastAPI()
saver = Saver()


@app.get("/creators")
def get_creators():
    creators = Saver.get_creators()
    return json.dumps(creators)


@app.get("/creators/{creator}/cards")
def get_creator_cards(creator: str):
    """
    This function receives a creator and returns all the solved cards of the given creator.
    :param creator: The creator of the cards to be returned.
    :return:
    """
    cards = saver.find_cards(True, creator=creator)
    return json.dumps(cards)


@app.get("/creators/{creator}/cards/{card_name}")
def get_solved_card_by_name(creator: str, card_name: str):
    """
    This function receives a creator and returns all the solved cards of the given creator.
    :param creator: The creator of the cards to be returned.
    :return:
    """
    card = saver.find_cards(True, creator=creator, name=card_name)[0] # Finds one anyways, this is a singleton
    return json.dumps(card)


@app.get("/creators/{creator}/cards/{card_name}/image.jpg")
def get_solved_card_image(creator: str, card_name: str):
    """
    This function receives a creator and returns all the solved cards of the given creator.
    :param creator: The creator of the cards to be returned.
    :param card_name: The name of the card to be returned.
    :return:
    """
    card = saver.find_cards(True, creator=creator, name=card_name)[0]
    image_bytes = card.get_image_bytes()
    return StreamingResponse(io.BytesIO(image_bytes), media_type="image/jpeg")
