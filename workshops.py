import yaml
import re
import os
import requests


def read_workshops_yml():
    with open("workshops.yml", "r") as file:
        return yaml.safe_load(file)


def convert_md_to_text(md_text):
    """
    Convert markdown text to plain text by removing markdown formatting.
    :param md_text: Markdown-formatted string.
    :return: Plain text string.
    """
    md_text = re.sub(r"\[", "", md_text)  # Remove opening square brackets
    md_text = re.sub(r"\]", " ", md_text)  # Replace closing square brackets with a space
    md_text = re.sub(r"^>+\s*", "", md_text, flags=re.MULTILINE)  # Remove blockquote symbols (>) and leading spaces
    md_text = re.sub(r"^\s+", "", md_text, flags=re.MULTILINE)  # Strip extra spaces at the beginning of each line
    return md_text


def generate_front_matter(data):
    """
    Generate a front matter string from a list of dictionaries, converting descriptions to plain text.
    :param data: List of dictionaries.
    :return: A list of YAML strings, each representing the front matter of an item.
    """
    front_matters = []
    for item in data:
        item["description"] = convert_md_to_text(item["quote"])
        front_matter = "---\n" + yaml.dump(item, default_flow_style=False) + "---\n"
        front_matters.append(front_matter)
    return front_matters


def generate_safe_filename(title):
    """
    Generate a URL-safe filename using vid and title.
    """
    safe_title = re.sub(r'[^\w\s-]', '', title).strip().replace(' ', '_')
    return safe_title


for item in read_workshops_yml():
    item["description"] = convert_md_to_text(item["description"])
    item["title"] = item["name"]
    for key in ["name", "quote", "qualification", "layout"]:
        item.pop(key, None)
    if not isinstance(item.get("tags", []), list):
        item["tags"] = [item["tags"]] if item["tags"] else []
    front_matter = "---\n" + yaml.dump(item, default_flow_style=False) + "---\n"
    link = item.get("link", "")
    
    if link.startswith("https://slides.com/"):
            text = f"""
<iframe src="{link}/embed" width="576" height="420" title="{item['title']}" scrolling="no" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen></iframe>
"""
    elif link.startswith("https://github.com/"):
        git_repo = link.replace("https://github.com/", "").strip()
        text = f"""
{{{{< github repo="{git_repo}" >}}}}
"""
    else:
        test = ""

    end_text = f"""
{item["description"]}
---
Consider [buying me a coffee {{{{< icon "mug-hot" >}}}}](https://github.com/sponsors/Cheukting) if you love the content.
"""
    filename = generate_safe_filename(item['title'])
    directory = os.path.join("content/workshops", filename)
    os.makedirs(directory, exist_ok=True)
    file_path = os.path.join(directory, "index.md")
    with open(file_path, "w") as file:
        file.write(front_matter + text + end_text)
