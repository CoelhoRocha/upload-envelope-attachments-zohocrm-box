import json
import pytest
import os

from lambda_function import lambda_handler


@pytest.fixture(scope="function")
def event_fixture():
    base_dir = os.path.dirname(os.path.dirname(__file__))
    event_file = os.path.join(base_dir, "Event", "Event.json")
    with open(event_file, encoding="utf-8") as f:
        return json.load(f)


def test_lambda_handler(event_fixture):
    res = lambda_handler(event_fixture, "")
    assert res["statusCode"] == 200


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
