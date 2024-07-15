# import requests
# from requests.adapters import HTTPAdapter
# from urllib3.util.retry import Retry
# import logging
# import json

# logging.basicConfig(level=logging.DEBUG)

# def get_course_content_from_api():
#     url = "http://localhost:11434/api/generate"
#     headers = {"Content-Type": "application/json"}
#     prompt = "Generate a comprehensive table of contents for a Terminal course, including main sections, subsections, lessons, exercises, and context, in a JSON format."
#     payload = {"prompt": prompt, "model": "mistral", "stream": False}

#     # Configure retry strategy
#     retry_strategy = Retry(
#         total=3,  # Number of retries
#         backoff_factor=2,  # Exponential backoff factor
#         status_forcelist=[500, 502, 503, 504],  # Retry on these status codes
#     )
#     adapter = HTTPAdapter(max_retries=retry_strategy)
    
#     with requests.Session() as session:
#         session.mount('http://', adapter)
#         try:
#             response = session.post(url, headers=headers, json=payload, timeout=32000)
#             response.raise_for_status()
#             json_data = response.json()
#         except requests.exceptions.RequestException as e:
#             logging.error(f"Error fetching course content: {e}")
#             return {}
#         except json.JSONDecodeError as e:
#             logging.error(f"Error decoding JSON response: {e}")
#             return {}

#     logging.debug("Initial API response: %s", json_data)
#     return json_data

# def parse_and_convert_to_markdown(course_content):
#     def recurse_content(content, level=1):
#         md = ""
#         if isinstance(content, dict):
#             for key, value in content.items():
#                 md += f"{'#' * level} {key}\n\n"
#                 md += recurse_content(value, level + 1)
#         elif isinstance(content, list):
#             for item in content:
#                 if isinstance(item, dict):
#                     md += recurse_content(item, level)
#                 else:
#                     md += f"- {item}\n"
#         else:
#             md += f"{content}\n\n"
#         return md

#     return recurse_content(course_content)

# def save_to_markdown_file(content, filename="course_content.md"):
#     with open(filename, 'w', encoding='utf-8') as file:
#         file.write(content)
#     logging.info(f"Course content written to {filename}")

# def main():
#     course_content = get_course_content_from_api()
#     if course_content:
#         logging.info("Course content received successfully.")
#         markdown_content = parse_and_convert_to_markdown(course_content)
#         save_to_markdown_file(markdown_content)
#     else:
#         logging.error("No course content received.")

# if __name__ == "__main__":
# #     main()import requests
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import logging
import json

logging.basicConfig(level=logging.DEBUG)

def get_course_content_from_api():
    url = "http://localhost:11434/api/generate"
    headers = {"Content-Type": "application/json"}
    prompt = "Generate a comprehensive table of contents for a Terminal course, including main sections, subsections, and context, in a JSON format."
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
