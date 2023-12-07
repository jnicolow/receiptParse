import os
basename = os.path.basename(os.getcwd())
if basename == 'receiptParse':
    os.chdir(os.path.dirname(os.getcwd())) # this is important we have to change the working directory back one
elif 'ICS-438' in basename:
    os.chdir(os.path.join(os.getcwd(), 'receiptParse')) # 
print(os.getcwd())


import os
from glob import glob
import json

#### MODEL ####
from langchain.chat_models import ChatOpenAI
# jnicolowathawiiAPIkey = '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'
os.environ['OPENAI_API_KEY'] = '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'
model = ChatOpenAI(model='gpt-3.5-turbo')

#### Prompt ####
from langchain.prompts import PromptTemplate
from langchain.prompts.few_shot import FewShotPromptTemplate

# get examples
annotatorDirs = glob(os.path.join('data', 'receipts', 'annotations', '*'))
examples = []
for annotatorDir in annotatorDirs:
    jsonFiles = glob(os.path.join(annotatorDir, '*.json'))
    for jsonFile in jsonFiles:
        baseFn = jsonFile.replace('.json', '')
        txtFile = glob(f'{baseFn}.txt')[0]
        with open(jsonFile, 'r') as f: JSONobj = f.read()
        with open(txtFile, 'r') as f: rawRecieptText = f.read()
        exampleDict = {
            "rawRecieptText": rawRecieptText,
            "JSONobj":JSONobj.replace('{', '{{{{').replace('}', '}}}}')
            }
        examples.append(exampleDict)

example_prompt = PromptTemplate(input_variables=["rawRecieptText", "JSONobj"], 
                                template="""
Can you extract the applicable information from raw text of a recipt. This information should be put into a valid JSON object with the structure below:

{{{{
  "ReceiptInfo": {{{{
    "merchant": "(string value)",
    "address": "(string value)",
    "city": "(string value)",
    "state": "(string value)",
    "phoneNumber": "(string value)",
    "tax": "(float value)",
    "total": "(float value)",
    "receiptDate": "(string value)",
    "receiptTime": "(string value)",


    "ITEMS": [
      {{{{
        "description": "(string value)",
        "quantity": "(integer value)",
        "unitPrice": "(float value)",
        "totalPrice": "(float value)",
        "discountAmount": "(float value)"
      }}}}, ...
    ]
  }}}}
}}}}

The returned object should have all of these fields. If there is missing information the value should be null

Below is an example of first reciept text:

{rawRecieptText}

The JSON object for this example:
{JSONobj}
""")


prompt = FewShotPromptTemplate(
    examples=[examples[0]], # only do one shot for now
    example_prompt=example_prompt,
    suffix="Get JSON for this:\n{input}",
    input_variables=["input"]
)

print(prompt.format(input="recieptTxt"))


#### Create Chain ####
chain = prompt | model # how to pass the prompt to the model (pipe prompt to model)


#### Run inference on reciepts ####
prompt = 'test'
recieptFiles = glob(os.path.join('data', 'receipts', 'text', '*.txt'))
for recieptFn in recieptFiles:
    with open(recieptFn, 'r') as f: recieptTxt = f.read()
    response = chain.invoke({'input':recieptTxt})
    data_dict = json.loads(response.content)
    with open(os.path.join('data', 'receipts', 'json', f'{os.path.basename(recieptFn).split(".tx")[0]}_{prompt}.json'), 'w') as f: json.dump(data_dict, f)
    break
