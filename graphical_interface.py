from tkinter import *
from tkinter import ttk, messagebox
import database

# Colors
blue_light = "#6BECFF"
bg_dark = "#1E1E1E"
turquoise = "#00FFB2"

# Fonts
font_title = ("Helvetica", 24, "bold")
font_text = ("Helvetica", 14)

# Root window
root = Tk()
root.title("Product management")
root.resizable(False, False)
root.configure(background=bg_dark, padx=30)

# Images
laurel_left = PhotoImage(file="media/laurel_left.png")
laurel_right = PhotoImage(file="media/laurel_right.png")

# My theme
ttk.Style().theme_create("my_theme", parent="alt", settings={
    "TLabel": {"configure": {"background": bg_dark, "foreground": "white", "font": font_text}},
    "TEntry": {
        "configure": {"fieldbackground": blue_light, "foreground": "black", "font": font_text, "justify": "center"}},
    "TButton": {"configure": {"background": "#6BECFF", "foreground": "black", "font": font_text, "anchor": "center"}},
    "TFrame": {"configure": {"background": bg_dark}},
    "Treeview": {
        "configure": {"background": bg_dark, "foreground": "white", "font": font_text, "rowheight": 30,
                      "bordercolor": "gray", "fieldbackground": bg_dark}
    },
    "Treeview.Heading": {"configure": {"background": turquoise, "foreground": "black", "font": font_text}},
})
ttk.Style().theme_use("my_theme")

# Variables
model_var = StringVar()
name_var = StringVar()
brand_var = StringVar()
price_var = StringVar()
list_all_products = []
product_repository = database.Product_repository()


# Function to clear the entries
def clear_entries():
    model_var.set("")
    name_var.set("")
    brand_var.set("")
    price_var.set("")


# Function to create a new product
def create_product():
    model = model_var.get()
    name = name_var.get()
    brand = brand_var.get()
    price = price_var.get()

    # If all fields are filled in then create the product
    if model and name and brand and price:
        try:
            product_repository.create_product(model, name, brand, price)
            # Insertar nueva fila en la tabla
            load_all_products()
            clear_entries()
            messagebox.showinfo("Success", "Product successfully created")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create product: {str(e)}")
    else:
        messagebox.showerror("Error", "All fields must be filled")


# Function to load all products into the table and save them in a list
def load_all_products():
    global list_all_products
    list_all_products = product_repository.get_all_products()
    # Clear the treeview
    for j in table_products.get_children():
        table_products.delete(j)

    # Insert products into the treeview
    for product in list_all_products:
        table_products.insert("", END, values=(product.id, product.model, product.name, product.brand, product.price))


# Function to update a product
def update_product():
    selected_row_id = table_products.selection()
    if selected_row_id:
        selected_row = table_products.item(selected_row_id)
        product_id = selected_row['values'][0]
        model = model_var.get()
        name = name_var.get()
        brand = brand_var.get()
        price = price_var.get()
        # If all fields are filled in then update the product
        if model and name and brand and price:
            try:
                product_repository.update_product(product_id, model, name, brand, price)
                clear_entries()
                load_all_products()
                messagebox.showinfo("Success", "Product successfully updated")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update product: {str(e)}")
        else:
            messagebox.showerror("Error", "All fields must be filled")
    else:
        messagebox.showerror("Error", "You must select a product to delete")


# Function to delete a product
def delete_product():
    selected_row_id = table_products.selection()
    if selected_row_id:
        selected_row = table_products.item(selected_row_id)
        product_id = selected_row['values'][0]
        confirm = messagebox.askyesno("Confirmation", "Are you sure you want to delete this product?")
        if confirm:
            product_repository.delete_product(product_id)
            load_all_products()
            clear_entries()
            messagebox.showinfo("Success", "Product successfully deleted")
    else:
        messagebox.showerror("Error", "You must select a product to delete")


def on_treeview_select(event):
    selected_row_id = table_products.selection()
    if selected_row_id:
        selected_row = table_products.item(selected_row_id)
        model_var.set(selected_row['values'][1])
        name_var.set(selected_row['values'][2])
        brand_var.set(selected_row['values'][3])
        price_var.set(selected_row['values'][4])
    table_products.tag_configure("selected", background=turquoise, foreground="black")
    for item in table_products.get_children():
        tags = () if item not in selected_row_id else ("selected",)
        table_products.item(item, tags=tags)


def on_heading_click(col):
    if col == "Id":
        sort_treeview(table_products, 0)
    elif col == "Model":
        sort_treeview(table_products, 1)
    elif col == "Name":
        sort_treeview(table_products, 2)
    elif col == "Brand":
        sort_treeview(table_products, 3)
    elif col == "Price":
        sort_treeview(table_products, 4)


