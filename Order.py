import Supplier


class Order(Supplier):
    def __init__(self, full_name, email, category, membership, note, quantity, description, price, order):
        super().__init__(full_name, email, category, membership, note, quantity, description, price)
        self.__order == order

    def get_order(self):
        return self.__order

    def set_order(self, order):
        self.__order = order
