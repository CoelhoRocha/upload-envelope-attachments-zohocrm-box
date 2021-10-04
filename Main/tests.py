
import json
import os.path

from Main.lambda_function import lambda_handler

# event = json.load(open('../Event/Event.json'))
with open('../Event/Event.json', encoding='utf-8') as f:
    event = json.load(f)

# print(event)

# print(event)
lambda_handler(event, '')

# document = r"C:\Users\LuizRocha\AppData\Local\Temp\test.pdf"
# print(os.path.dirname(document))
# fileName = os.path.join(os.path.split(document)[0], 'test2.pdf')
# os.rename(document, fileName)
# print(fileName)