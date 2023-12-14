import streamlit as st
import pandas as pd
import pygwalker as pyg
from evaluate_json import *

expected_json_directory = "data/receipts/json/expected"
actual_json_directory = "data/receipts/json/actual"
receipt_txt_directory = "data/receipts/text"
tags = ['MERCHANT']

nerv_dict = do_nervaluation_from_dir(receipt_txt_directory, expected_json_directory, actual_json_directory, tags)

st.title('Receipt Parse')

if st.checkbox('Show Individual Nervaluate Results'):
    for element in nerv_dict:
        st.text(element)
        df = pd.DataFrame.from_dict(nerv_dict[element])
        st.dataframe(df, use_container_width=True)

if st.checkbox('Show Nervaluate Results as a Bar Graph'):
    chart_dict = {"correct":0, "incorrect":0, "partial":0, "missed":0}
    for element in nerv_dict:
        for item in chart_dict:
            chart_dict[item] += nerv_dict[element]["strict"][item]
    st.bar_chart(chart_dict)
