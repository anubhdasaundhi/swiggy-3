import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# ===============================
# Page config
# ===============================
st.set_page_config(page_title="🍽️ City Food Recommendation", layout="wide")

st.markdown("""
<style>
.main-header {font-size: 2.8rem; color: #ff6b35; font-weight: bold;}
.sub-header {font-size: 1.4rem; color: #444;}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">🍽️ Best Food Recommendations by City</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Powered by Swiggy-style restaurant data</div>', unsafe_allow_html=True)

# ===============================
# Load data
# ===============================
@st.cache_data
def load_data():
    df = pd.read_csv("DOd.csv")
    df = df.dropna(subset=['city', 'name', 'rating', 'cost'])
    return df

df = load_data()

# ===============================
# Sidebar filters
# ===============================
st.sidebar.header("🔎 Filters")

city = st.sidebar.selectbox("Select City", sorted(df['city'].unique()))

min_rating = st.sidebar.slider("Minimum Rating", 0.0, 5.0, 4.0, 0.1)
budget = st.sidebar.slider("Max Cost (₹)", 100, int(df['cost'].max()), 500)

# ===============================
# City-wise filtering
# ===============================
city_df = df[
    (df['city'] == city) &
    (df['rating'] >= min_rating) &
    (df['cost'] <= budget)
]

# ===============================
# Recommendation logic
# ===============================
# Weighted score: rating + popularity
city_df['score'] = (
    city_df['rating'] * 0.7 +
    np.log1p(city_df['rating_count']) * 0.3
)

best_food = city_df.sort_values('score', ascending=False)

# ===============================
# Top recommendation
# ===============================
st.subheader(f"🏆 Best Food Picks in {city}")

if best_food.empty:
    st.warning("No restaurants match your filters. Try adjusting rating or budget.")
else:
    top_pick = best_food.iloc[0]

    col1, col2, col3 = st.columns(3)
    col1.metric("🍴 Restaurant", top_pick['name'])
    col2.metric("⭐ Rating", f"{top_pick['rating']}")
    col3.metric("💰 Cost", f"₹{int(top_pick['cost'])}")

# ===============================
# Top 10 recommendations table
# ===============================
st.subheader("🍽️ Top 10 Recommended Foods / Restaurants")

st.dataframe(
    best_food[['name', 'cuisine', 'rating', 'rating_count', 'cost']]
    .head(10)
    .reset_index(drop=True),
    use_container_width=True
)

# ===============================
# Visuals
# ===============================
st.subheader("📊 Rating vs Cost (Filtered)")

fig = px.scatter(
    best_food.head(50),
    x='cost',
    y='rating',
    size='rating_count',
    color='cuisine',
    hover_data=['name'],
    title=f"Best Food Options in {city}"
)

st.plotly_chart(fig, use_container_width=True)

# ===============================
# Footer
# ===============================
st.markdown("---")
st.markdown("*Food Recommendation App built using Data Science ❤️*")