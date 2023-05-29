import ttkbootstrap as ttk
import tkinter.messagebox as messagebox
import ttkbootstrap.dialogs
from ttkbootstrap.constants import *
from ttkbootstrap.tooltip import ToolTip
from ttkbootstrap.tableview import Tableview


# Pizza menu
pizza_menu = [
    {"name": "Margherita Pizza", "sizes": ["Small", "Medium", "Large"], "prices": [99, 199, 399]},
    {"name": "Cheese n Corn Pizza", "sizes": ["Small", "Medium", "Large"], "prices": [169, 309, 499]},
    {"name": "Cheese n Tomato Pizza", "sizes": ["Small", "Medium", "Large"], "prices": [169, 309, 499]},
    {"name": "Double Cheese Margherita Pizza", "sizes": ["Small", "Medium", "Large"], "prices": [189, 339, 539]},
    {"name": "Fresh Veggie Pizza", "sizes": ["Small", "Medium", "Large"], "prices": [189, 339, 539]},
    {"name": "Farmhouse Pizza", "sizes": ["Small", "Medium", "Large"], "prices": [229, 399, 599]},
    {"name": "Peppy Paneer Pizza", "sizes": ["Small", "Medium", "Large"], "prices": [229, 399, 599]},
    {"name": "Veggie Paradise Pizza", "sizes": ["Small", "Medium", "Large"], "prices": [229, 399, 599]},
    {"name": "Veg Extravaganza Pizza", "sizes": ["Small", "Medium", "Large"], "prices": [249, 459, 699]},
    {"name": "Cheese Dominator Pizza", "sizes": ["Small", "Medium", "Large"], "prices": [319, 579, 839]},
    {"name": "Cheese Pizza", "sizes": ["Small", "Medium", "Large"], "prices": [319, 579, 839]},
    {"name": "Deluxe Veggie Pizza", "sizes": ["Small", "Medium", "Large"], "prices": [249, 459, 699]},
    {"name": "Paneer Makhani Pizza", "sizes": ["Small", "Medium", "Large"], "prices": [249, 459, 699]},
    {"name": "Indi Tandoori Pizza", "sizes": ["Small", "Medium", "Large"], "prices": [249, 459, 699]},
    {"name": "Achari Do Pyaza Pizza", "sizes": ["Small", "Medium", "Large"], "prices": [169, 309, 499]},
    {"name": "Pepper Barbecue Chicken Pizza", "sizes": ["Small", "Medium", "Large"], "prices": [229, 399, 599]},
    {"name": "Pepper Barbecue Chicken & Onion Pizza", "sizes": ["Small", "Medium", "Large"], "prices": [229, 399, 599]},
    {"name": "Chicken Sausage Pizza", "sizes": ["Small", "Medium", "Large"], "prices": [189, 339, 539]},
    {"name": "Chicken Golden Delight Pizza", "sizes": ["Small", "Medium", "Large"], "prices": [249, 459, 699]},
    {"name": "Non Veg Supreme Pizza", "sizes": ["Small", "Medium", "Large"], "prices": [319, 579, 839]},
    {"name": "Chicken Pepperoni Pizza", "sizes": ["Small", "Medium", "Large"], "prices": [399, 599, 899]},
    {"name": "Chicken Fiesta Pizza", "sizes": ["Small", "Medium", "Large"], "prices": [249, 459, 699]},
    {"name": "Indi Chicken Tikka Pizza", "sizes": ["Small", "Medium", "Large"], "prices": [319, 579, 839]},
    {"name": "Keema Do Pyaza Pizza ", "sizes": ["Small", "Medium", "Large"], "prices": [189, 339, 539]},

]

# toppings
pizza_toppings = {
    "Tomato": 30,
    "Black Olives": 40,
    "Capsicum": 25,
    "Onion": 25,
    "Sausage": 10,
    "Mushrooms": 30,
    "Pepperoni": 25,
    "Extra Cheese": 50,
    "Green Peppers": 30,
    "Bacon": 30,
    "Sweet Corn": 30
}

def on_pizza_selected(event):
    # Clear the previous selection
    size_combobox.set("")
    price_combobox.set("")

    # Get the selected pizza
    selected_pizza = pizza_combobox.get()

    # Find the selected pizza in the menu
    for pizza in pizza_menu:
        if pizza["name"] == selected_pizza:
            # Update the sizes dropdown
            size_combobox["values"] = pizza["sizes"]
            size_combobox["state"] = "readonly"
            break

