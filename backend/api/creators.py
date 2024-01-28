from starlette.responses import StreamingResponse
from fastapi import APIRouter
import json
import io

from backend.data_management.saver import Saver

creator_router = APIRouter(prefix="/creators")
saver = Saver()


@creator_router.get("/")
def get_creators():
    creators = Saver.get_creators()
    return creators


@creator_router.get("/{creator}/cards")
def get_creator_cards(creator: str):
    """
    This function receives a creator and returns all the solved cards of the given creator.
    :param creator: The creator of the cards to be returned.
    :return:
    """
    cards = saver.find_cards(True, creator=creator)
    return cards


@creator_router.get("/{creator}/cards/{card_name}")
def get_solved_card_by_name(creator: str, card_name: str):
    """
    This function receives a creator and returns all the solved cards of the given creator.
    :param creator: The creator of the cards to be returned.
    :return:
    """
    card = saver.find_cards(True, creator=creator, name=card_name)
    if len(card) == 0:
        return json.dumps({})
    return json.dumps(card[0])


@creator_router.get("/{creator}/cards/{card_name}/image.jpg")
def get_solved_card_image(creator: str, card_name: str):
    """
    This function receives a creator and returns all the solved cards of the given creator.
    :param creator: The creator of the cards to be returned.
    :param card_name: The name of the card to be returned.
    :return:
    """
    cards = saver.find_cards(True, creator=creator, name=card_name)
    if len(cards) == 0:
        return json.dumps({})
    card = cards[0]
    image_bytes_io = io.BytesIO()
    card.image.image.save(image_bytes_io, format="JPEG")
    image_bytes_io.seek(0)
    return StreamingResponse(io.BytesIO(image_bytes_io.read()), media_type="image/jpeg")
