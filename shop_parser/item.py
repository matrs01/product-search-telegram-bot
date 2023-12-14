__all__ = ['Item']


class Item:
    '''Class for storing info about product:
    name, price, shop reference and picture link'''

    def __init__(self, name, price, ref, pic):
        self.name = name
        self.price = price
        self.ref = ref
        self.pic = pic
