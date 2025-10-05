import streamlit as st
from fastapi import FastAPI, Request
from pydantic import BaseModel
import uvicorn
import threading
import requests

# ---- INVOICE LOGIC ----
def generate_invoice(customer_name, product, quantity, unit_price):
    try:
        quantity = int(quantity)
        unit_price = float(unit_price)
    except:
        return {"error": "Quantity and Unit Price must be numbers"}

    invoice_amount = quantity * unit_price
    description = f"Invoice for {customer_name}: {quantity} x {product} at {unit_price} each. Total = {invoice_amount}"
    return {
        "customer_name": customer_name,
        "product": product,
        "quantity": quantity,
        "unit_price": unit_price,
        "invoice_amount": invoice_amount,
        "description": description
    }

# ---- FASTAPI SECTION ----
app = FastAPI()

class InvoiceRequest(BaseModel):
    customer_name: str
    product: str
    quantity: int
    unit_price: float

@app.post("/generate-invoice")
async def create_invoice(data: InvoiceRequest):
    return generate_invoice(data.customer_name, data.product, data.quantity, data.unit_price)

# Run FastAPI in background thread so Streamlit & API work together
def run_fastapi():
    uvicorn.run(app, host="0.0.0.0", port=8000)

threading.Thread(target=run_fastapi, daemon=True).start()

# ---- STREAMLIT SECTION ----
st.title("Invoice Generator (UI + API)")

customer_name = st.text_input("Customer Name")
product = st.text_input("Product")
quantity = st.number_input("Quantity", min_value=1, step=1)
unit_price = st.number_input("Unit Price", min_value=0.0, step=0.01)

if st.button("Generate Invoice"):
    result = generate_invoice(customer_name, product, quantity, unit_price)
    st.write(result)
    st.success(result["description"])
