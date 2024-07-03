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
def generate_table_of_contents(content):
    toc = []
    for section, subsections in content.items():
        toc.append(f"# {section}\n")
        for subsection in subsections:
            toc.append(f"## {subsection}\n")
    return "\n".join(toc)

# Function to get section content dynamically from the Ollama API
def get_section_content_from_api(section_title, subsection_title):
    url = "http://localhost:11434/api/generate"  # Corrected endpoint
    headers = {
        "Content-Type": "application/json"
    }
    prompt = f"Generate detailed content for the section '{section_title}' with subsection '{subsection_title}', including code examples and explanations."
    payload = {
        "prompt": prompt,
        "model": "mistral",
        "stream": False
    }
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return f"Error fetching content for {subsection_title}: {e}"

    return response.json()["text"]

# Function to generate sections with subsections, code examples, and explanations
def generate_section(title, subsections):
    section_content = f"## {title}\n\n"
    for subsection in subsections:
        content = get_section_content_from_api(title, subsection)
        section_content += f"### {subsection}\n"
        section_content += f"{content}\n\n"
    return section_content

# Main function to generate the course content and write it to a Markdown file
def main():
    course_content = get_course_content_from_api()
    if not course_content:
        print("Error: Unable to generate course content.")
        return

    toc = generate_table_of_contents(course_content)

    with open("course_content.md", "w") as file:
        file.write("# Table of Contents\n\n")
        file.write(toc + "\n\n")
        for section, subsections in course_content.items():
            if subsections:
                file.write(f"## {section}\n\n")
                for subsection in subsections:
                    content = get_section_content_from_api(section, subsection)
                    file.write(f"### {subsection}\n")
                    file.write(f"{content}\n\n")

if __name__ == "__main__":
    main()
