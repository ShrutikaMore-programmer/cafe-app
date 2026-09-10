from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

# 1. Define the menus
Espresso_menu = {"Espresso": 2.00, "Macchiato": 2.50, "Latte": 2.50, "Breve": 2.50, "Mocha": 3.00, "Cappuccino": 3.00, "Americano": 2.00}
Hot_menu = {"Daily Dark Roast": 2.75, "Pour Over": 3.25, "Hot Chocolate": 3.00, "Steamer": 3.00, "Cafe Au Lait": 4.00}
Quick_bites_menu = {"Bagel": 2.00, "Muffin": 2.20, "Breakfast Sandwich": 4.75, "Croissant": 1.75, "Scones": 2.25}
merged_menu = Espresso_menu | Hot_menu | Quick_bites_menu

# 2. Define what an incoming order item should look like
class OrderItem(BaseModel):
    item: str
    quantity: int

class OrderRequest(BaseModel):
    orders: List[OrderItem]
    payment_method: str  # "card" or "cash"
    cash_paid: float = 0.0

@app.get("/")
def read_root():
    return {
        "cafe_name": "SHRUTIKA's CAFE",
        "message": "Welcome! Send a POST request to /order to generate a receipt.",
        "menu": {
            "Espresso": Espresso_menu,
            "Hot Drinks": Hot_menu,
            "Quick Bites": Quick_bites_menu
        }
    }

@app.post("/order")
def place_order(request: OrderRequest):
    receipt_items = []
    total_quantity = 0
    total_price = 0
    
    # Process items
    for order in request.orders:
        if order.item not in merged_menu:
            raise HTTPException(status_code=400, detail=f"Item '{order.item}' not found in menu.")
        
        if order.quantity <= 0:
            raise HTTPException(status_code=400, detail="Quantity must be greater than 0.")
            
        price = merged_menu[order.item]
        item_total = price * order.quantity
        total_quantity += order.quantity
        total_price += item_total
        
        receipt_items.append({
            "item": order.item,
            "quantity": order.quantity,
            "unit_price": f"${price:.2f}",
            "total": f"${item_total:.2f}"
        })
        
    gratuity = total_price * 0.08
    final_price = total_price + gratuity
    
    # Process payment logic
    payment_status = "Pending"
    change_returned = 0.0
    
    pay_method = request.payment_method.lower()
    if pay_method == "card":
        payment_status = "Payment Successful via Card"
    elif pay_method == "cash":
        if request.cash_paid < final_price:
            raise HTTPException(status_code=400, detail=f"Insufficient cash. Total is ${final_price:.2f}")
        change_returned = request.cash_paid - final_price
        payment_status = "Payment Successful via Cash"
    else:
        raise HTTPException(status_code=400, detail="Invalid payment method. Use 'card' or 'cash'.")

    # Return the clean json receipt
    return {
        "status": payment_status,
        "receipt": {
            "items": receipt_items,
            "total_items": total_quantity,
            "subtotal": f"${total_price:.2f}",
            "8_percent_gratuity": f"${gratuity:.2f}",
            "total_with_tax": f"${final_price:.2f}",
            "cash_received": f"${request.cash_paid:.2f}" if pay_method == "cash" else "$0.00",
            "change_to_return": f"${change_returned:.2f}" if pay_method == "cash" else "$0.00"
        },
        "message": "Thank you for visiting SHRUTIKA's CAFE!"
    }