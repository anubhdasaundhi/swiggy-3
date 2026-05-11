import streamlit as st
import pandas as pd

# Page config
st.set_page_config(
    page_title="Restaurant Recommendation System",
    layout="wide"
)

# Load dataset
@st.cache_data
def load_data():
    return pd.read_csv("cleaned_swiggy.csv")

df = load_data()

# Title
st.title("🍽️ Swiggy Restaurant Recommendation System")
st.markdown("Select **City & Cuisine**, then click **Recommend Restaurants**")

# Sidebar
st.sidebar.header("User Preferences")

# Step 1: City selection
city = st.sidebar.selectbox(
    "Select City",
    sorted(df['city'].unique())
)

# Step 2: Cuisine based on selected city
city_filtered = df[df['city'] == city]

cuisine = st.sidebar.selectbox(
    "Select Cuisine",
    sorted(city_filtered['cuisine'].unique())
)

# Filters
min_rating = st.sidebar.slider("Minimum Rating", 0.0, 5.0, 3.5, 0.1)

max_cost = st.sidebar.slider(
    "Maximum Cost",
    int(city_filtered['cost'].min()),
    int(city_filtered['cost'].max()),
    int(city_filtered['cost'].max())
)

top_n = st.sidebar.slider("Number of Restaurants", 5, 20, 10)

# 👉 Recommendation button
recommend_btn = st.sidebar.button("🍴 Recommend Restaurants")

# ==============================
# Show results ONLY after click
# ==============================
if recommend_btn:

    # Recommendation logic
    recommended_df = city_filtered[
        (city_filtered['cuisine'] == cuisine) &
        (city_filtered['rating'] >= min_rating) &
        (city_filtered['cost'] <= max_cost)
    ]

    recommended_df = recommended_df.sort_values(
        by=['rating', 'rating_count'],
        ascending=False
    ).head(top_n)

    st.subheader(f"🍴 Dashboard of Recommended Restaurants in {city} ({cuisine})")

    if recommended_df.empty:
        st.warning("❌ No restaurant available for the selected preferences.")
    else:
        st.dataframe(
            recommended_df[['name', 'rating', 'rating_count', 'cost']],
            use_container_width=True
        )

        # Dashboard insights
        st.markdown("### 📊 Dashboard Insights")

        col1, col2, col3 = st.columns(3)

        col1.metric("Total Restaurants", recommended_df.shape[0])
        col2.metric(
            "Average Rating",
            round(recommended_df['rating'].mean(), 2)
        )
        col3.metric(
            "Average Cost",
            int(recommended_df['cost'].mean())
        )

else:
    st.info("👈 Please select preferences and click **Recommend Restaurants**")