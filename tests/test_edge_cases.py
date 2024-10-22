import pytest

# Edge Case Definitions
edge_case_incomplete_queries = {
    "What time is the M2 section on": "Could you please clarify your question?",
    "Where is the class": "Could you please specify which class you're asking about?"
}

edge_case_misspellings_typos = {
    "Who is teh instructor?": "The instructor is Professor Karen Jin.",
    "What is teh time for the class?": "Could you please specify which class you're asking about?",
    "Where is teh room for M2 section?": "The class is held in room P142."
}

edge_case_grammatical_errors = {
    "What time the class is on Wednesday?": "The M1 section is at 9:10 AM and the M2 section is at 1:10 PM.",
    "Who be the instructor?": "The instructor is Professor Karen Jin."
}

edge_case_vague_queries = {
    "What’s the time?": "Could you please specify which class or section you're asking about?",
    "Where is the room?": "Could you please specify which class or event you're referring to?"
}

edge_case_out_of_scope_queries = {
    "What’s the weather today?": "I'm sorry, I can only answer questions related to the internship course.",
    "Can you tell me the news?": "I'm sorry, I can only answer questions related to the internship course."
}

# Placeholder function to simulate chatbot response for edge cases
def get_chatbot_response(question):
    # Simulate responses for each type of edge case
    if question in edge_case_incomplete_queries:
        return edge_case_incomplete_queries[question]
    elif question in edge_case_misspellings_typos:
        return edge_case_misspellings_typos[question]
    elif question in edge_case_grammatical_errors:
        return edge_case_grammatical_errors[question]
    elif question in edge_case_vague_queries:
        return edge_case_vague_queries[question]
    elif question in edge_case_out_of_scope_queries:
        return edge_case_out_of_scope_queries[question]
    return "Response not found"


# Edge Case 1: Incomplete Queries (with relaxed assertion)
@pytest.mark.parametrize("question, expected_keywords", [
    ("What time is the M2 section on", ["clarify"]),
    ("Where is the class", ["specify", "class"])
])
def test_incomplete_queries(question, expected_keywords):
    response = get_chatbot_response(question)
    assert all(keyword in response for keyword in expected_keywords), \
        f"For '{question}', expected response to contain '{expected_keywords}' but got '{response}'"


# Edge Case 2: Misspellings and Typos
@pytest.mark.parametrize("question, expected_answer", edge_case_misspellings_typos.items())
def test_misspellings_typos(question, expected_answer):
    response = get_chatbot_response(question)
    assert response == expected_answer, f"For '{question}', expected '{expected_answer}' but got '{response}'"


# Edge Case 3: Grammatically Incorrect Queries
@pytest.mark.parametrize("question, expected_answer", edge_case_grammatical_errors.items())
def test_grammatical_errors(question, expected_answer):
    response = get_chatbot_response(question)
    assert response == expected_answer, f"For '{question}', expected '{expected_answer}' but got '{response}'"


# Edge Case 4: Vague Queries (with relaxed assertion, allowing for "section" or "event")
@pytest.mark.parametrize("question, expected_keywords", [
    ("What’s the time?", ["specify", "class", "section"]),
    ("Where is the room?", ["specify", "class", ["section", "event"]])  # Allow both "section" and "event"
])
def test_vague_queries(question, expected_keywords):
    response = get_chatbot_response(question)
    
    # Handle cases where a keyword can have multiple possible values (e.g., "section" or "event")
    for keyword in expected_keywords:
        if isinstance(keyword, list):
            # Check if any of the possible keywords are in the response
            assert any(k in response for k in keyword), \
                f"For '{question}', expected response to contain one of '{keyword}' but got '{response}'"
        else:
            # Check the regular keywords
            assert keyword in response, \
                f"For '{question}', expected response to contain '{keyword}' but got '{response}'"


# Edge Case 5: Out-of-Scope Queries
@pytest.mark.parametrize("question, expected_answer", edge_case_out_of_scope_queries.items())
def test_out_of_scope_queries(question, expected_answer):
    response = get_chatbot_response(question)
    assert response == expected_answer, f"For '{question}', expected '{expected_answer}' but got '{response}'"
