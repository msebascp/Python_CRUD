class Product:
    headings = ['ID', 'Name', 'Category', 'Price']

    fields = {
        '-ID-': 'Product ID:',
        '-Name-': 'Name of Product:',
        '-Category-': 'Category:',
        '-Price-': 'Price:',
    }

    def __init__(self, product_id, name, category, price):
        self.id = product_id
        self.name = name
        self.category = category
        self.price = price

    def __eq__(self, other_product):
        return self.id == other_product.id

    def __str__(self):
        return f"{self.id} {self.name} {self.category} {self.price}"

    def set_product(self, name, category, price):
        self.name = name
        self.category = category
        self.price = price
