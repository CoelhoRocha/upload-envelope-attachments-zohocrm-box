import os

import boxsdk.object.folder
import boxsdk.object.file
import boxsdk.client
from boxsdk.exception import BoxAPIException
import requests as requests
import json
from boxsdk import OAuth2, Client




def uploadFile(boxClient: boxsdk.client.Client, folderID, filePath):
    # Set Folder ID
    try:
        upload_folder: boxsdk.object.folder.Folder = boxClient.folder(folderID)
    except BoxAPIException as e:
        print(e)
    #Upload File or New Version
    try:
        new_file: boxsdk.object.file.File = upload_folder.upload(filePath, preflight_check=True)
        file_id = new_file.id
    except BoxAPIException as e:
        if 'conflicts' not in e.context_info:
            print(e)
        else:
            file_id = e.context_info['conflicts']['id']
            new_file = boxClient.file(file_id).update_contents(filePath)
    return new_file
