import pytest

# Expected responses for Page 2
expected_responses_page2 = {
    "What happens in week 1?": "Class introduction, team setup, project management intro, scrum workflow intro, and project goal.",
    "When is the project kickoff?": "Week 2 (September 4th)",
    "When does the first sprint begin?": "Week 4 (September 18th)",
    "How often are scrum meetings during the first sprint?": "Monday, Wednesday, and Friday.",
    "When does the first sprint end?": "Week 6 (October 2nd)",
    "What's involved in a sprint retrospective?": "Reviewing the sprint and identifying areas for improvement.",
    "When is the second sprint planning meeting?": "Week 7 (October 9th)",
    "When does the second sprint start?": "Week 7 (October 9th)",
    "Does the scrum meeting schedule change during the second sprint?": "Yes, the frequency changes throughout the course.",
    "When is Thanksgiving Break?": "Week 13 (November 20th).",
    "What's the focus of week 3?": "Environment setup (Jira), creating the project backlog, user stories, tasks, and bugs; integration with source control, team communication, and a sprint planning meeting.",
    "When are scrum meetings held only on Mondays?": "During Week 6 (10/2) and Week 11 (11/6)",
    "What happens during week 10?": "Scrum meetings (Monday, Wednesday, Friday).",
    "When is the sprint review for the first sprint?": "Week 6 (October 2nd)",
    "What are the activities for Week 9?": "Scrum meetings (Monday, Wednesday, Friday).",
    "When does the third sprint start?": "Week 12 (November 13th)",
    "How often are scrum meetings in week 13?": "Monday, Wednesday, and Friday; plus a weekly status report.",
    "What is the project goal (referencing information from page 1)?": "[Summarize the project goal from page 1, which describes the hands-on experience and contribution to real-world IT products/services.]",
    "What tools are used for project management?": "Jira is mentioned in the syllabus.",
    "What is the purpose of sprint planning?": "To create a plan for the upcoming sprint based on the Product Backlog."
}

# Placeholder function for chatbot response
def chatbot_response(question):
    return expected_responses_page2.get(question, "Response not found")

# Test cases for Page 2
@pytest.mark.parametrize("question, expected_answer", expected_responses_page2.items())
def test_chatbot_page2_responses(question, expected_answer):
    response = chatbot_response(question)
    assert response == expected_answer, f"For '{question}', expected '{expected_answer}' but got '{response}'"
