from fastapi import FastAPI, Depends
import sqlite3
from pydantic import BaseModel

app = FastAPI(
    title="BlockHouseTask API",
    description="This API allows users to manage trade orders, including creation, retrieval, and deletion.",
    version="1.0.0",
    contact={
        "name": "Kyle Dsouza",
        "email": "kyle.dsouza.official@gmail.com"
    }
)

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

@app.post("/orders", summary="Create a new trade order", response_description="Order created successfully")
async def create_order(order: Order, db: sqlite3.Connection = Depends(get_db)):
    """
    Create a new trade order.

    - **symbol**: The stock symbol (e.g., "KMD")
    - **price**: The price per unit of the stock
    - **quantity**: Number of units to trade
    - **order_type**: Type of order, either "buy" or "sell"

    **Returns:**
    - A confirmation message indicating the order has been created.
    """
    cursor = db.cursor()
    cursor.execute('''
        INSERT INTO orders (symbol, price, quantity, order_type)
        VALUES (?, ?, ?, ?)
    ''', (order.symbol, order.price, order.quantity, order.order_type))
    db.commit()
    return {"message": "Order created"}

@app.get("/orders", summary="Retrieve all trade orders", response_description="List of all trade orders")
async def get_orders(db: sqlite3.Connection = Depends(get_db)):
    """
    Retrieve all trade orders.

    **Returns:**
    - A list of all trade orders stored in the database.
    """
    cursor = db.cursor()
    cursor.execute('SELECT * FROM orders')
    orders = cursor.fetchall()
    return {"orders": [dict(order) for order in orders]}  # Convert rows to JSON-friendly format

@app.delete("/orders", summary="Delete all trade orders", response_description="All orders deleted successfully")
async def clear_orders(db: sqlite3.Connection = Depends(get_db)):
    """
    Delete all trade orders from the database.

    **Returns:**
    - A confirmation message indicating all orders have been deleted.
    """
    cursor = db.cursor()
    cursor.execute('DELETE FROM orders')  # Delete all rows
    db.commit()
    return {"message": "All orders deleted"}

@app.delete("/drop-table", summary="Drop and recreate orders table", response_description="Orders table reset")
async def drop_table(db: sqlite3.Connection = Depends(get_db)):
    """
    Drop the existing orders table and recreate it.

    **Returns:**
    - A confirmation message indicating the table has been reset.
    """
    cursor = db.cursor()
    cursor.execute('DROP TABLE IF EXISTS orders')
    db.commit()
    create_table()
    return {"message": "Table deleted and recreated"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
