class Product:
    count_id = 0

    def __init__(self, full_name, email, category, membership, note, quantity, description, price):
        Product.count_id += 1
        self.__supplier_id = Product.count_id
        self.__full_name = full_name
        self.__email = email
        self.__category = category
        self.__membership = membership
        self.__note = note
        self.__quantity = quantity
        self.__description = description
        self.__price = price

    def get_supplier_id(self):
        return self.__supplier_id

    def get_full_name(self):
        return self.__full_name

    def get_email(self):
        return self.__email

    def get_category(self):
        return self.__category

    def get_membership(self):
        return self.__membership

    def get_note(self):
        return self.__note

    def get_quantity(self):
        return self.__quantity

    def get_description(self):
        return self.__description

    def get_price(self):
        return self.__price

    def set_supplier_id(self, supplier_id):
        self.__supplier_id = supplier_id

    def set_full_name(self, full_name):
        self.__full_name = full_name

    def set_email(self, email):
        self.__email = email

    def set_category(self, category):
        self.__category = category

    def set_membership(self, membership):
        self.__membership = membership

    def set_note(self, note):
        self.__note = note

    def set_quantity(self, quantity):
        self.__quantity = quantity

    def set_description(self, description):
        self.__description = description
