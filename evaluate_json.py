import json
import os
from nervaluate import Evaluator
expected_json_directory = "data/receipts/json/expected"
actual_json_directory = "data/receipts/json/actual"
receipt_txt_directory = "data/receipts/text"

def find_span(text, entity_text, label):
    start = text.find(entity_text)
    if start == -1:
        return None
    end = start + len(entity_text)
    return {"start": start, "end": end, "label": label}

def recursive_entity_parse(json_dict, receipt_text):
    output = []
    for element in json_dict:
        if(type(json_dict[element]) == dict or type(json_dict[element]) == list):
            output.append(recursive_entity_parse(json_dict[element], receipt_text))
        elif(type(json_dict[element]) == str):
            output.append(find_span(json_dict[element], receipt_text, element.upper()))
        else:
            output.append(find_span(str(json_dict[element]), receipt_text, element.upper()))         
    return output

def make_txt_dict(path):
    output = {}
    for f in os.scandir(path):
        if(".txt" in f.name):
            file = open(f)
            data = file.read()
            file.close()
            output[f.name.replace(".txt", "")] = data
    return output

def make_json_file_dict(path):
    output = {}
    for f in os.scandir(path):
        if(".json" in f.name):
            file = open(f)
            json.load(file)
            key = f.name.replace(".json", "")
            output[key] = file
            f.close()
    return output

receipts = make_txt_dict(receipt_txt_directory)
expected = make_json_file_dict(expected_json_directory)
actual = make_json_file_dict(actual_json_directory)
evaluations = {}

for element in expected:
    if(element in actual and element in receipts):
        evaluations[element] = Evaluator(recursive_entity_parse(actual[element], receipts[element]),
                                         recursive_entity_parse(expected[element], receipts[element]),
                                         tags=['MERCHANT', 'UNITPRICE']).evaluate()
        print(evaluations[element])

