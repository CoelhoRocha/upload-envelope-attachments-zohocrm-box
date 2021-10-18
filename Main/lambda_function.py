import asyncio
import json
import os
import threading
from datetime import datetime
import boxsdk.object.file
from docusign_esign import EnvelopesApi
from box_file_metadata import setFileMetadata
from box_auth import boxAuth
from docusign_auth import dsauth
from upload_files import uploadFile
import re

threads = []
def lambda_handler(event, context):
    try:
        print('### event')
        print(event)
        envelope_id = event['envelopeId']
        documents = event['documents']
        contratantes = event['contratantes']
        servico = event['servico']


        ds_client = dsauth()
        box_client = boxAuth()
        envelope_api = EnvelopesApi(ds_client)
        folder_id = ""
        contract = documents[0]['name']
        result = asyncio.run(main(box_client, contract, documents, envelope_api, envelope_id, contratantes, servico))
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


async def main(box_client, contract, documents, envelope_api, envelope_id, contratantes, servico):
    tasks = []
    for document in documents:
        task = asyncio.create_task(download_and_send(box_client, contract, document, envelope_api,
                                                     envelope_id, contratantes, servico))
        tasks.append(task)
    await asyncio.gather(*tasks)
    print(threads)
    # Wait for all to complete
    for thread in threads:
        thread.join()
    print("Completed")


async def download_and_send(box_client, contract, document, envelope_api, envelope_id,
                            contratantes, servico):
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
            setFileMetadata(box_client, file, metadata, metadataTemplate)
            os.remove(file_path)
            print(f'file {file_name} uploaded')
        except Exception as e:
            print(e)

    metadata = ''
    metadataTemplate = 'instrumentosDeMandato'
    document_name = document['name']
    if document_name.startswith('Procura'):
        document_name = document_name + "_" + contract
        metadata = {
            'outorgados': 'Luiz Rocha',
            'dataDaOutorga': datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
            'tipo1': 'Procuração',
            'outorgantes': re.match(r'.*_(.*)_', document['name']).group(1),
            'idDoContrato': contract}

        folder_id = '18731439245'
    elif document_name.startswith('DH'):
        document_name = "Declaração de Hipossuficiência_" + \
                        re.match(r'.*_(.*)_', document['name']).group(1) + "_" + contract
        metadata = {
            'outorgados': 'Luiz Rocha',
            'dataDaOutorga': datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
            'tipo1': 'Declaração de Hipossuficiência',
            'outorgantes': re.match(r'.*_(.*)_', document['name']).group(1),
            'idDoContrato': contract}
        folder_id = '18731439245'
    elif document_name == "Summary":
        return
    else:
        metadata = {
            'objeto': servico,
            'tipo': 'Contrato de Prestação de Serviço',
            'idDoContrato': document_name,
            'dataDeAssinatura': datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
            'contratantes': contratantes}
        metadataTemplate = 'contatosDeServio'
        folder_id = '14686953579'
    thread: threading.Thread = envelope_api.get_document(
        account_id='57ba9986-6592-497a-adfc-13a604b379a7',
        document_id=document['documentId'], envelope_id=envelope_id, callback=callback_docusing)
    print(thread)
    threads.append(thread)
