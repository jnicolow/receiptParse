from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI


model = ChatOpenAI(model='gpt-3.5-turbo')

prompt_str="""
What is the tallest building in state of {state}? Only respond with the name of the building.
"""

prompt = PromptTemplate.from_template(prompt_str)
print(prompt.format(**{'state':'Michigan'})) # you dont have to unpact input when calling chain.invoke


chain = prompt | model # how to pass the prompt to the model (pipe prompt to model)
response = chain.invoke({'state':'hawaii'}) # no variables are passed so input dictionary is empty

print(response.content)


#### JSON
import json

prompt_str="""
What is the tallest building in state of {state}? Only respond with the name of the building.

state: Michigan
{{"City":"Detriot"}}

state: Hawaii
{{"City":"Honolulu"}}

{state}
"""

# notice that we have to do double {{ because single { is used for the variables in the promps


chain = prompt | model # how to pass the prompt to the model (pipe prompt to model)
response = chain.invoke({'state':'Florida'}) # no variables are passed so input dictionary is empty

print(response.content)

d = json.load(response)
d["City"]

#### one way to provide helpful examples is to get the embeding of the users question and the example questions and see which one it is closest to and use that as the example
prompt_examples = [
    {"ExampleState":"Hawaii", "ExampleCity":"Honolulu"},
    ......
    {etc......}
]


examples_prompt_str = "State: {ExampleState}\nCity: {ExampleCity"
examples_prompt_str.format(**promt_examples[0]) # you could then do a for loop for these but there is an easier way but look below for better way


#### FewShot
from langchain.prompts.few_shot import FewShotPromptTemplate

prompt_prefix = "What is the tallest building in state provided below? Provide no additional information."


example_prompt = PromptTemplate(input_variables=["ExampleState", "ExampleCity"], template=example_prompt_str)

FewShotPromptTemplate(
    prefix = prompt_prefix,
    input_variables = ["state"],
    examples = prompt_examples,
    example_prompt=example_prompt,
    example_separator= "/n/n",
    suffix = "State: {state}"



