import requests
import json

# Function to get course content from API
def get_course_content_from_api():
    url = "http://localhost:11434/api/generate"
    headers = {"Content-Type": "application/json"}
    prompt = "Generate a comprehensive table of contents for a Terminal course, including main sections and subsections, in a JSON format."
    payload = {"prompt": prompt, "model": "mistral", "stream": False, "format": "json"}
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        json_data = response.json()
        print('response JSON:', json_data)  # Debug line
    except requests.exceptions.RequestException as e:
        print(f"Error fetching course content: {e}")
        return {}
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON response: {e}")
        return {}

    content = json_data.get("response", "")
    
    # Debug: Print the raw content string
    print('Raw nested JSON content:', content)  # Debug line

    # Parse the nested JSON string in the "response" field
    try:
        # Handle potential multiline JSON strings
        content = content.replace('\n', '').replace('\r', '')
        content_json = json.loads(content)
        print('Parsed nested JSON content:', content_json)  # Debug line
    except json.JSONDecodeError as e:
        print(f"Error decoding nested JSON content: {e}")
        return {}

    return parse_course_content(content_json)

# Function to parse course content into structured format
def parse_course_content(content):
    table_of_contents = content.get("Table of Contents", {})
    print('Parsed Table of Contents:', table_of_contents)  # Debug line
    return table_of_contents

# Function to generate the table of contents in a Markdown file
def generate_table_of_contents(content, file_path):
    with open(file_path, "w") as file:
        file.write("# Table of Contents\n\n")
        for section, subsections in content.items():
            file.write(f"## {section}\n")
            for subsection in subsections:
                file.write(f"### {subsection}\n")

# Function to get section content dynamically from the ollama API
def get_section_content_from_api(section_title, subsection_title):
    if not section_title or not subsection_title:
        return "Invalid section or subsection title."

    url = "http://localhost:11434/api/generate"
    headers = {"Content-Type": "application/json"}
    prompt = f"Generate detailed content for '{subsection_title}', including code examples and explanations. Code examples should be displayed correctly in a Markdown file with highlighted syntax as per code snippet language, reply in JSON format."
    payload = {"prompt": prompt, "model": "mistral", "stream": True,  "raw": True, }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        response_data = response.json()
        return response_data.get('text', "No content available")
    except requests.exceptions.RequestException as e:
        return f"Error fetching content for {subsection_title}: {e}"
    except json.JSONDecodeError as e:
        return f"Error decoding JSON response: {e}"

# Main function to generate the course content and write it to a Markdown file
def main():
    course_content = get_course_content_from_api()
    if not course_content:
        print("Error: Unable to generate course content.")
        return

    generate_table_of_contents(course_content, "course_content.md")

    with open("course_content.md", "a") as file:  # Append to the file after the table of contents
        for section, subsections in course_content.items():
            file.write(f"## {section}\n\n")
            for subsection in subsections:
                content = get_section_content_from_api(section, subsection)
                print('Content:', content)  # Debug line
                file.write(f"### {subsection}\n\n")
                file.write(f"{content}\n\n")

if __name__ == "__main__":
    main()
