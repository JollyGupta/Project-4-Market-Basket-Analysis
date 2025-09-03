import streamlit as st
import pickle
import pandas as pd

# Load saved rules
with open("model_MBA.pkl", "rb") as f:
    rules = pickle.load(f)

# 🧹 Format frozensets to clean string
def format_set(itemset):
    return ", ".join(itemset) if isinstance(itemset, frozenset) else str(itemset)

# 🔍 Define recommendation function
def get_product_rules(rules_df, product, top_n=5, min_conf=0.0):
    product = str(product).lower()
    
    # Filter rules where the product appears in antecedents (case-insensitive)
    mask = rules_df['antecedents'].apply(
        lambda items: any(product in str(i).lower() for i in items)
    )
    filtered = rules_df[mask]
    
    # Apply confidence filter
    filtered = filtered[filtered['confidence'] >= min_conf]

    # Format frozen sets to clean strings
    filtered = filtered.copy()
    filtered['antecedents'] = filtered['antecedents'].apply(format_set)
    filtered['consequents'] = filtered['consequents'].apply(format_set)

    return filtered.sort_values(by='lift', ascending=False).head(top_n)

# 🎨 UI
st.set_page_config(page_title="Market Basket Recommender", page_icon="🛒")
st.title("🛒 Market Basket Recommender")
st.caption("🔍 Enter a product to get associated recommendations based on Apriori analysis.")

# 📥 Product input
product = st.text_input("Enter a product keyword (e.g. SPACEBOY, CUTLERY, etc.):").strip()

# 🎚️ Sliders
min_conf = st.slider("Minimum confidence", 0.0, 1.0, 0.6)
top_n = st.slider("How many recommendations to show", 1, 20, 10)

# 🔁 Recommendation logic
if product:
    result_df = get_product_rules(rules, product, top_n=top_n, min_conf=min_conf)
    
    if result_df.empty:
        st.warning(f"❌ No recommendations found for '{product}'. Try another keyword.")
    else:
        st.success(f"✅ Found {len(result_df)} recommendation(s) for '{product}'")
        st.dataframe(result_df[['antecedents', 'consequents', 'confidence', 'lift']])

        # 📤 Download button
        csv = result_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Download as CSV",
            data=csv,
            file_name=f"{product}_recommendations.csv",
            mime="text/csv"
        )

