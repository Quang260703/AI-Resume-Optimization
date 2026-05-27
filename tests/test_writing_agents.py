import pytest
from unittest.mock import MagicMock, patch
from src.writing_agents import run_writing_agent


@patch("src.writing_agents.GoogleGenAI")
def test_writing_agent_returns_latex_string(mock_genai_cls):
    """Test that the agent returns a valid-looking LaTeX string."""
    mock_llm = MagicMock()
    latex_output = r"\documentclass{article}\begin{document}Hello World\end{document}"
    mock_llm.complete.return_value = latex_output
    mock_genai_cls.return_value = mock_llm

    result = run_writing_agent(
        [MagicMock(text="Python dev")],
        "Write a resume.",
        "ML Engineer",
        "Python skills required.",
    )

    assert isinstance(result, str)
    assert r"\documentclass" in result
    assert r"\begin{document}" in result
    mock_llm.complete.assert_called_once()


@patch("src.writing_agents.GoogleGenAI")
def test_writing_agent_raises_on_llm_error(mock_genai_cls):
    """Test that the agent propagates LLM errors (e.g., API failures)."""
    mock_llm = MagicMock()
    mock_llm.complete.side_effect = Exception("Model request failed")
    mock_genai_cls.return_value = mock_llm

    with pytest.raises(Exception, match="Model request failed"):
        run_writing_agent(
            [MagicMock(text="Python dev")],
            "Add TensorFlow.",
            "ML Engineer",
            "We need Python skills.",
        )