def sort_treeview(treeview, column):
    if column == 4:
        data = [(float(treeview.set(child, column)), child) for child in treeview.get_children('')]
        data.sort()

        for indx, item in enumerate(data):
            treeview.move(item[1], '', indx)
    else:
        data = [(treeview.set(child, column), child) for child in treeview.get_children('')]
        data.sort()

        for indx, item in enumerate(data):
            treeview.move(item[1], '', indx)


# Header --------------------------------------------------------------------------------------------------
header = ttk.Frame(root, padding=(10, 10))

label_header_title = ttk.Label(header, text="Product management", font=font_title)
label_header_title.configure(anchor="center")
label_header_icon_left = ttk.Label(header, image=laurel_left)
label_header_icon_right = ttk.Label(header, image=laurel_right)

label_header_icon_left.grid(row=0, column=0, sticky="e")
label_header_title.grid(row=0, column=1, sticky="ew")
label_header_icon_right.grid(row=0, column=2, sticky="w")

header.columnconfigure(0, weight=1)
header.columnconfigure(1, weight=1)
header.columnconfigure(2, weight=1)

# Form product ----------------------------------------------------------------------------------------------
# Widgets
frame_form = ttk.Frame(root, padding=(10, 0))
label_title = ttk.Label(frame_form, text="Product", font=("Helvetica", 16, "bold"))
label_model = ttk.Label(frame_form, text="Model:", anchor="w")
label_name = ttk.Label(frame_form, text="Name:", anchor="w")
label_brand = ttk.Label(frame_form, text="Brand:", anchor="w")
label_price = ttk.Label(frame_form, text="Price:", anchor="w")
entry_model = ttk.Entry(frame_form, textvariable=model_var, width=40, font=font_text, justify="center")
entry_name = ttk.Entry(frame_form, textvariable=name_var, width=40, font=font_text, justify="center")
entry_brand = ttk.Entry(frame_form, textvariable=brand_var, width=40, font=font_text, justify="center")
entry_price = ttk.Entry(frame_form, textvariable=price_var, width=40, font=font_text, justify="center")
btn_create_product = ttk.Button(frame_form, text="Create product", command=create_product)
btn_update_product = ttk.Button(frame_form, text="Update product", command=update_product)
btn_delete_product = ttk.Button(frame_form, text="Delete product", command=delete_product)
btn_clear_entries = ttk.Button(frame_form, text="Clear entries", command=clear_entries)

# Form design
label_title.grid(row=0, column=0, columnspan=2, pady=(0, 5))
label_model.grid(row=1, column=0, padx=(0, 5), sticky="w")
label_name.grid(row=2, column=0, padx=(0, 5), sticky="w")
label_brand.grid(row=3, column=0, padx=(0, 5), sticky="w")
label_price.grid(row=4, column=0, padx=(0, 5), sticky="w")
entry_model.grid(row=1, column=1, sticky="w")
entry_name.grid(row=2, column=1, sticky="w")
entry_brand.grid(row=3, column=1, sticky="w")
entry_price.grid(row=4, column=1, sticky="w")
btn_create_product.grid(row=5, column=0, columnspan=2, pady=(15, 0), sticky="ew")
btn_update_product.grid(row=6, column=0, columnspan=2, pady=(15, 0), sticky="ew")
btn_delete_product.grid(row=7, column=0, columnspan=2, pady=(15, 0), sticky="ew")
btn_clear_entries.grid(row=8, column=0, columnspan=2, pady=(15, 0), sticky="ew")

for i in range(1, 5):
    frame_form.grid_rowconfigure(i, pad=10)

# Table ---------------------------------------------------------------------------------------------------
frame_table = ttk.Frame(root)
columns = ("Id", "Model", "Name", "Brand", "Price")
table_products = ttk.Treeview(frame_table, columns=columns, show="headings", selectmode="browse", height=11)
table_products.bind("<<TreeviewSelect>>", on_treeview_select)

# Configure headings
for col in columns:
    table_products.heading(col, text=col, command=lambda c=col: on_heading_click(c))

# Configure columns
for col in columns:
    table_products.column(col, width=150, anchor="center")

table_products.grid(row=0, column=0, sticky="nsew")

load_all_products()

# Confirgurar posición de los widgets -----------------------------------------------
header.grid(row=0, column=0, columnspan=2, sticky="ew")
frame_form.grid(row=1, column=0, sticky="nsew", pady=(0, 30))
frame_table.grid(row=1, column=1, sticky="nsew", pady=(0, 30))

# Iniciar la aplicación
root.mainloop()
