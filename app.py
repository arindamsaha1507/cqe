"""Streamlit app for CQE."""

import streamlit as st

import cqe


def create_input_label(name, unit) -> str:
    """Input number."""

    label = f"# **{name}** ({unit})"
    return label


st.title("Hello World")

st.write("Welcome to my first Streamlit app!")

inputs = {}

for prop in cqe.get_all_property_names():
    if prop == "Ratio":
        continue

    inputs[prop] = st.number_input(create_input_label(prop, cqe.units[prop]))

if st.button("Calculate"):
    compost = cqe.Compost(inputs)

    st.write(compost.check_compliance())
    st.write(compost.get_fertility_index())
    st.write(compost.get_clean_index())
    st.write(compost.get_grade())

else:
    st.write("Click the button to calculate!")
