import asyncio
import json
import os
import threading

import boxsdk.object.file
from docusign_esign import EnvelopesApi

from box_auth import boxAuth
from docusign_auth import dsauth
from upload_files import uploadFile

threads = []
def lambda_handler(event, context):
    try:
        print('### event')
        print(event)
        envelope_id = event['envelopeId']
        documents = event['documents']

        ds_client = dsauth()
        box_client = boxAuth()
        envelope_api = EnvelopesApi(ds_client)
        folder_id = ""
        contract = documents[0]['name']
        result = asyncio.run(main(box_client, contract, documents, envelope_api, envelope_id))
        print(result)

        return {
            'status': 200,
            'body': 'Done'
        }
    except Exception as e:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Error, bad request!', 'log': str(e), 'event': event})
        }


async def main(box_client, contract, documents, envelope_api, envelope_id):
    tasks = []
    for document in documents:
        task = asyncio.create_task(download_and_send(box_client, contract, document, envelope_api, envelope_id))
        tasks.append(task)
    await asyncio.gather(*tasks)
    print(threads)
    # Wait for all to complete
    for thread in threads:
        thread.join()
    print("Completed")


async def download_and_send(box_client, contract, document, envelope_api, envelope_id):
    def callback_docusing(docusing_document):
        print(docusing_document)
        upload_to_box(docusing_document)

    def upload_to_box(docusing_document):
        try:
            file_folder = os.path.dirname(docusing_document)
            file_name = f"{document_name}.pdf"
            file_path = os.path.join(file_folder, file_name)
            print(file_path)
            os.rename(docusing_document, file_path)
            file: boxsdk.object.file.File = uploadFile(boxClient=box_client, filePath=file_path, folderID=folder_id)
            os.remove(file_path)
            print(f'file {file_name} uploaded')
        except Exception as e:
            print(e)

    document_name = document['name']
    if document_name.startswith('Procura'):
        document_name = document_name + "_" + contract
        folder_id = '18731439245'
    elif document_name.startswith('DH'):
        document_name = document_name + "_" + contract
        folder_id = '18731439245'
    elif document_name == "Summary":
        return
    else:
        folder_id = '14686953579'
    thread: threading.Thread = envelope_api.get_document(
        account_id='57ba9986-6592-497a-adfc-13a604b379a7',
        document_id=document['documentId'], envelope_id=envelope_id, callback=callback_docusing)
    print(thread)
    threads.append(thread)
