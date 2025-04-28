# GenAI Multi-Agent Research Assistant

This project is an intelligent multi-agent system that helps automate market research, generate use cases, search for relevant datasets in real-time, and suggest GenAI-based solutions. It also allows users to download a full research report.  
The system is built using Large Language Models (LLMs), Retrieval-Augmented Generation (RAG) techniques, real-time web search, and a simple Streamlit web application.

## Project Overview

The project uses multiple specialized agents that work together:

- Research Agent: Performs market research and generates a summary.
- Use Case Agent: Creates relevant GenAI use cases based on the research.
- Resource Agent: Finds real-world datasets or resources using live Google Search powered by SerpAPI.
- Solution Agent: Suggests suitable GenAI solutions for the identified problems.

The agents collaborate in sequence, and the final output can be viewed and downloaded as a Markdown report.

## Key Features

- Modular multi-agent architecture.
- Real-time data fetching from the web using SerpAPI.
- Small and efficient LLM model (TinyLlama) used instead of heavy models.
- Fast and parallel resource searching to improve performance.
- Streamlit web application to interact with the system.
- Full Markdown report generation for easy download.
- Unit tests included for each major agent module.

## Technology Stack

- Python 3.10
- Streamlit for building the web interface
- HuggingFace Transformers (TinyLlama Model)
- SerpAPI for real-time Google search results
- BeautifulSoup and requests for web scraping
- Concurrent futures for parallel execution
- Pytest for unit testing

## Folder Structure

```
multi_Agent/
│
├── agents/
│   ├── research_agent.py
│   ├── usecase_agent.py
│   ├── resource_agent.py
│   ├── solution_agent.py
│
├── reports/
│   ├── report_generator.py
│
├── tests/
│   ├── test_research_agent.py
│   ├── test_usecase_agent.py
│   ├── test_resource_agent.py
│   ├── test_solution_agent.py
│
├── streamlit_app.py
├── main.py
├── requirements.txt
├── README.md
└── .gitignore
```

## How to Set Up the Project Locally

1. Clone the repository

```bash
git clone https://github.com/Prudhvi-goli/GenAI-Multi-Agent-Market-Research-Assistant.git
cd genai-multi-agent-research-assistant
```

2. Create and activate a virtual environment

```bash
python -m venv venv
venv\Scripts\activate    # For Windows
source venv/bin/activate # For Mac/Linux
```

3. Install the required packages

```bash
pip install -r requirements.txt
```

4. Set up the environment variables

Create a `.env` file in the root directory and add the following:

```
SERPAPI_API_KEY=your_serpapi_key_here
```

You can get a free API key from [serpapi.com](https://serpapi.com/).

5. Run the Streamlit app

```bash
streamlit run streamlit_app.py
```

6. Open your browser and go to

```
http://localhost:8501
```

You will see a simple interface to enter a company or industry name and generate the full report.

## How It Works

- Enter a company name or industry field in the input box.
- The Research Agent performs web-based market research using the TinyLlama model.
- The Use Case Agent generates multiple GenAI use cases based on the research.
- The Resource Agent uses SerpAPI to fetch real-time relevant links from Google search.
- The Solution Agent suggests suitable GenAI solutions.
- The system organizes all results into a structured report.
- You can view the report on screen and download it as a Markdown file.

## Testing the Project

You can run all unit tests using:

```bash
pytest -v
```

This will check that each agent (research, usecase, resource, solution) works correctly.

## Future Improvements

- Adding vector database support for advanced document search.
- Expanding resource agent to support multiple search providers.
- Improving parallel search performance with asyncio.
- Adding a simple dashboard for past queries and reports.
