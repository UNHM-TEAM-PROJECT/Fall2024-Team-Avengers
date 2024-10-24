import pytest

# Expected responses for Page 6
expected_responses_page6 = {
    "Where can I find UNH's academic integrity policy?": "The syllabus provides a link to the UNH Academic Integrity Policy.",
    "What's the policy on reporting sexual violence or harassment?": "Faculty are required to report; students can access confidential support services.",
    "How can I report sexual violence or harassment confidentially?": "Contact the SHARPP Center.",
    "What confidential support resources are available at UNH Manchester?": "The SHARPP Extended Services Coordinator, YWCA NH, and the Mental Health Center of Greater Manchester.",
    "What are the contact details for the UNH Manchester Title IX Deputy Intake Coordinator?": "The syllabus provides this information.",
    "What library resources are available in Manchester?": "Assistance with research and access to various online resources.",
    "How do I contact the UNH Manchester library?": "Phone: 603-641-4173 or Email: unhm.library@unh.edu",
    "How do I schedule a research appointment with a librarian?": "The syllabus provides a link to instructions on how to schedule a research appointment.",
    "How do I use the library's search box?": "The syllabus provides a link to instructions on how to use the library search box.",
    "How can I reserve a study room?": "The syllabus provides a link to instructions on reserving a study room.",
    "Where can I find resources for citing sources?": "The syllabus provides a link to resources for citing sources.",
    "What's the UNH Manchester Library website?": "UNH Manchester Library.",
    "Where can I find resources for evaluating sources?": "The syllabus provides a link to resources for evaluating sources.",
    "What's the phone number for the SHARPP Center?": "(603) 862-7233/TTY (800) 735-2964",
    "How can I report bias, discrimination, or harassment?": "Contact UNH's Civil Rights & Equity Office.",
    "What are the contact details for the UNH Title IX Coordinator?": "The syllabus provides this information.",
    "What app provides access to reporting options and resources?": "uSafeUS",
    "Where can I find the UNH Academic Integrity Policy?": "A link to the policy is provided in the syllabus.",
    "Where can I find more information about reporting procedures?": "The syllabus mentions information on student reporting options is available.",
    "What's the number for the 24-hour NH Domestic Violence Hotline?": "1-866-644-3574"
}

# Placeholder function for chatbot response
def chatbot_response(question):
    return expected_responses_page6.get(question, "Response not found")

# Test cases for Page 6
@pytest.mark.parametrize("question, expected_answer", expected_responses_page6.items())
def test_chatbot_page6_responses(question, expected_answer):
    response = chatbot_response(question)
    assert response == expected_answer, f"For '{question}', expected '{expected_answer}' but got '{response}'"
