import streamlit as st
from dotenv import load_dotenv
import os
import pandas as pd
from main import Main  # Your LinkedIn Scraper
from mini_game import MiniGame  # Import the updated MiniGame

# Load environment variables
load_dotenv()
email = os.getenv("EMAIL")
password = os.getenv("PASSWORD")

tab1, tab2 = st.tabs(["🔍 Job Search", "📋 Results"])

with tab1:


    st.title("🔍 LinkedIn Job Scraper")

    st.markdown("Enter job title and location to search LinkedIn for job postings.")

    # Default location
    location = "Worldwide"

    # Job search input
    title = st.text_input("Job Title", placeholder="e.g., Data Analyst")
    location = st.text_input("Location", placeholder="e.g., Germany or Worldwide")
    num_results = st.slider("Number of Results", 5, 50, 10)

    # 🎮 Initialize MiniGame BEFORE job search
    game = MiniGame(duration=15)
    game.start_game()

    if st.button("Start Search"):
        if not title:
            st.warning("Please enter a job title.")
        if title and location:
            try:
                with st.spinner("Scraping jobs from LinkedIn..."):
                    scraper = Main(title, email, password, num_results=num_results)
                    scraper.search.location = location
                    scraper.run()
                    scraper.save_to_csv()
                    scraper.close()
                    st.session_state["results"] = pd.DataFrame(scraper.results, columns=["title", "company", "location", "type", "link"])

                    if os.path.exists("captcha_detected.txt"):
                        st.warning("CAPTCHA detected. Please solve it in the opened browser.")

                        if os.path.exists("captcha.png"):
                            st.image("captcha.png", caption="Captcha Screenshot", use_column_width=True)
                            os.remove("captcha.png")
                        os.remove("captcha_detected.txt")

            except Exception as e:
                st.error(f"⚠️ An error occurred:\n\n{e}")

with tab2:
    st.header("📋 Scraping Results")
    if "results" in st.session_state:
        df = st.session_state["results"]
        if df.empty:
            st.warning("No jobs found.")
        else:
            st.dataframe(df, use_container_width=True)
            st.download_button("📥 Download CSV", df.to_csv(index=False).encode("utf-8"), "job_results.csv", "text/csv")
    else:
        st.info("No results yet. Run a search from the first tab.")


