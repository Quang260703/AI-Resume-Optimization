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
        # 1. Initialize app and inject valid document state
        at = AppTest.from_file(app_path)
        at.session_state.docs_loaded = True
        at.run()

        # 2. Provide a Job Title but leave Job Description empty
        at.text_input(key="job_title_input").input("ML Engineer").run()
        # Ensure description is empty/blank
        at.text_area(key="job_desc_input").input("").run()

        # 3. Click the "Optimize" button
        # (Assuming the index of the button is 0)
        at.button[0].click().run()

        # 4. Verify that an error message is displayed
        assert len(at.error) > 0, "No error message was displayed for missing input."
        assert "provide both" in at.error[0].value.lower(), (
            "Expected error message not found."
        )
