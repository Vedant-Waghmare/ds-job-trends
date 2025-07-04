import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import plotly.express as px

st.set_page_config(page_title="DS Job Trends", layout="wide")

st.title("📊 Data Science Job Trends & Skill Analysis")
st.markdown("### By Vedant Waghmare – AI & Data Science Intern Applicant")

# Load dataset
@st.cache_data
def load_data():
    return pd.read_csv("ds_salaries.csv")

df = load_data()

# Sidebar filters
st.sidebar.header("🔍 Filter Jobs")
year = st.sidebar.selectbox("Select Year", sorted(df['work_year'].unique(), reverse=True))
experience = st.sidebar.multiselect(
    "Experience Level",
    options=df['experience_level'].unique(),
    default=list(df['experience_level'].unique())
)

filtered_df = df[(df['work_year'] == year) & (df['experience_level'].isin(experience))]

# Display data summary
st.subheader("📌 Filtered Dataset Preview")
st.dataframe(filtered_df.head(10), use_container_width=True)

# Top Job Titles
st.subheader("🏷️ Top Job Titles")
top_titles = (
    filtered_df['job_title'].value_counts()
    .reset_index()
)
top_titles.columns = ['Job_Title', 'Count']

fig1 = px.bar(
    top_titles.head(10),
    x='Count',
    y='Job_Title',
    orientation='h',
    title="Top 10 Job Titles"
)
st.plotly_chart(fig1, use_container_width=True)

# Company Locations
st.subheader("🌍 Company Locations")

top_locations = (
    filtered_df['company_location'].value_counts()
    .reset_index()
)
top_locations.columns = ['Company_Location', 'Count']  # Explicit column names

fig2 = px.bar(
    top_locations.head(10),
    x='Company_Location',
    y='Count',
    title="Top Company Locations"
)
st.plotly_chart(fig2, use_container_width=True)

# Experience Level Distribution
st.subheader("📊 Experience Level Distribution")
exp_counts = filtered_df['experience_level'].value_counts()
fig3 = px.pie(
    names=exp_counts.index, 
    values=exp_counts.values, 
    title="Experience Level Breakdown",
    hole=0.4
)
st.plotly_chart(fig3, use_container_width=True)

# Remote Work Analysis
st.subheader("🏠 Remote Work Ratio")
remote_counts = filtered_df['remote_ratio'].value_counts().sort_index()
fig4 = px.bar(
    x=remote_counts.index, 
    y=remote_counts.values,
    labels={'x': 'Remote Work %', 'y': 'Job Count'},
    title="Remote Work Preference"
)
st.plotly_chart(fig4, use_container_width=True)

# WordCloud from Job Descriptions (or combine columns if missing)
st.subheader("☁️ In-Demand Skills (WordCloud)")
text_data = ""

if 'job_description' in df.columns:
    text_data = " ".join(filtered_df['job_description'].dropna().astype(str))
else:
    cols_to_combine = ['job_title', 'experience_level', 'employment_type']
    text_data = " ".join(filtered_df[cols_to_combine].astype(str).agg(' '.join, axis=1))

if text_data.strip():
    wordcloud = WordCloud(width=1000, height=500, background_color='white').generate(text_data)
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.imshow(wordcloud, interpolation="bilinear")
    ax.axis("off")
    st.pyplot(fig)
else:
    st.warning("No descriptive text available to generate WordCloud.")

st.markdown("---")
st.markdown("Made using Streamlit by **Vedant Waghmare**")