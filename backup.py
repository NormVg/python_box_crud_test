import os,io
from box_sdk_gen import BoxClient, BoxDeveloperTokenAuth
from box_sdk_gen.managers.uploads import UploadFileAttributes, UploadFileAttributesParentField
from box_sdk_gen.managers.folders import CreateFolderParent
from tqdm import tqdm

import re

import multiprocessing

# Authentication
dev_token = "VTNMlwfEzzua7S1Ibp9KVBCYfKSnbTtL"
my_music_root_id = "303632286123"

auth = BoxDeveloperTokenAuth(token=dev_token)
client = BoxClient(auth=auth)


def sanitize_folder_name(folder_name: str) -> str:

    """Remove invalid characters and trim whitespace for Box folder names."""

    # Remove non-printable ASCII characters
    folder_name = re.sub(r'[^\x20-\x7E]', '', folder_name)

    # Remove /, \, and double backslashes
    folder_name = re.sub(r'[\\/]', '', folder_name)

    # Strip leading and trailing whitespace
    folder_name = folder_name.strip()

    # Remove Unicode characters outside the Basic Multilingual Plane
    folder_name = ''.join(c for c in folder_name if ord(c) <= 0xFFFF)

    # # Check if the name is not "." or ".."
    # if folder_name in {'.', '..'}:
    #     raise ValueError('The special folder names "." and ".." are not allowed.')

    return folder_name




def upload_local_file(file_path: str, box_folder_id: str):
    """Upload a file to Box."""
    with open(file_path, 'rb') as file:
        file_content = file.read()
    file_name = os.path.basename(file_path)
    file_name = sanitize_folder_name(file_name)
    client.uploads.upload_file(
        UploadFileAttributes(
            name=file_name,
            parent=UploadFileAttributesParentField(id=box_folder_id)
        ),
        io.BytesIO(file_content)
    )


def Backup_Folder(local_folder_path: str, box_folder_id: str = "0"):
    """
    Backs up a local folder to Box while preserving the folder structure and skipping hidden files/folders.
    Includes a loading indicator for progress.
    
    :param local_folder_path: Path to the local folder to back up.
    :param box_folder_id: The ID of the Box folder where the backup will be created.
    """
    # Collect all files and folders to show a proper progress bar
    total_files = 0
    for root, dirs, files in os.walk(local_folder_path):
        dirs[:] = [d for d in dirs if not d.startswith(".")]
        total_files += len([f for f in files if not f.startswith(".")])

    with tqdm(total=total_files, desc="Backing up files", unit="file") as progress_bar:
        for root, dirs, files in os.walk(local_folder_path):
            # Filter out hidden directories
            dirs[:] = [d for d in dirs if not d.startswith(".")]
            # Compute the relative path to preserve structure
            rel_path = os.path.relpath(root, local_folder_path)

            # Skip the base folder's path (".")
            if rel_path == ".":
                rel_path = ""

            # Create corresponding folder on Box
            current_box_folder_id = box_folder_id
            if rel_path:  # Create subfolder if not the root folder
                folder_names = rel_path.split(os.sep)
                for folder_name in folder_names:
                    # Check if the folder already exists in Box
                    existing_folders = client.folders.get_folder_items(current_box_folder_id).entries
                    folder_exists = next((f for f in existing_folders if f.type == "folder" and f.name == folder_name), None)

                    if folder_exists:
                        current_box_folder_id = folder_exists.id
                    else:
                        # Create the folder if it doesn't exist
                        sanitized_folder_name = sanitize_folder_name(folder_name)
                        new_folder = client.folders.create_folder(sanitized_folder_name, CreateFolderParent(id=current_box_folder_id))
                        current_box_folder_id = new_folder.id

            # Upload files in the current directory




            for file_name in files:
                if not file_name.startswith("."):  # Skip hidden files
                    
                    local_file_path = os.path.join(root, file_name)
                    print(file_name)
                    upload_local_file(local_file_path, current_box_folder_id)
                    progress_bar.update(1)

# Example usage
Backup_Folder("/home/vishnu/Music/My Music/Hip Hop/void", my_music_root_id)
