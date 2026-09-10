from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse  # 👈 ADD THIS IMPORT
from pydantic import BaseModel
from typing import List

app = FastAPI()

Espresso_menu = {"Espresso": 2.00, "Macchiato": 2.50, "Latte": 2.50, "Breve": 2.50, "Mocha": 3.00, "Cappuccino": 3.00, "Americano": 2.00}
Hot_menu = {"Daily Dark Roast": 2.75, "Pour Over": 3.25, "Hot Chocolate": 3.00, "Steamer": 3.00, "Cafe Au Lait": 4.00}
Quick_bites_menu = {"Bagel": 2.00, "Muffin": 2.20, "Breakfast Sandwich": 4.75, "Croissant": 1.75, "Scones": 2.25}
merged_menu = Espresso_menu | Hot_menu | Quick_bites_menu

class OrderItem(BaseModel):
    item: str
    quantity: int

class OrderRequest(BaseModel):
    orders: List[OrderItem]
    payment_method: str
    cash_paid: float = 0.0

# 🔴 UPDATE THIS FUNCTION TO SERVE THE WEBSITE WEBSITE UI
@app.get("/", response_class=HTMLResponse)
def read_root():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>SHRUTIKA's CAFE</title>
        <link href="https://googleapis.com" rel="stylesheet">
        <style>
            body {
                font-family: 'Poppins', sans-serif;
                background-color: #fcf8f2;
                color: #4a3b32;
                margin: 0;
                padding: 20px;
                display: flex;
                flex-direction: column;
                align-items: center;
            }
            .container {
                max-width: 600px;
                width: 100%;
                background: white;
                padding: 30px;
                border-radius: 16px;
                box-shadow: 0 10px 30px rgba(74, 59, 50, 0.1);
            }
            h1 {
                text-align: center;
                color: #8c6239;
                font-weight: 600;
                margin-bottom: 5px;
                text-transform: uppercase;
                letter-spacing: 2px;
            }
            .tagline {
                text-align: center;
                font-size: 0.9rem;
                color: #a08470;
                margin-bottom: 30px;
            }
            .section-title {
                font-size: 1.2rem;
                color: #6f4e37;
                border-bottom: 2px solid #f3e9dc;
                padding-bottom: 5px;
                margin-top: 25px;
                font-weight: 600;
            }
            .menu-item {
                display: flex;
                justify-content: space-between;
                margin: 12px 0;
                font-size: 1rem;
            }
            .item-name {
                font-weight: 400;
            }
            .item-price {
                font-weight: 600;
                color: #8c6239;
            }
            footer {
                text-align: center;
                margin-top: 40px;
                font-size: 0.8rem;
                color: #a08470;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>SHRUTIKA's CAFE</h1>
            <div class="tagline">Freshly Brewed Digital Innovation</div>
            
            <div class="section-title">ESPRESSO BAR</div>
            <div class="menu-item"><span class="item-name">Espresso</span><span class="item-price">$2.00</span></div>
            <div class="menu-item"><span class="item-name">Macchiato</span><span class="item-price">$2.50</span></div>
            <div class="menu-item"><span class="item-name">Latte</span><span class="item-price">$2.50</span></div>
            <div class="menu-item"><span class="item-name">Breve</span><span class="item-price">$2.50</span></div>
            <div class="menu-item"><span class="item-name">Mocha</span><span class="item-price">$3.00</span></div>
            <div class="menu-item"><span class="item-name">Cappuccino</span><span class="item-price">$3.00</span></div>
            <div class="menu-item"><span class="item-name">Americano</span><span class="item-price">$2.00</span></div>

            <div class="section-title">HOT CLASSICS</div>
            <div class="menu-item"><span class="item-name">Daily Dark Roast</span><span class="item-price">$2.75</span></div>
            <div class="menu-item"><span class="item-name">Pour Over</span><span class="item-price">$3.25</span></div>
            <div class="menu-item"><span class="item-name">Hot Chocolate</span><span class="item-price">$3.00</span></div>
            <div class="menu-item"><span class="item-name">Steamer</span><span class="item-price">$3.00</span></div>
            <div class="menu-item"><span class="item-name">Cafe Au Lait</span><span class="item-price">$4.00</span></div>

            <div class="section-title">QUICK BITES</div>
            <div class="menu-item"><span class="item-name">Bagel</span><span class="item-price">$2.00</span></div>
            <div class="menu-item"><span class="item-name">Muffin</span><span class="item-price">$2.20</span></div>
            <div class="menu-item"><span class="item-name">Breakfast Sandwich</span><span class="item-price">$4.75</span></div>
            <div class="menu-item"><span class="item-name">Croissant</span><span class="item-price">$1.75</span></div>
            <div class="menu-item"><span class="item-name">Scones</span><span class="item-price">$2.25</span></div>
        </div>
        <footer>Thank you for visiting SHRUTIKA's CAFE!</footer>
    </body>
    </html>
    """

# ... (Keep your @app.post("/order") function at the bottom exactly as it was) ...