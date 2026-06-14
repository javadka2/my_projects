import sqlite3
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import database
from datetime import datetime

database.create_tables()

app = FastAPI()

class ProductCreate(BaseModel):
    name: str
    price: int
    quantity: int

class ProductResponse(BaseModel):
    id: int
    name: str
    price: int
    quantity: int 

class SaleCreate(BaseModel):
    product_name: str
    quantity: int
    customer_name: str
    customer_phone: str

class CustomerResponse(BaseModel):
    id: int
    name: str
    phone: str
    created_at: str   
    purchase_history: str

@app.get("/")
def home():
    return {"message": "Bookstore API with SQLite"}

@app.get("/products", response_model=list[ProductResponse])
def get_products():
    conn = database.get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, price, quantity FROM products")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

@app.post("/products", response_model=ProductResponse)
def add_product(product: ProductCreate):
    conn = database.get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO products (name, price, quantity) VALUES (?, ?, ?)",
        (product.name, product.price, product.quantity)
    )
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return ProductResponse(id=new_id, name=product.name, price=product.price, quantity=product.quantity)

@app.get("/products/{product_id}", response_model=ProductResponse)
def get_product(product_id: int):
    conn = database.get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, price, quantity FROM products WHERE id = ?", (product_id,))
    row = cursor.fetchone()
    conn.close()
    if row is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return dict(row)

@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    conn = database.get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
    conn.commit()
    deleted = cursor.rowcount
    conn.close()
    if deleted == 0:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": f"Product {product_id} deleted"}

@app.post("/sales")
def sale_product(sale: SaleCreate):
    conn = database.get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id FROM customers WHERE phone = ?", (sale.customer_phone,))
        row = cursor.fetchone()
        if row:
            customer_id = row["id"]
        else:
            normalized_name = sale.customer_name.strip().title()
            cursor.execute(
                "INSERT INTO customers (name, phone) VALUES (?, ?)",
                (normalized_name, sale.customer_phone)
            )
            conn.commit()
            customer_id = cursor.lastrowid
    except sqlite3.IntegrityError:
        conn.close()
        raise HTTPException(status_code=400, detail="Phone number already exists")
    
    normal_name = sale.product_name.strip().title()
    cursor.execute("SELECT price, quantity FROM products WHERE name = ?", (normal_name,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail="Product not found")
    price, available_qty = row
    if available_qty < sale.quantity:
        conn.close()
        raise HTTPException(status_code=400, detail="Insufficient stock")
    
    total = sale.quantity * price
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    cursor.execute(
        "INSERT INTO sales (product_name, customer_id, quantity_sold, total_price) VALUES (?, ?, ?, ?)",
        (normal_name, customer_id, sale.quantity, total)
    )
    
    cursor.execute(
        "UPDATE products SET quantity = quantity - ? WHERE name = ?",
        (sale.quantity, normal_name)
    )
    
    cursor.execute("SELECT purchase_history FROM customers WHERE id = ?", (customer_id,))
    old_history = cursor.fetchone()[0] or ""  
    
    new_entry = f"{normal_name}:{sale.quantity}:{now_str};"
    
    if old_history and not old_history.endswith(";"):
        old_history += ";"
    updated_history = old_history + new_entry
    cursor.execute(
        "UPDATE customers SET purchase_history = ? WHERE id = ?",
        (updated_history, customer_id)
    )
    
    conn.commit()
    conn.close()
    
    return {
        "message": "Sale recorded",
        "total_price": total,
        "customer_id": customer_id,
        "purchase_history_updated": updated_history
    }

@app.get("/customers")
def get_all_customers():
    conn = database.get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, phone, created_at, purchase_history FROM customers")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

@app.get("/customers/{customer_phone}",response_model=CustomerResponse)
def get_customer(customer_phone: str):
    conn = database.get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, phone, created_at, purchase_history FROM customers WHERE phone = ?", (customer_phone,))
    row = cursor.fetchone()
    conn.close()
    if row is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return dict(row)

@app.get("/reports/top-products")
def get_top_product():
    conn = database.get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT product_id, SUM(quantity_sold) as total_sold
        FROM sales
        GROUP BY product_id
        ORDER BY total_sold DESC
        LIMIT 1
    """)
    top = cursor.fetchone()
    conn.close()
    if not top:
        raise HTTPException(status_code=404, detail="No sales found")
    product_id, total_sold = top
    conn = database.get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, price FROM products WHERE id = ?", (product_id,))
    product = cursor.fetchone()
    conn.close()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return {
        "product_id": product["id"],
        "product_name": product["name"],
        "product_price": product["price"],
        "total_quantity_sold": total_sold
    }