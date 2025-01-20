from box_sdk_gen import BoxClient, BoxCCGAuth, CCGConfig



#this is  going to be in the server
ccg_config = CCGConfig(
    client_id="",
    client_secret="",
    user_id="",
)
auth = BoxCCGAuth(config=ccg_config)
client = BoxClient(auth=auth)


def get_Walk_All_File(id:str = "0"):
    for item in client.folders.get_folder_items(id).entries:
        if item.type == "folder":
            print("<---",item.name,"--->")
            get_Walk_All_File(item.id)
        else:
            print(item.name)


get_Walk_All_File()

