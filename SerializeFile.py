import xml.etree.ElementTree as Et
from bs4 import BeautifulSoup

from Product import Product


def save_product(f, product):
    # Cargar el archivo XML existente si ya tiene datos
    try:
        tree = Et.parse(f)
        root = tree.getroot()
    except (FileNotFoundError, Et.ParseError):
        # Si el archivo no existe o está vacío, crear un nuevo árbol XML
        root = Et.Element("products")
        tree = Et.ElementTree(root)

    # Crear un nuevo elemento "product" dentro de "products"
    product_element = Et.SubElement(root, "product")

    # Añadir subelementos con los datos del producto
    Et.SubElement(product_element, "ID").text = str(product.id)
    Et.SubElement(product_element, "Name").text = product.name
    Et.SubElement(product_element, "Category").text = product.category
    Et.SubElement(product_element, "Price").text = str(product.price)

    # Guardar el árbol XML actualizado en el archivo
    tree.write(f)


def modify_product(file_path, updated_product):
    with open(file_path, 'r') as file:
        xml_content = file.read()

    soup = BeautifulSoup(xml_content, 'xml')
    products = soup.find_all('product')

    # Buscar el producto por su posición en el archivo y reemplazar sus datos
    for product in products:
        if int(product.find('ID').text) == updated_product.id:
            product.find('Name').replace_with(BeautifulSoup(f"<Name>{updated_product.name}</Name>", "xml").Name)
            product.find('Category').replace_with(
                BeautifulSoup(f"<Category>{updated_product.category}</Category>", "xml").Category)
            product.find('Price').replace_with(BeautifulSoup(f"<Price>{updated_product.price}</Price>", "xml").Price)

    # Guardar el archivo actualizado
    with open(file_path, 'w') as output_file:
        output_file.write(str(soup))


def read_products(file, product_list):
    # Leer el contenido del archivo XML
    with open(file, 'r') as file:
        xml_content = file.read()

    # Parsear el contenido XML con BeautifulSoup
    soup = BeautifulSoup(xml_content, 'xml')

    # Encontrar todos los elementos "product"
    products = soup.find_all('product')

    # Iterar sobre los elementos y agregar productos a la lista
    for product in products:
        product_list.append(Product(
            int(product.find('ID').text),
            product.find('Name').text,
            product.find('Category').text,
            float(product.find('Price').text)
        ))


def delete_product_by_id(file_path, product_id):
    # Leer el contenido del archivo XML
    with open(file_path, 'r') as file:
        xml_content = file.read()

    # Parsear el contenido XML con BeautifulSoup
    soup = BeautifulSoup(xml_content, 'xml')

    # Encontrar todos los elementos "product"
    products = soup.find_all('product')

    # Verificar si el producto con la 'ID' dada existe
    found_product = False
    for product in products:
        if int(product.find('ID').text) == product_id:
            product.extract()
            found_product = True
            break

    # Si se encontró el producto, actualizar las 'IDs' de los productos restantes
    if found_product:
        for product in products:
            current_id = int(product.find('ID').text)
            if current_id > product_id:
                product.find('ID').string = str(current_id - 1)

        # Guardar el archivo actualizado solo si se realizó algún cambio
        with open(file_path, 'w') as file:
            file.write(str(soup))
