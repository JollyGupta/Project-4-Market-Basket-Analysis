import streamlit as st
import pickle
import pandas as pd

# Load saved rules
with open("model_MBA.pkl", "rb") as f:
    rules = pickle.load(f)

# Define recommendation function
def get_product_rules(rules_df, product, top_n=5):
    product = str(product)
    mask = rules_df['antecedents'].apply(lambda items: any(product in str(i) for i in items))
    return rules_df[mask].sort_values(by='lift', ascending=False).head(top_n)

# UI
st.title("🛒 Market Basket Recommender")

product = st.text_input("Enter a product keyword (e.g. SPACEBOY, CUTLERY, etc.):")

if product:
    result_df = get_product_rules(rules, product)
    if result_df.empty:
        st.warning("No recommendations found.")
    else:
        st.dataframe(result_df[['antecedents', 'consequents', 'confidence', 'lift']])
