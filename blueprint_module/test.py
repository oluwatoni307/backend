import requests
import json

# URL of your Flask application
url = 'http://localhost:5000/query_essay'

# Sample data for testing
test_data = {
    "course_information": "Grade 12 English AP",
    "rubric": """
    <table>
        <tr>
            <th>Criteria</th>
            <th>Level 1</th>
            <th>Level 2</th>
            <th>Level 3</th>
            <th>Level 4</th>
        </tr>
        <tr>
            <td>Thesis</td>
            <td>Weak or no thesis</td>
            <td>Basic thesis</td>
            <td>Clear thesis</td>
            <td>Strong, insightful thesis</td>
        </tr>
        <tr>
            <td>Evidence</td>
            <td>Little or no evidence</td>
            <td>Some evidence</td>
            <td>Relevant evidence</td>
            <td>Comprehensive evidence</td>
        </tr>
    </table>
    """,
    "assignment_instructions": "Write a persuasive essay on the importance of reading in today's digital age.",
    "essay": """
    Reading is a fundamental skill that remains crucial in our digital age. Despite the prevalence of technology, the ability to read and comprehend text is more important than ever. Books provide a depth of knowledge and perspective that is often lacking in quick online content. Moreover, reading improves vocabulary, enhances critical thinking, and fosters imagination. In a world of short attention spans, the act of reading a book cultivates patience and focus. While digital media has its place, the immersive experience of reading a physical book is unparalleled. Therefore, we must continue to promote and value reading as an essential activity for personal growth and societal progress.
    """
}

# Send POST request
response = requests.post(url, json=test_data)

# Check if the request was successful
if response.status_code == 200:
    # Print the response JSON
    print(json.dumps(response.json(), indent=2))
else:
    print(f"Error: {response.status_code}")
    print(response.text)