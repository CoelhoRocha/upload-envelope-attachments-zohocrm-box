import boxsdk.object.file
import boxsdk.object.metadata_template
import boxsdk.client
from boxsdk.exception import BoxAPIException


def setFileMetadata(boxClient: boxsdk.client.Client, file: boxsdk.object.file.File, metadata, template):
    try:
        boxClient.file(file.object_id).metadata(scope='enterprise_1760289', template=template).set(metadata)
    except BoxAPIException as e:
        if 'exists for group' not in e.context_info:
            print(e)
        else:
            boxClient.file(file.object_id).metadata(scope='enterprise_1760289', template=template).delete()
            boxClient.file(file.object_id).metadata(scope='enterprise_1760289', template=template).set(metadata)