def on_size_selected(event):
    # Get the selected pizza and size
    selected_pizza = pizza_combobox.get()
    selected_size = size_combobox.get()

    # Find the selected pizza in the menu
    for pizza in pizza_menu:
        if pizza["name"] == selected_pizza:
            # Find the index of the selected size
            size_index = pizza["sizes"].index(selected_size)

            # Update the price dropdown
            price_combobox.set(pizza["prices"][size_index])
            break

orders = []
global total_collection_value
total_collection_value = 0.0

def calculate_total():
    orders.clear()
    # Get the selected pizza, size, toppings, and offer status
    selected_pizza = pizza_combobox.get()
    selected_size = size_combobox.get()
    selected_toppings = [topping_var.get() for topping_var in topping_vars]
    offer_selected = offer_var.get()

    # Find the selected pizza in the menu
    pizza = next((item for item in pizza_menu if item["name"] == selected_pizza), None)

    # Calculate the total price
    price_index = pizza["sizes"].index(selected_size)
    base_price = pizza["prices"][price_index]
    topping_prices = [pizza_toppings[topping] for topping in selected_toppings if topping]
    total_price = base_price + sum(topping_prices)

    # Apply offer if selected
    if offer_selected:
        total_price *= 0.8  # 20% off

    # Update the receipt labels
    order_count.set(order_count.get() + 1)

    # Join selected toppings or display "No toppings"
    if selected_toppings:
        selected_toppings = [topping for topping in selected_toppings if topping != '']
        if selected_toppings:
            toppings_text = " ".join(selected_toppings)
        else:
            toppings_text = "No toppings"
    else:
        toppings_text = "No toppings"

    gst_amount = round(total_price * 0.18, 2)
    total_amount = round(total_price + gst_amount, 2)

    orders.append((
        f"{selected_pizza}",
        f"    {selected_size}",
        f"      {total_price:.2f}",
        f"{toppings_text}",
        f"    {gst_amount:.2f}",
        "  Yes " if offer_selected else "  No",
        f"      {total_amount:.2f}"
    ))
    saving_amount = orders.copy()
    # Insert the updated order items
    for i,order in enumerate(orders):
        dv.insert_row(index=i,values=order)
    dv.load_table_data()

    # Calculate total collection
    for total in saving_amount:
        global total_collection_value
        total_collection_value += float(total[6])  # Accumulate the total price (column index 2)
        t_collection.set(f"Total Collection: {total_collection_value:.2f} Rs")

    # orders.reverse()
    order_total.set(f"Total Orders: {order_count.get()}")


def clear_orders():
    # Clear the order details
    order_count.set(0)
    order_text.set("")
    order_total.set("Total Orders: 0")

def confirm_quit():
    response = messagebox.askokcancel("Exit Application", "Are you sure you want to exit?")
    if response:
        root.destroy()

# Create the main window
root = ttk.Window(themename="litera")
root.geometry("2100x1080+0+0")
root.title("PizzaHouse APP")
colors = root.style.colors

# Create labels
title_label = ttk.Label(root, text="Pizza Home App",bootstyle="danger",font=("Times New Roman", 26,'bold'))
title_label.grid(row=0, column=2, columnspan=2, pady=10,padx=50)

# Create dropdowns
pizza_label = ttk.Label(root, text="Select Pizza:",font=("Times New Roman", 13))
pizza_label.grid(row=1, column=0,columnspan=1, pady=10,padx=100,ipadx=100)

size_label = ttk.Label(root, text="Select Size:",font=("Times New Roman", 13))
size_label.grid(row=1, column=2,columnspan=1, pady=10,padx=100,ipadx=100)

price_label = ttk.Label(root, text="Price:",font=("Times New Roman", 13))
price_label.grid(row=1, column=4,columnspan=1, pady=10,padx=100,ipadx=100)

topping_label = ttk.Label(root, text="Select Toppings:",font=("Times New Roman", 18))
topping_label.grid(row=6, column=2,columnspan=2,pady=20,padx=30)

