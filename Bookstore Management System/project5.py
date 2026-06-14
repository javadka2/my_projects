import pandas as pd
import os
from datetime import datetime

PRODUCTS_FILE = 'products.csv'
CUSTOMERS_FILE = 'customers.csv'
SALES_FILE = 'sales.csv'

def load_data(filename):
    if not os.path.exists(filename):
        return pd.DataFrame()
    try:
        return pd.read_csv(filename)
    except pd.errors.EmptyDataError:
        return pd.DataFrame()

def save_data(df, filename):
    df.to_csv(filename, index=False, encoding='utf-8-sig') 

def get_next_id(df, id_column, prefix):
    if df.empty or id_column not in df.columns or df[id_column].isnull().all():
        return f"{prefix}001"
    
    max_num = 0
    for index_val in df[id_column]:
        if isinstance(index_val, str) and index_val.startswith(prefix):
            try:
                num = int(index_val[len(prefix):])
                if num > max_num:
                    max_num = num
            except ValueError:
                continue
    return f"{prefix}{max_num + 1:03d}"

def display_products():
    products_df = load_data(PRODUCTS_FILE)
    if products_df.empty:
        print("\nNo products found.")
        return
    
    print("\n--- Product List ---")
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 1000)
    pd.set_option('display.colheader_justify', 'center')
    pd.set_option('display.max_colwidth', 50)
    
    if 'product_id' in products_df.columns and 'name' in products_df.columns and 'quantity' in products_df.columns and 'selling_price' in products_df.columns:
        print(products_df[['product_id', 'name', 'quantity', 'selling_price']].to_string(index=False))
    else:
        print("Required product columns not found.")
    print("--------------------")

def add_product():
    products_df = load_data(PRODUCTS_FILE)
    
    product_id = get_next_id(products_df, 'product_id', 'P')
    name = input("Product Name: ")
    while True:
        try:
            quantity = int(input("Quantity in stock: "))
            if quantity < 0:
                print("Quantity cannot be negative.")
                continue
            break
        except ValueError:
            print("Please enter a valid integer for quantity.")
    while True:
        try:
            purchase_price = int(input("Purchase Price (currency): "))
            if purchase_price < 0:
                print("Purchase price cannot be negative.")
                continue
            break
        except ValueError:
            print("Please enter a valid integer for purchase price.")
    while True:
        try:
            selling_price = int(input("Selling Price (currency): "))
            if selling_price < 0:
                print("Selling price cannot be negative.")
                continue
            break
        except ValueError:
            print("Please enter a valid integer for selling price.")

    new_product = pd.DataFrame([{
        'product_id': product_id,
        'name': name,
        'quantity': quantity,
        'purchase_price': purchase_price,
        'selling_price': selling_price
    }])
    
    if products_df.empty:
        products_df = new_product
    else:
        products_df = pd.concat([products_df, new_product], ignore_index=True)
        
    save_data(products_df, PRODUCTS_FILE)
    print(f"Product '{name}' with ID '{product_id}' added successfully.")

