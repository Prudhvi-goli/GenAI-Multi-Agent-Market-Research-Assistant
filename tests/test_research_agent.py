import pytest
from agents.research_agent import run_research_agent

def test_run_research_agent_success():
    """
    Test that the research agent returns a non-empty summary.
    """
    query = "Tesla"
    result = run_research_agent(query)
    assert isinstance(result, str), "Result should be a string"
    assert len(result) > 100, "Result should not be too short"
    assert "Sources" in result, "Result should contain sources section"

def test_run_research_agent_invalid_input():
    """
    Test that the research agent handles empty input gracefully.
    """
    query = ""
    result = run_research_agent(query)
    assert isinstance(result, str)
    assert "Error" in result or len(result) < 100, "Should return an error or a small response"
