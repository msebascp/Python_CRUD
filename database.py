import pyodbc


def get_connection():
    dsn_name = 'python_crud'
    database_name = 'python_crud'
    connection = pyodbc.connect('DSN={}'.format(dsn_name))
    connection.execute('USE {}'.format(database_name))
    return connection


class Product:
    def __init__(self, id, model, name, brand, price):
        self.id = id
        self.model = model
        self.name = name
        self.brand = brand
        self.price = price


class Product_repository:
    def __init__(self):
        self.connection = get_connection()

    def create_product(self, model, name, brand, price):
        query = "INSERT INTO products (model, name, brand, price) VALUES (?, ?, ?, ?)"
        values = (model, name, brand, price)
        cursor = self.connection.cursor()
        cursor.execute(query, values)
        self.connection.commit()
        print("Product successfully created")

    def get_all_products(self):
        query = "SELECT * FROM products"
        cursor = self.connection.cursor()
        cursor.execute(query)
        products = cursor.fetchall()
        return [Product(id=p[0], model=p[1], name=p[2], brand=p[3], price=p[4]) for p in products]

    def update_product(self, product_id, model, name, brand, price):
        query = "UPDATE products SET model = ?, name = ?, brand = ?, price = ? WHERE id = ?"
        values = (model, name, brand, price, product_id)
        cursor = self.connection.cursor()
        cursor.execute(query, values)
        self.connection.commit()
        print("Product successfully updated")

    def delete_product(self, product_id):
        query = "DELETE FROM products WHERE id = ?"
        values = (product_id,)
        cursor = self.connection.cursor()
        cursor.execute(query, values)
        self.connection.commit()
        print("Product successfully deleted")