def update_product():
    products_df = load_data(PRODUCTS_FILE)
    if products_df.empty:
        print("\nNo products to update.")
        return

    product_id_to_update = input("Enter the product ID to update: ")
    
    idx = products_df.index[products_df['product_id'] == product_id_to_update].tolist()

    if not idx:
        print(f"Product with ID '{product_id_to_update}' not found.")
        return

    idx = idx[0] 

    print(f"\nCurrent product details: {products_df.loc[idx, 'name']}")
    
    current_quantity = products_df.loc[idx, 'quantity']
    current_purchase_price = products_df.loc[idx, 'purchase_price']
    current_selling_price = products_df.loc[idx, 'selling_price']

    while True:
        new_quantity_str = input(f"New quantity in stock (current: {current_quantity}) - Press Enter to keep current: ")
        if not new_quantity_str:
            break
        try:
            new_quantity = int(new_quantity_str)
            if new_quantity < 0:
                print("Quantity cannot be negative.")
            else:
                products_df.loc[idx, 'quantity'] = new_quantity
                break
        except ValueError:
            print("Please enter a valid integer for quantity.")

    while True:
        new_purchase_price_str = input(f"New purchase price (current: {current_purchase_price}) - Press Enter to keep current: ")
        if not new_purchase_price_str:
            break
        try:
            new_purchase_price = int(new_purchase_price_str)
            if new_purchase_price < 0:
                print("Purchase price cannot be negative.")
            else:
                products_df.loc[idx, 'purchase_price'] = new_purchase_price
                break
        except ValueError:
            print("Please enter a valid integer for purchase price.")

    while True:
        new_selling_price_str = input(f"New selling price (current: {current_selling_price}) - Press Enter to keep current: ")
        if not new_selling_price_str:
            break
        try:
            new_selling_price = int(new_selling_price_str)
            if new_selling_price < 0:
                print("Selling price cannot be negative.")
            else:
                products_df.loc[idx, 'selling_price'] = new_selling_price
                break
        except ValueError:
            print("Please enter a valid integer for selling price.")
            
    save_data(products_df, PRODUCTS_FILE)
    print(f"Details for product '{products_df.loc[idx, 'name']}' updated successfully.")

def search_product():
    products_df = load_data(PRODUCTS_FILE)
    if products_df.empty:
        print("\nNo products found.")
        return
    
    search_query = input("Enter product ID or part of the product name to search: ").lower()
    
    results = products_df[
        products_df['product_id'].str.lower().str.contains(search_query, na=False) |
        products_df['name'].str.lower().str.contains(search_query, na=False)
    ]
    
    if results.empty:
        print("No products found matching your search criteria.")
    else:
        print("\n--- Search Results ---")
        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', 1000)
        pd.set_option('display.colheader_justify', 'center')
        pd.set_option('display.max_colwidth', 50)
        if 'product_id' in results.columns and 'name' in results.columns and 'quantity' in results.columns and 'purchase_price' in results.columns and 'selling_price' in results.columns:
            print(results[['product_id', 'name', 'quantity', 'purchase_price', 'selling_price']].to_string(index=False))
        else:
            print("Required columns for search results not found.")
        print("--------------------")

def display_customers():
    customers_df = load_data(CUSTOMERS_FILE)
    if customers_df.empty:
        print("\nNo customers found.")
        return
    
    print("\n--- Customer List ---")
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 1000)
    pd.set_option('display.colheader_justify', 'center')
    pd.set_option('display.max_colwidth', 50)
    if 'phone' in customers_df.columns and 'name' in customers_df.columns:
        print(customers_df[['phone', 'name']].to_string(index=False))
    else:
        print("Required customer columns not found.")
    print("--------------------")

def search_customer():
    customers_df = load_data(CUSTOMERS_FILE)
    if customers_df.empty:
        print("\nNo customers found.")
        return
    
    phone_number = input("Enter customer phone number: ").strip()
    customers_df['phone'] = customers_df['phone'].astype(str)
    customer_data = customers_df[customers_df['phone'] == phone_number]

    
    if customer_data.empty:
        print(f"Customer with phone number '{phone_number}' not found.")
        return
    else:
        print("\n--- Customer Details ---")
        
        phone = customer_data.iloc[0].get('phone', 'N/A')
        name = customer_data.iloc[0].get('name', 'N/A')
        purchase_history_str = customer_data.iloc[0].get('purchase_history', '')

        print(f"Phone: {phone}")
        print(f"Name: {name}")
        
        if pd.notna(purchase_history_str) and purchase_history_str.strip():
            print("\nPurchase History:")
            items = purchase_history_str.split(';')
            products_df_for_history = load_data(PRODUCTS_FILE)
            for item in items:
                if ':' in item:
                    try:
                        prod_id, qty = item.split(':', 1)
                        product_name = "Unknown Product"
                        if not products_df_for_history.empty and prod_id in products_df_for_history['product_id'].values:
                            product_name = products_df_for_history.loc[products_df_for_history['product_id'] == prod_id, 'name'].iloc[0]
                        print(f"- {product_name} (ID: {prod_id}): {qty} units")
                    except ValueError:
                        print(f"- Invalid history item: {item}")
                else:
                    print(f"- Invalid history item: {item}")
        else:
            print("No purchase history recorded for this customer.")
        
        print("--------------------")

