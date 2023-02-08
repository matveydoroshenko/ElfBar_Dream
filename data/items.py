from dataclasses import dataclass

from db_tg.db import Database


@dataclass
class Item:
    id: int
    name: str
    description: str
    photo: str


def create_items_list(item_id):
    db = Database()
    item_data = db.select_product(item_id=item_id)
    item = Item(id=item_data[0], name=item_data[1], photo=item_data[2], description=item_data[3])
    puffs = item_data[4]
    return item, puffs
