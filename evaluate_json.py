import json
import os
from nervaluate import Evaluator
expected_json_directory = "data/receipts/json/expected"
actual_json_directory = "data/receipts/json/actual"
receipt_txt_directory = "data/receipts/text"

def find_span(input, label, receipt_text):
    start = receipt_text.find(input)
    if start == -1:
        return []
    end = start + len(input)
    return [{"start": start, "end": end, "label": label}]

def recursive_entity_parse(input, label, receipt_text):
    if(type(input) == dict):
        output = []
        for element in input:
            output = output + (recursive_entity_parse(input[element], element, receipt_text))
        return output
    elif(type(input) == list):
        output = []
        for element in input:
            output = output + (recursive_entity_parse(element, '',  receipt_text))
        return output
    elif(type(input) == str):
        return find_span(input, label.upper(), receipt_text)
    else:
        return find_span(str(input), label.upper(), receipt_text)

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
            try:
                with open(f, "r") as fp:
                    data = json.load(fp)
                key = f.name.replace(".json", "")
                output[key] = data
            except:
                print("Error decoding json")
    return output

receipts = make_txt_dict(receipt_txt_directory)
expected = make_json_file_dict(expected_json_directory)
actual = make_json_file_dict(actual_json_directory)
evaluations = {}
tag_list = ['MECHANT']
for element in expected:
    if(element in actual and element in receipts):
        actual_parsed = recursive_entity_parse(actual[element], '', receipts[element])
        expected_parsed = recursive_entity_parse(expected[element], '', receipts[element])
        print(actual_parsed)
    evaluator = Evaluator(expected_parsed, actual_parsed, tags=tag_list)
    print(evaluator.evaluate())

