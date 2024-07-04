import requests
import json

# Modify the get_course_content_from_api function to parse JSON response before processing
def get_course_content_from_api():
    url = "http://localhost:11434/api/generate"  # Corrected endpoint
    headers = {
        "Content-Type": "application/json"
    }
    prompt = "Generate a comprehensive table of contents for an HTML course, including main sections and subsections, in a JSON format."
    payload = {
        "prompt": prompt,
        "model": "mistral",
        "stream": False
    }
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching course content: {e}")
        return {}

    json_data = response.json()  # Parse JSON response
    content = json_data.get("response", "No response found")
    course_content = {}
    current_section = ""
    for line in content.split("\n"):
        if line.strip() and not line.startswith(" "):
            current_section = line.strip()
            course_content[current_section] = []
        elif line.strip():
            if current_section:
                course_content[current_section].append(line.strip())
    return course_content

# Function to generate the table of contents
def generate_table_of_contents(content, file_path):
    with open(file_path, "w") as file:
        file.write("# Table of Contents\n\n")
        for section, subsections in content.items():
            file.write(f"## {section}\n")
            for subsection in subsections:
                file.write(f"### {subsection}\n")

# Function to get section content dynamically from the Ollama API
def get_section_content_from_api(section_title, subsection_title):
    if section_title is not None and subsection_title is not None:
        print('Section: ', section_title)
        print('Subsection: ', subsection_title)
        url = "http://localhost:11434/api/generate"  # Corrected endpoint
        headers = {
            "Content-Type": "application/json"
        }
        prompt = f"Generate detailed content for '{subsection_title}', including code examples and explanations. Code examples should be displayed correctly in a Markdown file with highlighted syntax as per code snippet language."
        payload = {
            "prompt": prompt,
            "model": "mistral",
            "stream": False
        }
        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            return f"Error fetching content for {subsection_title}: {e}"

        response_data = response.json()
        if 'text' in response_data:
            return response_data['text']
        else:
            # Handle the case when 'text' key is not present in the response
            return None  # or raise an exception, depending on your requirements

# Main function to generate the course content and write it to a Markdown file
def main():
    course_content = get_course_content_from_api()
    if not course_content:
        print("Error: Unable to generate course content.")
        return

    generate_table_of_contents(course_content, "course_content.md")

    with open("course_content.md", "w") as file:
        for section, subsections in course_content.items():
            if subsections:
                file.write(f"## {section}\n\n")
                for subsection in subsections:
                    content = get_section_content_from_api(section, subsection)
                    print('content: ', content)
                    if content is not None and "text" in content:
                        file.write(f"### {subsection}\n\n")
                        file.write(f"{content['text']}\n\n")
                    else:
                        file.write(f"### {subsection}\n")
                        file.write(f"No content available\n\n")

if __name__ == "__main__":
    main()
