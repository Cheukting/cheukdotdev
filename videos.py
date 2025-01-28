import yaml
import re
import os
import requests

def read_videos_yml():
    with open("videos.yml", "r") as file:
        return yaml.safe_load(file)

def generate_front_matter(data):
    """
    Generate a front matter string from a list of dictionaries.
    :param data: List of dictionaries.
    :return: A list of YAML strings, each representing the front matter of an item.
    """
    front_matters = []
    for item in data:
        front_matter = "---\n" + yaml.dump(item, default_flow_style=False) + "---\n"
        front_matters.append(front_matter)
    return front_matters
    
def generate_safe_filename(vid, title):
    """
    Generate a URL-safe filename using vid and title.
    """
    safe_title = re.sub(r'[^\w\s-]', '', title).strip().replace(' ', '_')
    safe_filename = f"{vid}_{safe_title}"
    return safe_filename

for item in read_videos_yml()[:1]:
    front_matter = "---\n" + yaml.dump(item, default_flow_style=False) + "params:\n  showHero: false\n---\n"
    html = f"""
<iframe width="630" height="472"
src="https://www.youtube.com/embed/{item['vid']}">
</iframe>
<br/>
<p>{item['description']}</p>"""
    filename = generate_safe_filename(item['vid'], item['title'])
    directory = os.path.join("output", filename)
    os.makedirs(directory, exist_ok=True)
    file_path = os.path.join(directory, "index.html")
    with open(file_path, "w") as file:
        file.write(front_matter + html)
    thumnail_url = f"https://img.youtube.com/vi/{item['vid']}/hqdefault.jpg"
    thumbnail_response = requests.get(thumnail_url)
    if thumbnail_response.status_code == 200:
        thumbnail_path = os.path.join(directory, "feature_thumbnail.jpg")
        with open(thumbnail_path, "wb") as thumbnail_file:
            thumbnail_file.write(thumbnail_response.content)
