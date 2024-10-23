import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from chatbot_fat import get_response, main

# Fixture for setup
@pytest.fixture(scope="module", autouse=True)
def setup_chatbot():
    pdf_path = './qdrant/2024-fall-comp690-M2-M3-jin-1.pdf'
    main(pdf_path)

# Expected responses for Page 3
expected_responses_page3 = {
    "What are the components of the final grade?": ["Class Attendance (10%), Sprint Grade (60%), Homework (10%), and Final Project Report (20%)."],
    "How much is class attendance worth?": ["10% of the final grade."],
    "How is the Sprint Grade calculated?": ["Teamwork Grade multiplied by Sprint Grade."],
    "What determines the Teamwork Grade?": ["Peer evaluation for each of the three sprints; detailed rubrics are TBA (To Be Announced)."],
    "What determines the Sprint Grade?": ["The technical aspects of the product and team project management; detailed rubrics are TBA."],
    "What percentage is the final project report worth?": ["20%"],
    "Where can I find the final project report format?": ["See Appendix A."],
    "What's the policy on late submissions?": ["Very strict; only granted in exceptional cases (illness, accident, emergencies) with proper documentation."],
    "When might a late submission be considered?": ["Only if the student emails before the deadline, explains the circumstances, and provides evidence."],
    "What is UNH's attendance policy?": ["Students are responsible for attending scheduled meetings and are expected to abide by the University Policy on Attendance."],
    "What if I can't make a scheduled meeting?": ["Email the instructor beforehand, explain the situation, and request to be excused. Schedule a meeting to update the instructor."],
    "How many hours per week should I expect to spend on this course?": ["A minimum of 45 hours per credit per term."],
    "What should I do if I'm sick and can't come to class?": ["Email the instructor beforehand; follow the late submission guidelines if applicable."],
    "What happens if I don't follow the late submission rules?": ["You may receive no credit for the assignment."],
    "Are there specific rubrics for teamwork evaluation?": ["Detailed rubrics are TBA (To Be Announced)."],
    "Are there specific rubrics for sprint evaluation?": ["Detailed rubrics are TBA (To Be Announced)."],
    "What's the minimum final project report grade needed to pass the course?": ["75%"],
    "Is there any homework besides the final report?": ["Yes, additional homework in project management and development tools."],
    "How much is the additional homework worth?": ["10% of the final grade."],
    "What's the minimum credit hour workload estimate?": ["45 hours per credit per term."]
}

# Test function for Page 3
@pytest.mark.parametrize("question, expected_keywords", expected_responses_page3.items())
def test_chatbot_page3_responses(question, expected_keywords):
    response = get_response(question)  # Call the real model function
    # Check that at least one expected keyword is in the response
    assert any(keyword in response for keyword in expected_keywords), f"For '{question}', expected one of {expected_keywords} but got '{response}'"
