import pytest
from agents.solution_agent import suggest_genai_solutions

def test_suggest_genai_solutions_success():
    dummy_summary = "This is a sample industry research summary."
    suggestions = suggest_genai_solutions(dummy_summary)
    assert isinstance(suggestions, list), "Suggestions should be a list"
    assert len(suggestions) >= 2, "Should return at least two solutions"
    for suggestion in suggestions:
        assert isinstance(suggestion, str), "Each suggestion should be a string"
