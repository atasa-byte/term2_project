import streamlit as st
import pandas as pd


# uploaded_file = st.file_uploader("job_result.csv", type=["csv"])

st.title("📄 نمایش نتایج اسکرپ شده")

try:
    df = pd.read_csv("job_results.csv")  # File saved from previous script
    st.success("✅ فایل با موفقیت بارگذاری شد.")
    st.dataframe(df)
except FileNotFoundError:
    st.error("❌ فایل job_results.csv پیدا نشد.")
