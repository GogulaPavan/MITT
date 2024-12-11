import streamlit as st
import requests
import pandas as pd
from typing import List

# Fetch products from API
def fetch_products(page: int = 1, limit: int = 10) -> List[dict]:
    url = f"https://fakestoreapi.com/products?limit={limit}&page={page}"
    response = requests.get(url)
    return response.json()

# Display product details on product detail page
def display_product_details(product_id: int):
    product = next(p for p in products if p['id'] == product_id)
    st.image(product['image'], width=300)
    st.title(product['title'])
    st.subheader(f"Price: ${product['price']}")
    st.text(f"Description: {product['description']}")
    st.text(f"Rating: {product['rating']['rate']} stars")
    st.text(f"Reviews: {product['rating']['count']} reviews")
    st.button("Add to Cart", on_click=add_to_cart, args=(product,))

# Function to add products to the cart
def add_to_cart(product):
    cart.append(product)
    st.success(f"Added {product['title']} to the cart")

# Display the cart
def display_cart():
    if not cart:
        st.warning("Your cart is empty!")
        return
    st.header("Your Cart")
    total_price = 0
    for product in cart:
        st.image(product['image'], width=50)
        st.write(f"{product['title']} - ${product['price']}")
        total_price += product['price']
    st.write(f"Total Price: ${total_price}")
    st.button("Proceed to Checkout", on_click=checkout)

# Checkout functionality
def checkout():
    st.write("Proceeding to checkout...")
    st.write("Thank you for your purchase!")

# Main app layout
st.title("E-Commerce Store")
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Choose page", ["Homepage", "Cart"])

# Global cart variable to store selected products
if 'cart' not in st.session_state:
    st.session_state.cart = []

cart = st.session_state.cart

if page == "Homepage":
    st.header("Featured Products")
    products = fetch_products(page=1)
    for product in products:
        st.image(product['image'], width=100)
        st.subheader(product['title'])
        st.write(f"Price: ${product['price']}")
        st.write(f"Rating: {product['rating']['rate']} stars")
        if st.button(f"View {product['title']} details", key=product['id']):
            display_product_details(product['id'])
        if st.button(f"Add {product['title']} to cart", key=f"add_{product['id']}"):
            add_to_cart(product)

elif page == "Cart":
    display_cart()
