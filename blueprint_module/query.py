from openai import OpenAI
from flask import request, jsonify
from . import blueprint
from blueprint_module import blueprint
from dotenv import load_dotenv
import os
import json

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI API
api_key = os.getenv("api_key")

import re


def remove_prefix(text):
    # Strip leading/trailing whitespace
    text = text.strip()
    
    # Regular expression to match prefixes
    # This regex matches:
    # 1. One or more words (letters, numbers, underscores)
    # 2. Optionally followed by single quotes, double quotes, or triple quotes
    # 3. At the start of the string
    prefix_pattern = r'^(\w+\s*)+[\'"""]*'
    
    # Remove the prefix
    cleaned_text = re.sub(prefix_pattern, '', text)
    
    # Strip any leading/trailing quotes and whitespace
    cleaned_text = cleaned_text.strip('\'"'' ')
    
    return cleaned_text





# OpenAI Prompt Parameters
AI_ROLE = """You are GradeAI, a replacement for teachers in a High School, located in North America.
You are a trained expert on writing and literary analysis. Your job is to accurately and effectively grade a student's essay and give them helpful feedback according to the assignment prompt."""

SYSTEM_INSTRUCTIONS = """Assess the student's assignment based on the provided rubric.
Respond back with graded points and a level for each criteria. Don't rewrite the rubric in order to save processing power. In the end, write short feedback about what steps they might take to improve on their assignment. Write a total percentage grade and letter grade. In your overall response, try to be lenient and keep in mind that the student is still learning. While grading the essay remember the writing level the student is at while considering their course level, grade level, and the overall expectations of writing should be producing.
Your grade should only be below 70% if the essay does not succeed at all in any of the criteria. Your grade should only be below 80% if the essay is not sufficient in most of the criteria. Your grade should only be below 90% if there are a few criteria where the essay doesn't excell. Your grade should only be above 90% if the essay succeeds in most of the criteria.
Understand that the essay was written by a human and think about their writing expectations for their grade level/course level, be lenient and give the student the benefit of the doubt.

Additionally, provide a Reliability Index, which is a score from 0 to 100 indicating how confident you are in your assessment of the essay. A score of 0 means you have no confidence in your assessment, while a score of 100 means you are completely confident in your assessment.

Give me your entire response in JSON format for easy processing.
Response Format:
[
    {"Criteria": "...", "Level": "4", "Feedback": "Student must..."},
    {"Grade": "B", "Percentage": "85%"},
    {"Feedback": "Some suggestions to improve..."},
    {"ReliabilityIndex": 85}
]
where you create a Criteria object for each individual criteria, Grade represents the overall assignment grade, Feedback is a list of bullet points regarding the specific suggestions in their essay with references to examples in the essay, and ReliabilityIndex is your confidence score in the assessment.
"""


@blueprint.route("/query_essay", methods=["POST"])
def query_essay():
    """
    POST /query_essay

    Assess a student's essay and provide graded points, levels, and feedback.
    """
    """
    Assess a student's essay and provide graded points, levels, and feedback.

    Args:
        COURSE_INFORMATION (str): Information about the course.
        RUBRIC (str): The rubric for grading the essay.
        ASSIGNMENT_INSTRUCTIONS (str): Instructions for the assignment.
        ESSAY (str): The student's essay.

    Returns:
        dict: A JSON response containing graded points, levels, feedback, and overall grade.
              The response is in the following format:
              [{"Criteria": "...", "Level": "4", "Feedback": "Student must..."}, {"Grade": "B", "Percentage": "75%"}]
              Each individual criterion is represented by a Criteria object, and the Grade represents the overall assignment grade.
    """

    data = request.get_json()

    required_parameters = [
        "course_information",
        "rubric",
        "assignment_instructions",
        "essay",
    ]

    for parameter in required_parameters:
        if parameter not in data:
            return f'"{parameter}" JSON Parameter Missing', 400

    COURSE_INFORMATION = data.get("course_information")
    RUBRIC = data.get("rubric")
    ASSIGNMENT_INSTRUCTIONS = data.get("assignment_instructions")
    ESSAY = data.get("essay")

    prompt = f"""
System Instructions:
{SYSTEM_INSTRUCTIONS}

Course Information:
{COURSE_INFORMATION}

Rubric:
{RUBRIC}

Assignment Instructions:
{ASSIGNMENT_INSTRUCTIONS}

Essay:
{ESSAY}
"""

    # Query response from OpenAI
    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": AI_ROLE,
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.1,
        top_p=0.3,
        # response_format=jsonify
    )
    response = response.choices[0].message.content
    cleaned_text = re.sub(r'(```json?|json```|\`{3})', '', response)
    import ast
    cleaned_text = ast.literal_eval(cleaned_text)
    return jsonify(cleaned_text)



    # Return OpenAI response in JSON format
    # return response


