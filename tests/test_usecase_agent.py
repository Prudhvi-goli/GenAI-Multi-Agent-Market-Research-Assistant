import pytest
from agents.usecase_agent import generate_use_cases

def test_generate_use_cases_success():
    dummy_summary = """
    Tesla is investing in AI-driven autonomous driving technology and energy optimization solutions.
    """
    use_cases = generate_use_cases(dummy_summary)
    assert isinstance(use_cases, list), "Use cases should be a list"
    assert len(use_cases) > 0, "There should be at least one use case"
    for use_case in use_cases:
        assert use_case.startswith("Title:"), "Each use case should start with 'Title:'"
