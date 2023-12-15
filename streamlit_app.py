import streamlit as st
import pandas as pd
from evaluate_json import *

expected_json_directory = "data/receipts/json/expected"
actual_json_directory = "data/receipts/json/prompt2"
receipt_txt_directory = "data/receipts/text"
tag_list = ['MERCHANT', 'TOTAL', 'DESCRIPTION', 'QUANTITY']
nerv_dict = do_nervaluation_from_dir(receipt_txt_directory, expected_json_directory, actual_json_directory, tag_list)

st.title('Receipt Parse')
st.subheader('Nervaluate')
st.text('Using several prompts, we were able to generate valid json files from the receipt text. \nHere are the results of our running nervaluate on our outputted json files.')
if st.checkbox('Show Individual Nervaluate Results'):
    for element in nerv_dict:
        st.text(element)
        df = pd.DataFrame.from_dict(nerv_dict[element])
        st.dataframe(df, use_container_width=True)

chart_dict = {"correct":0, "incorrect":0, "partial":0, "missed":0}
for element in nerv_dict:
    for item in chart_dict:
        chart_dict[item] += nerv_dict[element]["strict"][item]
st.bar_chart(chart_dict)
st.text('Here are all of out notebooks: ')
with open("convert_testset_to_json.ipynb", 'rb') as file:
    st.download_button(label="Convert Testset to JSON notebook", data=file, file_name="convert_testset_to_json.ipynb")
with open("item_classification.ipynb", 'rb') as file:
    st.download_button(label="Item classification notebook", data=file, file_name="item_classification.ipynb")
with open("LLM_get_structured_data.ipynb", 'rb') as file:
    st.download_button(label="Get structured data with LLM", data=file, file_name="LLM_get_structured_data.ipynb")
