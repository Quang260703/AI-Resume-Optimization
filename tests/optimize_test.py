import pytest
from unittest.mock import patch
from src.reading_agents import run_reading_agent


class MockDocument:
    def __init__(self, text):
        self.text = text


@pytest.fixture
def mock_docs():
    return [MockDocument("Experience: Python Developer at Tech Corp.")]


@pytest.fixture
def sample_job_data():
    return {
        "query_text": "Optimize keywords",
        "job_title": "Senior AI Engineer",
        "job_description": "Must know Python and Gemini API.",
    }


def test_optimization_success(mock_docs, sample_job_data):
    with patch("src.reading_agents.GoogleGenAI") as mock_genai:
        mock_instance = mock_genai.return_value
        mock_instance.complete.return_value = (
            "## Key Findings\n• Strong Python skills found."
        )

        result = run_reading_agent(documents=mock_docs, **sample_job_data)

        assert "Key Findings" in result
        assert "Strong Python skills" in result
        mock_instance.complete.assert_called_once()


def test_optimization_api_failure(mock_docs, sample_job_data):
    with patch("src.reading_agents.GoogleGenAI") as mock_genai:
        mock_instance = mock_genai.return_value
        mock_instance.complete.side_effect = Exception("Quota Exceeded")

        with pytest.raises(Exception) as excinfo:
            run_reading_agent(mock_docs, **sample_job_data)

        assert "Quota Exceeded" in str(excinfo.value)