def record_sale():
    products_df = load_data(PRODUCTS_FILE)
    customers_df = load_data(CUSTOMERS_FILE)
    sales_df = load_data(SALES_FILE)

    if products_df.empty:
        print("Error: No products registered in the system. Please add products first.")
        return

    sale_items = []
    total_amount = 0
    
    print("\n--- Record Customer Sale ---")
    print("Please enter purchased items. Type 'done' to finish the purchase.")

    while True:
        product_input = input("Enter Product ID or Name (or 'done' to finish): ").strip()
        if product_input.lower() == 'done':
            break
        
        product_match = products_df[
            (products_df['product_id'].str.lower() == product_input.lower()) |
            (products_df['name'].str.lower().str.contains(product_input.lower(), na=False))
        ]

        if product_match.empty:
            print("Product with this ID or Name not found. Please try again.")
            continue
        
        product_info = product_match.iloc[0]
        product_id = product_info['product_id']
        product_name = product_info['name']
        available_quantity = product_info['quantity']
        selling_price = product_info['selling_price']

        if available_quantity == 0:
            print(f"Sorry, product '{product_name}' is out of stock.")
            continue

        while True:
            try:
                quantity_to_buy_str = input(f"Quantity to buy for '{product_name}' (available: {available_quantity}): ")
                if not quantity_to_buy_str: continue
                quantity_to_buy = int(quantity_to_buy_str)
                if quantity_to_buy <= 0:
                    print("Quantity must be positive.")
                elif quantity_to_buy > available_quantity:
                    print(f"Insufficient stock. You can buy a maximum of {available_quantity} units.")
                else:
                    break
            except ValueError:
                print("Please enter a valid integer.")
        
        item_total_price = quantity_to_buy * selling_price
        sale_items.append({'product_id': product_id, 'quantity': quantity_to_buy, 'price_per_item': selling_price})
        total_amount += item_total_price
        
        products_df.loc[products_df['product_id'] == product_id, 'quantity'] -= quantity_to_buy
        print(f"'{product_name}' ({quantity_to_buy} units) added to cart. Current total: {total_amount} currency.")

    if not sale_items:
        print("No items selected for purchase. Returning to main menu.")
        return

    print(f"\nTotal amount due: {total_amount} currency.")

    customer_phone = ""
    customer_name = ""
    customer_purchase_history = ""
    is_new_customer = False

    while not customer_phone:
        customer_phone_input = input("Customer Phone Number (for record/lookup - Enter for Guest): ").strip()
        if not customer_phone_input:
            customer_phone = "" 
            customer_name = "Guest"
            print("Sale will be recorded as a guest purchase.")
            break

        if not customer_phone_input.startswith('09') or len(customer_phone_input) != 11 or not customer_phone_input.isdigit():
            print("Invalid phone number format. Please enter a valid 11-digit number starting with 09.")
            continue
            
        customer_phone = customer_phone_input
        customer_data = customers_df[customers_df['phone'] == customer_phone]
        
        if not customer_data.empty:
            customer_name = customer_data.iloc[0]['name']
            customer_purchase_history = customer_data.iloc[0]['purchase_history']
            print(f"Customer found: {customer_name}")
        else:
            is_new_customer = True
            customer_name = input("This is a new customer. Enter customer name: ").strip()
            if not customer_name:
                customer_name = "Unknown Customer"
            print(f"New customer: {customer_name}")
            break

    updated_history_items_dict = {}
    if pd.notna(customer_purchase_history) and customer_purchase_history.strip():
        try:
            items = customer_purchase_history.split(';')
            for item in items:
                if ':' in item:
                    prod_id, qty_str = item.split(':', 1)
                    updated_history_items_dict[prod_id] = updated_history_items_dict.get(prod_id, 0) + int(qty_str)
        except Exception as e:
            print(f"Error processing existing purchase history: {e}")

    for item in sale_items:
        prod_id = item['product_id']
        qty = item['quantity']
        updated_history_items_dict[prod_id] = updated_history_items_dict.get(prod_id, 0) + qty

    customer_purchase_history_updated = ";".join([f"{pid}:{q}" for pid, q in updated_history_items_dict.items()])

    if customer_phone: 
        if is_new_customer:
            new_customer = pd.DataFrame([{
                'phone': customer_phone,
                'name': customer_name,
                'purchase_history': customer_purchase_history_updated
            }])
            if customers_df.empty:
                customers_df = new_customer
            else:
                customers_df = pd.concat([customers_df, new_customer], ignore_index=True)
        else:
            customers_df.loc[customers_df['phone'] == customer_phone, 'name'] = customer_name
            customers_df.loc[customers_df['phone'] == customer_phone, 'purchase_history'] = customer_purchase_history_updated

    sale_id = get_next_id(sales_df, 'sale_id', 'S')
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    import json
    items_json = json.dumps([{"product_id": item['product_id'], "quantity": item['quantity']} for item in sale_items])

    new_sale = pd.DataFrame([{
        'sale_id': sale_id,
        'timestamp': timestamp,
        'customer_phone': customer_phone if customer_phone else "Guest",
        'customer_name': customer_name,
        'items': items_json,
        'total_amount': total_amount
    }])
    
    if sales_df.empty:
        sales_df = new_sale
    else:
        sales_df = pd.concat([sales_df, new_sale], ignore_index=True)

    save_data(products_df, PRODUCTS_FILE)
    save_data(customers_df, CUSTOMERS_FILE)
    save_data(sales_df, SALES_FILE)
    
    print("\n--- Sale Summary ---")
    print(f"Sale ID: {sale_id}")
    print(f"Timestamp: {timestamp}")
    print(f"Customer: {customer_name} ({customer_phone if customer_phone else 'Guest'})")
    print("Items Purchased:")
    for item in sale_items:
        product_name = "Unknown Product"
        product_row = products_df[products_df['product_id'] == item['product_id']]
        if not product_row.empty:
            product_name = product_row.iloc[0]['name']
        print(f"- {product_name} (ID: {item['product_id']}): {item['quantity']} units x {item['price_per_item']} currency = {item['quantity'] * item['price_per_item']} currency")
    print(f"Total Amount: {total_amount} currency")
    print("Sale recorded successfully and product stock updated.")

