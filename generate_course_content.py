import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import logging
import json

logging.basicConfig(level=logging.DEBUG)

def get_course_content_from_api():
    url = "http://localhost:11434/api/generate"
    headers = {"Content-Type": "application/json"}
    # Use first prompt to generate table of contents, then use second prompt to generate every single section of it.
    prompt = "Generate the most detailed table of contents for HTML educational course you can do. It should be a base for a book explaining this technology from A to Z. Please do it in Markdown format. Please don't use numberings in heading syntax."
    #prompt = "Generate content for 'SECTION_OF_GENERATE_TOC' It should contain best practices, From this table of contents generate a book. The book should include main sections, subsections, and context. Context should have a comprehensive paragraph explaining particular subsections, along with code examples. It should be so much detailed a student could use it an A to Z guide for this technology. I want to see a couple of thousands of lines of Markdown code. Everything should be in Markdown format. Please don't use numberings in heading syntax. Please make new lines after every level of Markdown heading, such as '#', '##', '###', '####', '#####', and '######'."
    payload = {"prompt": prompt, "model": "mistral", "stream": False}

    # Configure retry strategy
    retry_strategy = Retry(
        total=3,  # Number of retries
        backoff_factor=2,  # Exponential backoff factor
        status_forcelist=[500, 502, 503, 504],  # Retry on these status codes
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)

    with requests.Session() as session:
        session.mount('http://', adapter)
        try:
            response = session.post(url, headers=headers, json=payload, timeout=32000)
            response.raise_for_status()
            json_data = response.json()
        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching course content: {e}")
            return {}
        except json.JSONDecodeError as e:
            logging.error(f"Error decoding JSON response: {e}")
            return {}

    logging.debug("Initial API response: %s", json_data)
    return json_data

def parse_and_convert_to_markdown(course_content):
    def recurse_content(content, level=1):
        md = ""
        if isinstance(content, dict):
            for key, value in content.items():
                md += f"{'#' * level} {key}\n\n"
                md += recurse_content(value, level + 1)
        elif isinstance(content, list):
            for item in content:
                if isinstance(item, dict):
                    md += recurse_content(item, level + 1)
                else:
                    md += f"- {item}\n"
        else:
            md += f"{content}\n\n"
        return md

    return recurse_content(course_content)

def save_to_markdown_file(content, filename="course_content.md"):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(content)
    logging.info(f"Course content written to {filename}")

def main():
    course_content = get_course_content_from_api()
    if course_content:
        logging.info("Course content received successfully.")
        if 'response' in course_content:
            markdown_content = parse_and_convert_to_markdown(course_content['response'])
            save_to_markdown_file(markdown_content)
        else:
            logging.error("Expected 'response' key in the course content JSON.")
    else:
        logging.error("No course content received.")

if __name__ == "__main__":
    main()
