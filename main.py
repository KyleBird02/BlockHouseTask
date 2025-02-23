from fastapi import FastAPI, Depends
import sqlite3
from pydantic import BaseModel

app = FastAPI()

# Create orders table if it doesn't exist
def create_table():
    with sqlite3.connect('orders.db', check_same_thread=False) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                symbol TEXT NOT NULL,
                price FLOAT NOT NULL,
                quantity INTEGER NOT NULL,
                order_type TEXT NOT NULL
            )
        ''')
        conn.commit()

create_table()  # Ensure table exists at startup

# Dependency to get a database connection
def get_db():
    conn = sqlite3.connect('orders.db', check_same_thread=False)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

class Order(BaseModel):
    symbol: str
    price: float
    quantity: int
    order_type: str

@app.post("/orders")
async def create_order(order: Order, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute('''
        INSERT INTO orders (symbol, price, quantity, order_type)
        VALUES (?, ?, ?, ?)
    ''', (order.symbol, order.price, order.quantity, order.order_type))
    db.commit()
    return {"message": "Order created"}

@app.get("/orders")
async def get_orders(db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute('SELECT * FROM orders')
    orders = cursor.fetchall()
    return {"orders": [dict(order) for order in orders]}  # Convert rows to JSON-friendly format

@app.delete("/orders")
async def clear_orders(db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute('DELETE FROM orders')  # Delete all rows
    db.commit()
    return {"message": "All orders deleted"}

@app.delete("/drop-table")
async def drop_table(db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute('DROP TABLE orders')
    db.commit()
    create_table()  
    return {"message": "Table deleted and recreated"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)