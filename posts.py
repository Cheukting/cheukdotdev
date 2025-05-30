import os
import re
import shutil


def get_md_filenames(directory="content/posts"):
    """
    Scans the specified directory for markdown files (.md) and returns a list of their filenames.
    """
    return [file for file in os.listdir(directory) if file.endswith(".md")]


def organize_md_files(directory="content/posts"):
    """
    Organizes .md files in the specified directory by creating a folder for each file
    and renaming the file to '_index.md'.
    """
    md_files = get_md_filenames(directory)
    for file in md_files:
        # Remove .md to get the folder name
        folder_name = os.path.splitext(file)[0]
        folder_path = os.path.join(directory, folder_name)
        os.makedirs(folder_path, exist_ok=True)  # Create folder if it doesn't exist

        # Read the contents of the file to extract the front matter
        old_file_path = os.path.join(directory, file)
        with open(old_file_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Use regex to extract the image path from the front matter
        image_match = re.search(r'image:\s*(["\']?(.*?\.(jpg|png|jpeg|gif))["\']?|[^"\']\S+\.(jpg|png|jpeg|gif))',
                                content, re.IGNORECASE)
        if image_match:
            image_path = image_match.group(1)[1:]

            # If the image path is valid, move the image to the new folder
            if os.path.isfile(image_path):
                # Rename the image file by adding "feature_" to the beginning of the file name
                new_image_name = "feature_" + os.path.basename(image_path)
                new_image_path = os.path.join(folder_path, new_image_name)
                shutil.move(image_path, new_image_path)

        # Move and rename the file
        old_file_path = os.path.join(directory, file)
        new_file_path = os.path.join(folder_path, "_index.md")
        os.rename(old_file_path, new_file_path)


# Organize markdown files in the directory
# organize_md_files()

def rename_index_files(directory="content/posts"):
    """
    Renames all '_index.md' files to '_index.md' in the specified directory.
    """
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file == "_index.md":
                old_file_path = os.path.join(root, file)
                new_file_path = os.path.join(root, "_index.md")
                os.rename(old_file_path, new_file_path)

# Rename '_index.md' files to '_index.md'
# rename_index_files()

def generate_safe_filename(title):
    """
    Generate a URL-safe filename using vid and title.
    """
    safe_title = re.sub(r'[^\w\s-]', '', title).strip().replace(' ', '_')
    safe_title = safe_title.lower()
    return safe_title

print(generate_safe_filename("Migrate my website contents from Jekyll to Hugo with good prompts"))