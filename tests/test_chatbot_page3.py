import sys
import os
import pytest

# Add project directory to sys.path for imports
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from chatbot_fat import get_response, main


# Fixture for setup
@pytest.fixture(scope="module", autouse=True)
def setup_chatbot():
    pdf_path = './qdrant/2024-fall-comp690-M2-M3-jin-1.pdf'
    main(pdf_path)  # Initialize chatbot with the provided PDF


# Expected responses for Page 3
expected_responses_page3 = {
    "What are the three components of the final grade?": [
        "Class Attendance (10%)", "Sprint Grade (60%)", "Final Project Report (20%)", "Homework (10%)"
    ],
    "What percentage of the final grade is class attendance?": ["10%"],
    "How is the Sprint Grade calculated?": ["Teamwork Grade x Sprint Grade"],
    "What is included in the Teamwork Grade?": ["Peer evaluation for each of the three sprints", "detailed rubrics are TBA"],
    "What is included in the Sprint Grade?": ["The technical aspects of the product", "team project management", "detailed rubrics are TBA"],
    "What is the percentage weight of the final project report?": ["20%"],
    "What are the requirements for the final project report?": ["See Appendix A for details"],
    "What is the policy on late submissions?": ["The policy is very strict", "only in exceptional cases", "illness, accident, emergencies", "proper documentation"],
    "Under what circumstances might a late submission be accepted?": ["With prior email notification", "explanation of circumstances", "supporting evidence"],
    "What is the university's policy on attendance?": ["Students are responsible for attending scheduled meetings", "University Policy on Attendance", "UNH Student Rights, Rules, and Responsibilities"],
    "What should students do if they cannot attend a scheduled meeting?": ["Email the instructor BEFORE the meeting", "explain the circumstances", "request to be excused", "Arrange a meeting to update internship progress"],
    "What is the minimum number of hours required for the course?": ["A minimum of 45 hours of student academic work per credit per term"],
    "What should students do if they cannot attend class due to illness?": ["Email the instructor before class", "explain the situation", "request an excused absence", "Follow the late submission policy"],
    "What happens if a student fails to comply with late submission rules?": ["No credit for the assignment"],
    "What are the detailed rubrics for evaluating teamwork?": ["The detailed rubrics are TBA"],
    "What are the detailed rubrics for evaluating sprints?": ["The detailed rubrics are TBA"],
    "What is the minimum grade needed on the final report to pass the course?": ["75%"],
    "Is there any additional homework besides the final report?": ["Yes", "additional homework in project management and development tools"],
    "What is the weight of the homework towards the final grade?": ["10%"],
    "What is the credit hour workload estimate for this course?": ["A minimum of 45 hours per credit per term"]
}

# Test function for Page 3
@pytest.mark.parametrize("question, expected_keywords", expected_responses_page3.items())
def test_chatbot_page3_responses(question, expected_keywords):
    response = get_response(question)  # Call the real model function
    # Check that at least one expected keyword is in the response
    assert any(keyword in response for keyword in expected_keywords), f"For '{question}', expected one of {expected_keywords} but got '{response}'"
