import pytest
from agents.resource_agent import fetch_resources

def test_fetch_resources_success():
    dummy_use_cases = [
        "Title: AI Optimization in Manufacturing",
        "Title: Intelligent Customer Service Bot"
    ]
    resources = fetch_resources(dummy_use_cases)
    assert isinstance(resources, dict), "Should return a dictionary"
    assert len(resources) > 0, "There should be at least one resource set"
    for key, links in resources.items():
        assert isinstance(links, list), "Links should be a list"
        for link in links:
            assert "title" in link and "url" in link
