import os
from streamlit.testing.v1 import AppTest
from unittest.mock import patch


def test_optimization_without_job_description():
    """
    Test that the app displays an error message when the user
    tries to optimize without providing a job description.
    """
    app_path = "src/main.py"

    with patch.dict(os.environ, {"GEMINI_API_KEY": "fake_test_key"}):
        at = AppTest.from_file(app_path, default_timeout=10).run()
        at.session_state.docs_loaded = True
        at.text_input(key="job_title_input").input("ML Engineer").run()
        at.text_area(key="job_desc_input").input("").run()
        at.button[0].click().run()
        assert len(at.error) > 0, "No error message was displayed for missing input."
        assert "provide both" in at.error[0].value.lower()