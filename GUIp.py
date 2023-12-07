from SerializeFile import read_products, save_product, modify_product, delete_product_by_id
from Product import Product
import PySimpleGUI as Sg
import re

file_product = 'Product.xml'
lista_product = []
pattern_price = r'^\d+(\.\d{1,2})?$'


def add_product(lista_products, table_product_interfaz, object_product):
    """
    Función para agregar un nuevo producto a la lista y la tabla de la interfaz.

    Args:
        lista_products (list): Lista de productos.
        table_product_interfaz (list): Datos de la tabla de la interfaz.
        object_product (Product): Objeto de la clase Product a agregar.
    """
    lista_products.append(object_product)
    save_product(file_product, object_product)
    table_product_interfaz.append(
        [object_product.id, object_product.name, object_product.category, object_product.price])


def load_table_data(table_data):
    """
    Carga los datos de los productos en la tabla de la interfaz.

    Args:
        table_data (list): Datos de la tabla de la interfaz.
    """
    # Volver a leer los productos del archivo XML y actualizar las listas
    lista_product.clear()
    table_data.clear()
    read_products(file_product, lista_product)

    # Actualizar la tabla de la interfaz
    for p in lista_product:
        table_data.append([p.id, p.name, p.category, p.price])


def interfaz():
    """
    Función principal que muestra la interfaz de usuario y maneja los eventos.
    """
    font1, font2 = ('Arial', 14), ('Arial', 16)
    Sg.theme('DarkGrey5')
    Sg.set_options(font=font1)
    table_data = []
    row_to_update = []
    read_products(file_product, lista_product)
    for p in lista_product:
        table_data.append([p.id, p.name, p.category, p.price])

    layout = ([
                  [Sg.Push(), Sg.Text('Product CRUD'), Sg.Push()]] +
              [
                  [Sg.Text(text), Sg.Push(), Sg.Input(key=key)] for key, text in Product.fields.items() if
                  key != '-ID-'
              ] +
              [
                  [Sg.Push()] +
                  [Sg.Button(button) for button in ('Add', 'Delete', 'Modify', 'Clear')] +
                  [Sg.Push()],
                  [Sg.Table(values=table_data, headings=Product.headings, max_col_width=50, num_rows=10,
                            display_row_numbers=False, justification='center', enable_events=True,
                            enable_click_events=True, vertical_scroll_only=False,
                            select_mode=Sg.TABLE_SELECT_MODE_BROWSE,
                            expand_x=True, bind_return_key=True, key='-Table-')],
              ])
    Sg.theme('DarkGrey5')
    window = Sg.Window('Product Management with Files', layout, finalize=True)  # Cambia Customer por Product

    last_sort_col = None
    sort_order = 'asc'
    while True:
        event, values = window.read()
        if event == Sg.WIN_CLOSED:
            break
        if event == 'Add':
            valida = False
            # Validación del precio
            if re.match(pattern_price, values['-Price-']):
                valida = True
            if valida:
                # Agrega un nuevo producto a la lista y actualiza la tabla
                add_product(lista_product, table_data,
                            Product(len(lista_product), values['-Name-'], values['-Category-'], values['-Price-'])
                            )
                window['-Table-'].update(table_data)

        if event == 'Delete':
            if len(values['-Table-']) > 0:
                # Obtener la 'ID' del producto en la posición de la tabla
                id_product = table_data[values['-Table-'][0]][0]
                # Llama a la función delete_product_by_id para eliminar el producto del archivo XML
                delete_product_by_id(file_product, id_product)
                # Vuelve a cargar los datos de la tabla después de la eliminación
                load_table_data(table_data)
                window['-Table-'].update(table_data)

        if event == 'Clear':
            # Limpia los campos de entrada en la interfaz
            window['-Name-'].update('')
            window['-Category-'].update('')
            window['-Price-'].update('')

        if event == 'Modify':
            if values['-Table-']:
                id_product = table_data[values['-Table-'][0]][0]
                if 0 <= id_product < len(lista_product):
                    # Obtiene los valores actuales o ingresados en la interfaz
                    name = values['-Name-'] if values['-Name-'] != '' else table_data[values['-Table-'][0]][1]
                    category = values['-Category-'] if values['-Category-'] != '' else table_data[values['-Table-'][0]][
                        2]
                    price = values['-Price-'] if values['-Price-'] != '' else table_data[values['-Table-'][0]][3]
                    valida = False
                    # Validación del precio
                    if re.match(pattern_price, price):
                        valida = True
                    if valida:
                        # Actualiza el producto y vuelve a cargar los datos de la tabla
                        updated_product = Product(id_product, name, category, price)
                        modify_product(file_product, updated_product)
                        load_table_data(table_data)
                        window['-Table-'].update(table_data)

        if isinstance(event, tuple):
            print(event)
            if event[0] == '-Table-':
                if event[2][0] == -1:  # Se hizo clic en el encabezado de la tabla
                    col_num_clicked = event[2][1]
                    # Verifica si es la primera vez que se hace clic en un encabezado
                    if last_sort_col is not None:
                        # Cambia el orden al contrario (ascendente o descendente)
                        sort_order = 'desc' if sort_order == 'asc' else 'asc'

                    # Ordena la tabla según la columna y el estado de orden
                    table_data = sorted(table_data,
                                        key=lambda x: str(x[col_num_clicked]).lower() if isinstance(x[col_num_clicked],
                                                                                                    str) else x[
                                            col_num_clicked],
                                        reverse=(sort_order == 'desc'))
                    window['-Table-'].update(table_data)

                    # Actualiza last_sort_col
                    last_sort_col = col_num_clicked

        if event == '-Table-':
            if len(values['-Table-']) > 0:
                print("hola")
                # Obtiene la fila seleccionada en la tabla
                row = values['-Table-'][0]
                # Actualiza los campos de entrada con los valores de la fila seleccionada
                window['-Name-'].update(str(table_data[row][1]))
                window['-Category-'].update(str(table_data[row][2]))
                window['-Price-'].update(str(table_data[row][3]))

    window.close()


interfaz()
