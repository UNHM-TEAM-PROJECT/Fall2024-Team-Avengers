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


# Expected responses for Page 6
expected_responses_page6 = {
    "What is UNH's policy on academic integrity?": [
        "UNH Academic Integrity Policy is available online", "The chatbot cannot directly provide the policy but can direct you to the relevant link"
    ],
    "What is the policy regarding mandatory reporting of sexual violence or harassment?": [
        "Faculty members are required to report incidents of sexual violence or harassment", "report to the university's Title IX Coordinator"
    ],
    "How can I report sexual violence or harassment confidentially?": [
        "Contact the SHARPP Center for Interpersonal Violence Awareness", "Prevention", "Advocacy"
    ],
    "What resources are available for confidential support at UNH Manchester?": [
        "SHARPP Extended Services Coordinator", "YWCA NH", "Mental Health Center of Greater Manchester"
    ],
    "What are the contact details for the UNH Manchester Title IX Deputy Intake Coordinator?": [
        "Lisa Enright's email address (lisa.enright@unh.edu)", "Lisa Enright's phone number"
    ],
    "What resources are available at the UNH Manchester library?": [
        "Assistance with research", "access to online library resources"
    ],
    "How can I contact the UNH Manchester library?": [
        "Contact the library at 603-641-4173", "unhm.library@unh.edu"
    ],
    "How can I make a research appointment with a librarian?": [
        "The syllabus provides a link to instructions on making a research appointment", "The chatbot should ideally provide the link if available"
    ],
    "How can I use the library search box?": [
        "The syllabus provides a link to instructions on using the library search box", "The chatbot should ideally provide the link if available"
    ],
    "How can I reserve a study room?": [
        "The syllabus provides a link to instructions on reserving a study room", "The chatbot should ideally provide the link if available"
    ],
    "Where can I find resources for citing sources?": [
        "The syllabus provides a link to resources for citing sources", "The chatbot should ideally provide the link if available"
    ],
    "What is the website for the UNH Manchester Library?": [
        "The syllabus lists this information", "The chatbot should ideally provide the link if available"
    ],
    "What resources are available for evaluating sources?": [
        "The syllabus provides a link to resources for evaluating sources", "The chatbot should ideally provide the link if available"
    ],
    "What is the phone number of the SHARPP Center?": [
        "(603) 862-7233", "TTY (800) 735-2964"
    ],
    "What resources are available to report bias, discrimination, or harassment?": [
        "Contact the Civil Rights & Equity Office at UNH"
    ],
    "What are the contact details for the UNH Title IX Coordinator?": [
        "Bo Zaryckyj's email address (Bo.Zaryckyj@unh.edu)", "Bo Zaryckyj's phone number"
    ],
    "What is the name of the app that provides access to reporting options and resources?": ["uSafeUS"],
    "Where can I find the UNH Academic Integrity Policy?": [
        "The syllabus includes a link to the policy", "The chatbot should ideally provide the link if available"
    ],
    "Where can I find more information about what happens when I report an incident?": [
        "The syllabus mentions a page with information on student reporting options", "The chatbot should ideally reference this"
    ],
    "What is the phone number for the 24-hour NH Domestic Violence Hotline?": ["1-866-644-3574"]
}

# Test function for Page 6
@pytest.mark.parametrize("question, expected_keywords", expected_responses_page6.items())
def test_chatbot_page6_responses(question, expected_keywords):
    response = get_response(question)  # Call the real model function
    # Check that at least one expected keyword is in the response
    assert any(keyword in response for keyword in expected_keywords), f"For '{question}', expected one of {expected_keywords} but got '{response}'"
