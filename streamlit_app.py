import streamlit as st
import sys
import os
os.environ["STREAMLIT_WATCHER_TYPE"] = "none"
import tempfile
from datetime import datetime

from agents.research_agent import run_research_agent
from agents.usecase_agent import generate_use_cases
from agents.resource_agent import fetch_resources
from agents.solution_agent import suggest_genai_solutions
from reports.report_generator import generate_markdown_report

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))

st.title("GenAI Market Research Assistant")

query = st.text_input("Enter a company or industry")

if st.button("Generate Report") and query:
    with st.spinner("Researching and generating insights..."):
        summary = run_research_agent(query)
        st.subheader("Research Summary")
        st.write(summary)

        use_cases = generate_use_cases(summary)
        st.subheader("Generated Use Cases")
        for case in use_cases:
            st.markdown(f"{case}\n")

        resources = fetch_resources(use_cases)
        st.subheader("Relevant Datasets")
        for title, links in resources.items():
            st.markdown(f"**{title}**")
            for url in links:
                st.markdown(f"- [Link]({url})")

        solutions = suggest_genai_solutions(summary)
        st.subheader("Suggested GenAI Solutions")
        for idea in solutions:
            st.markdown(f"- {idea}")

        # Save report and offer download
        date = datetime.now().strftime("%Y-%m-%d")
        report_name = f"{query.replace(' ', '_')}_GenAI_Report_{date}.md"
        report_path = generate_markdown_report(query, summary, use_cases, resources, solutions)

        with open(report_path, "r", encoding="utf-8") as file:
            st.download_button(
                label="📄 Download Markdown Report",
                data=file.read(),
                file_name=os.path.basename(report_path),
                mime="text/markdown"
            )
