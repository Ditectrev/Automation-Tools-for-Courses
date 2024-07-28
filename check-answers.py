import re
import requests

# FIXME: still far from perfect, often marks answers incorrect. Microsoft Bing Copilot is much more precise.
# Function to call the locally running Ollama service
def call_ollama_service(data):
    data = {
        "model": "mistral",
    }
    response = requests.post('http://localhost:11434/api/generate', json=data)
    return response.json()

# Read the README.md file
with open('README.md', 'r') as file:
    content = file.read()

# Extract questions and correct answers
questions = re.findall(r'### (.+?)\n\n(.+?)\n\n- \[(x| )\]', content, re.DOTALL)

# Iterate through each question and marked answer
for i, (question, answers, marked) in enumerate(questions, start=1):
    answer_lines = answers.split('\n')
    correct_answer_index = None

    # Find the index of the correct answer
    for index, line in enumerate(answer_lines):
        if '- [x]' in line:
            correct_answer_index = index
            break

    # Convert index to letter (A, B, C, D, ...)
    correct_answer_letter = chr(65 + correct_answer_index) if correct_answer_index is not None else 'None'

    # Check if the marked answer is correct
    if marked != 'x':
        # Call the locally running Ollama service
        result = call_ollama_service({
            'question': question,
            'marked_answer': marked,
            'correct_answer': correct_answer_letter
        })
        print(f'Question {i} has a different marked answer: {marked} (Correct answer: {correct_answer_letter})')
