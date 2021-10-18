import json
import re
from box_auth import boxAuth
from box_file_metadata import setFileMetadata
import boxsdk.object.metadata_template
from datetime import datetime
import os.path

from Main.lambda_function import lambda_handler

# event = json.load(open('../Event/Event.json'))
with open('../Event/Event.json', encoding='utf-8') as f:
    event = json.load(f)

# envelope_id = event['envelopeId']
# documents = event['documents']
# contratantes = event['contratantes']
# servico = event['servico']

# print(event)

# # print(event)
lambda_handler(event, '')


# Update metadata test
# boxClient = boxAuth()
# metadata = {
#     'objeto': '1Elaboração de Contrato de Compromisso de Compra e Venda -Imóveis 9.669 e 9.670',
#     'tipo': 'Contrato de Prestação de Serviço',
#     'idDoContrato': '1CA674',
#     'dataDeAssinatura': datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
#     'contratantes': '1Rodrigo Bartoli Machado'}

# metadata = {
#             'outorgados': 'Luiz Rocha',
#             'dataDaOutorga': datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
#             'tipo1': 'Procuração',
#             'outorgantes': re.match(r'.*_(.*)_', documents[1]['name']).group(1),
#             'idDoContrato': 'contractID'}
#
# boxFile: boxsdk.object.file.File = boxClient.file("873869022875")
# setFileMetadata(boxClient, boxFile, metadata, "instrumentosDeMandato")

# document = r"C:\Users\LuizRocha\AppData\Local\Temp\test.pdf"
# print(os.path.dirname(document))
# fileName = os.path.join(os.path.split(document)[0], 'test2.pdf')
# os.rename(document, fileName)
# print(fileName)
