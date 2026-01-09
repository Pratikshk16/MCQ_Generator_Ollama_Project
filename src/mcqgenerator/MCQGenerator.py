import os
import json
import traceback
import pandas as pd
from src.mcqgenerator.logger import logging
from src.mcqgenerator.utils import read_file, get_table_data

from langchain.prompts import PromptTemplate
from langchain_community.chat_models import ChatOllama
from langchain.chains import LLMChain

llm = ChatOllama(
    model="phi3:mini",
    temperature=0.2,
    num_ctx=1024
)

TEMPLATE = """
Text:
{text}

You are an expert MCQ maker. Given the above text, it is your job to
create a quiz of {number} multiple choice questions for {subject} students in {tone} tone.

Make sure the questions are not repeated.
Ensure all questions strictly conform to the provided text.
Format your response exactly like RESPONSE_JSON below and use it as a guide.
Ensure to generate exactly {number} MCQs.

### RESPONSE_JSON
{response_json}
"""

quiz_generation_prompt = PromptTemplate(
    input_variables=["text", "number", "subject", "tone", "response_json"],
    template=TEMPLATE
)

quiz_chain = quiz_generation_prompt | llm

TEMPLATE2 = """
You are an expert English grammarian and writer.
Given a Multiple Choice Quiz for {subject} students:

You need to evaluate the complexity of the questions and give a complete analysis of the quiz.
Use at most 50 words for the complexity analysis.

If the quiz is not at par with the cognitive and analytical abilities of the students,
update the quiz questions that need to be changed and adjust the tone so that it perfectly
fits the students’ abilities.

Quiz_MCQs:
{quiz}

Check from an expert English writer of the above quiz:
"""

quiz_evaluation_prompt = PromptTemplate(
    input_variables=["subject", "quiz"],
    template=TEMPLATE2
)

review_chain = quiz_evaluation_prompt | llm

def generate_evaluate_chain(inputs, review=True):
    quiz = quiz_chain.invoke(inputs).content
    if not review:
        return {"quiz": quiz}

    review_text = review_chain.invoke({
        "subject": inputs["subject"],
        "quiz": quiz
    }).content

    return {"quiz": quiz, "review": review_text}