import streamlit as st
import pickle
import pandas as pd

# Load saved rules
with open("model_MBA.pkl", "rb") as f:
    rules = pickle.load(f)

# Format frozensets to clean string
def format_set(itemset):
    return ", ".join(itemset) if isinstance(itemset, frozenset) else str(itemset)

# Define recommendation function

def get_product_rules(rules_df, product, top_n=5, min_conf=0.0):
    product = str(product)
    
    # Filter rules containing the product in antecedents
    mask = rules_df['antecedents'].apply(lambda items: any(product in str(i) for i in items))
    filtered = rules_df[mask]
    
    # Apply confidence filter
    filtered = filtered[filtered['confidence'] >= min_conf]

    # Format frozen sets
    filtered = filtered.copy()
    filtered['antecedents'] = filtered['antecedents'].apply(format_set)
    filtered['consequents'] = filtered['consequents'].apply(format_set)

    return filtered.sort_values(by='lift', ascending=False).head(top_n)

# UI
st.title("Market Basket Recommender")

# Text input for product
product = st.text_input("Enter a product keyword (e.g. SPACEBOY, CUTLERY, etc.):")

# Slider for confidence threshold
min_conf = st.slider("Minimum confidence", 0.0, 1.0, 0.6)

# Recommendation logic
if product:
 
    top_n = st.slider("How many recommendations to show", 1, 20, 10)
result_df = get_product_rules(rules, product, top_n=top_n, min_conf=min_conf)
    #result_df = get_product_rules(rules, product, top_n=10, min_conf=min_conf)
    
    if result_df.empty:
        st.warning(" No recommendations found for this product.")
    else:
        st.success(f"Found {len(result_df)} recommendations for '{product}'")
        st.dataframe(result_df[['antecedents', 'consequents', 'confidence', 'lift']])