pizza_combobox = ttk.Combobox(root, values=[pizza["name"] for pizza in pizza_menu], state="readonly",
                              bootstyle="primary",font=("Times New Roman", 15))
pizza_combobox.grid(row=4, column=0,columnspan=1, pady=10,padx=30)
pizza_combobox.bind("<<ComboboxSelected>>", on_pizza_selected)

size_combobox = ttk.Combobox(root, state="disabled",font=("Times New Roman", 15),bootstyle="primary")
size_combobox.grid(row=4, column=2,columnspan=1, pady=10,padx=30)
size_combobox.bind("<<ComboboxSelected>>", on_size_selected)

price_combobox = ttk.Combobox(root, state="disabled",bootstyle="primary",font=("Times New Roman", 15))
price_combobox.grid(row=4, column=4,columnspan=1, pady=10,padx=10)

topping_vars = []
row_count = 7
col_count = 0
checkBoxStyle = ttk.Style()
checkBoxStyle.configure("TCheckbutton", font=("Helvetica", 12))
for i, topping in enumerate(pizza_toppings):
    var = ttk.StringVar()
    topping_checkbutton = ttk.Checkbutton(root, text=topping + "-"+str(pizza_toppings[topping]), variable=var, onvalue=topping, offvalue="",bootstyle="info")
    topping_checkbutton.grid(row=row_count, column=col_count, padx=100, pady=10,columnspan=3)
    topping_vars.append(var)

    col_count += 1
    if col_count == 4:
        row_count += 2
        col_count = 0

# styles of buttons
my_style = ttk.Style()
my_style.configure('my.TButton',font=("Times New Roman", 15))

# Create buttons
cancel_button = ttk.Button(root, text="Cancel", command=confirm_quit,style='my.TButton')
cancel_button.grid(row=18, column=0, pady=30,columnspan=2,ipadx=50)

order_button = ttk.Button(root, text="Make Order", command=calculate_total,style='my.TButton')
order_button.grid(row=18, column=2, pady=30,columnspan=2,ipadx=50)

generate_receipt_button = ttk.Button(root, text="Print Receipt", command=calculate_total,style='my.TButton')
generate_receipt_button.grid(row=18, column=4, pady=30,columnspan=2,ipadx=50)

offer_var = ttk.BooleanVar()
t_collection = ttk.StringVar()
t_collection.set("Total Collection: 0.00 Rs")

offer_checkbox = ttk.Checkbutton(root, text="Apply Offer (20% off)", variable=offer_var)
offer_checkbox.grid(row=19, column=0,columnspan=1,padx=30)

# Create order receipt
receipt_label = ttk.Label(root, text="Order Receipt",font=("Times New Roman", 15,'bold'))
receipt_label.grid(row=20, column=2, columnspan=1,padx=100)

# Create order receipt
total_collection = ttk.Label(root,textvariable=t_collection,font=("Times New Roman", 13))
total_collection.grid(row=19, column=3, columnspan=4,padx=100)

order_count = ttk.IntVar()
order_text = ttk.StringVar()
order_total = ttk.StringVar()

order_total.set("Total Orders: 0")

# OrderDetailsColumns = ("pizza_name","size","price","topping_name","gst(%)","any_offer","total")

order_total_label = ttk.Label(root, textvariable=order_total,font=("Times New Roman", 13))
order_total_label.grid(row=19, column=1, columnspan=3, padx=100,pady=10,ipadx=80)

OrderDetailsColumns = [
    {"text": "PizzaName", "stretch": True},
    {"text":"Size","stretch":False},
    {"text":"Price","stretch":False},
    {"text":"Toppings","stretch":True},
    {"text":"GST (18%)","stretch":True},
    {"text":"Today's Offer","stretch":False},
    {"text":"Total Price","stretch":True},
]  # Columns with Names and style

dv = ttk.tableview.Tableview(
    master=root,
    paginated=True,
    coldata=OrderDetailsColumns,
    rowdata=orders,
    searchable=True,
    bootstyle=INFO,
    height=8,
    stripecolor=(colors.light,""),
)
dv.grid(row=20,column=0,columnspan=6,pady=5,padx=50,ipadx=170,ipady=5)
dv.align_column_left() # Fit in current view
dv.align_heading_center()
# Run the main event loop
root.mainloop()

