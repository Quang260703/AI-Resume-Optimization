import unittest
from unittest.mock import patch, MagicMock
import os
from src.reading_agents import run_reading_agent


class TestReadingAgent(unittest.TestCase):
    def setUp(self):
        # Mocking document objects
        self.mock_doc = MagicMock()
        self.mock_doc.text = "Sample resume text content."
        self.documents = [self.mock_doc]
        self.query = "Highlight my management skills."
        self.job_title = "Senior Developer"
        self.job_desc = "Looking for a leader with 5+ years exp."

    @patch("src.reading_agents.GoogleGenAI")
    @patch.dict(os.environ, {"GEMINI_API_KEY": "fake_key"})
    def test_run_reading_agent_success(self, mock_llm_class):
        # Setup mock behavior
        mock_llm_instance = mock_llm_class.return_value
        mock_llm_instance.complete.return_value = (
            "Optimized resume content based on job description."
        )

        # Execute
        result = run_reading_agent(
            self.documents, self.query, self.job_title, self.job_desc
        )

        # Assertions
        self.assertEqual(result, "Optimized resume content based on job description.")
        mock_llm_instance.complete.assert_called_once()

    @patch("src.reading_agents.GoogleGenAI")
    def test_run_reading_agent_exception(self, mock_llm_class):
        # Simulate an API error
        mock_llm_class.side_effect = Exception("API Connection Error")

        # Verify that the exception is raised
        with self.assertRaises(Exception) as context:
            run_reading_agent(self.documents, self.query, self.job_title, self.job_desc)

        self.assertTrue("API Connection Error" in str(context.exception))


if __name__ == "__main__":
    unittest.main()
