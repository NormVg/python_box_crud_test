from box_sdk_gen import BoxClient, BoxDeveloperTokenAuth
from box_sdk_gen.managers.uploads import UploadFileAttributes
from box_sdk_gen.managers.uploads import UploadFileAttributesParentField
from box_sdk_gen.managers.folders import CreateFolderParent

import os, io


dev_token = "YOUR DEVELOPER TOKEN"
my_music_root_id = "303528265620"

auth: BoxDeveloperTokenAuth = BoxDeveloperTokenAuth(token=dev_token)
client: BoxClient = BoxClient(auth=auth)



# GET ALL FILES : done
# GET FILE DOWNLOAD : done
# UPLOAD FILE : done
# UPLOAD FOLDER 
# DELETE FILE : done
# DELETE FOLDER : done 
# CREATE FOLDER : done


def get_Walk_All_File(id:str = "0"):
    for item in client.folders.get_folder_items(id).entries:
        if item.type == "folder":
            print("<---",item.name,"--->")
            get_Walk_All_File(item.id)
        else:
            print(item.name)


def Upload_Local_File(file_path,to_id:str = "0"):

    with open(file_path, 'rb') as file:
        file_content = file.read()

    file_content_stream = io.BytesIO(file_content)
    file_name = os.path.basename(file_path)

    client.uploads.upload_file(
        UploadFileAttributes(
            name=file_name, parent=UploadFileAttributesParentField(id=to_id)
        ),
        file_content_stream,
    )
    
    
def Create_Folder(folder_name:str,to_id:str = "0"):
    client.folders.create_folder(folder_name, CreateFolderParent(id=to_id))

def Delete_Folder(folder_id):
    client.folders.delete_folder_by_id(folder_id)

def Delete_File(file_id):
    client.files.delete_file_by_id(file_id)

def Get_Download_Link(file_id:str):
    link = client.downloads.get_download_file_url(file_id)
    return link

