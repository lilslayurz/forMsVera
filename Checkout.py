class Checkout:
    count_id = 0

    def __init__(self, name, email, country, address, card, date, cvv, status):
        Checkout.count_id += 1
        self.__order_id = Checkout.count_id
        self.__name = name
        self.__email = email
        self.__country = country
        self.__address = address
        self.__card = card
        self.__date = date
        self.__cvv = cvv
        self.__status = status

    def get_order_id(self):
        return self.__order_id

    def get_name(self):
        return self.__name

    def get_email(self):
        return self.__email

    def get_country(self):
        return self.__country

    def get_address(self):
        return self.__address

    def get_card(self):
        return self.__card

    def get_date(self):
        return self.__date

    def get_cvv(self):
        return self.__cvv

    def get_status(self):
        return self.__status

    def set_order_id(self, order_id):
        self.__order_id = order_id

    def set_name(self, name):
        self.__name = name

    def set_email(self, email):
        self.__email = email

    def set_country(self, country):
        self.__country = country

    def set_address(self, address):
        self.__address = address

    def set_card(self, card):
        self.__card = card

    def set_date(self, date):
        self.__date = date

    def set_CVV(self, cvv):
        self.__cvv = cvv

    def set_status(self, status):
        self.__status = status
