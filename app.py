import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

df = pd.read_csv("1000_people_dataset.csv")

st.set_page_config("Data Dashboard", layout="wide")

st.markdown("📊 Interactive Data analytics Dashboard")
st.markdown("## Analyze and explore people data easily")
st.markdown("----")

df.drop_duplicates(inplace=True)
df["city"] = df["city"].str.strip()
df["profession"] = df["profession"].str.strip()

st.sidebar.header("🔍 Filters")

selected_city = st.sidebar.multiselect( # label , option , default
    "select city",
    df["city"].unique(),
    df["city"].unique()
)

selected_prof = st.sidebar.multiselect( # label , option , default
    "select profession",
    df["profession"].unique(),
    df["profession"].unique()
)

filtered_df= df[ df["city"].isin(selected_city)
                &
                df["profession"].isin(selected_prof)
                ]

if filtered_df.empty:
    st.warning("⚠️ No data found for selected filters")
    st.stop()

st.subheader("📌 Key Insights")

col1 , col2  ,col3 = st.columns(3)

col1.metric("Total people", len((filtered_df)))
col2.metric("Unique Cities", filtered_df["city"].nunique())
col3.metric("Unique Profession",filtered_df["profession"].nunique())

top_city= filtered_df["city"].value_counts().idxmax()
st.success(f"Top city is {top_city}")

top_prof= filtered_df["profession"].value_counts().idxmax()
st.success(f"Top profession is {top_prof}")

st.subheader("📄 Data Preview")

data =filtered_df.head(50)
st.dataframe(data)

st.subheader("City Distribution")

city_count=filtered_df["city"].value_counts()

fig1 , ax1 = plt.subplots()
ax1.bar(city_count.index , city_count.values)
plt.xticks(rotation=45)
st.pyplot(fig1)

st.subheader("Top 5 Cities")
top_5 = city_count.head()
st.bar_chart(top_5)

st.subheader("Profession Distribution")

prof_count=filtered_df["profession"].value_counts()

fig2 , ax2 = plt.subplots()
ax2.bar(prof_count.index , prof_count.values)
plt.xticks(rotation=45)
st.pyplot(fig2)

st.subheader("📧 Email Domain Analysis")

filtered_df["domain"]=filtered_df["email"].str.split("@").str[1]

domain_counts = filtered_df["domain"].value_counts()

st.bar_chart(domain_counts)

st.subheader("🔎 Search by Name")

search_name = st.text_input("Enter First name")


result = filtered_df.copy()


if search_name:
    result = filtered_df[
        filtered_df["fname"].str.contains(search_name, case=False, na=False)
    ]
    

if search_name and result.empty:
    st.warning("No matching names found")
    st.stop()

if search_name:
    st.write(f"🔍 Found {len(result)} matching records")

st.dataframe(result)

result["domain"] = result["email"].str.split("@").str[1]

st.subheader("📧 Domain vs Profession Insight")

domain_prof = pd.crosstab(result['domain'], result['profession'])
st.dataframe(domain_prof)


if search_name:
    st.subheader(f"📧 Domains used by '{search_name}'")
else:
    st.subheader("📧 Domain Usage (All Data)")

domain_counts = result["domain"].value_counts()
st.bar_chart(domain_counts)