def display_menu():
    print("\n===== Main Menu =====")
    print("1. Display Products")
    print("2. Add New Product")
    print("3. Update Product")
    print("4. Search Product")
    print("5. Record Customer Sale")
    print("6. Display Customers")
    print("7. Search Customer")
    print("8. Exit")
    print("=====================")

def main():
    if not os.path.exists(PRODUCTS_FILE):
        pd.DataFrame(columns=['product_id', 'name', 'quantity', 'purchase_price', 'selling_price']).to_csv(PRODUCTS_FILE, index=False, encoding='utf-8-sig')
    if not os.path.exists(CUSTOMERS_FILE):
        pd.DataFrame(columns=['phone', 'name', 'purchase_history']).to_csv(CUSTOMERS_FILE, index=False, encoding='utf-8-sig')
    if not os.path.exists(SALES_FILE):
        pd.DataFrame(columns=['sale_id', 'timestamp', 'customer_phone', 'customer_name', 'items', 'total_amount']).to_csv(SALES_FILE, index=False, encoding='utf-8-sig')

    while True:
        display_menu()
        choice = input("Please select an option: ")

        if choice == '1':
            display_products()
        elif choice == '2':
            add_product()
        elif choice == '3':
            update_product()
        elif choice == '4':
            search_product()
        elif choice == '5':
            record_sale()
        elif choice == '6':
            display_customers()
        elif choice == '7':
            search_customer()
        elif choice == '8':
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()