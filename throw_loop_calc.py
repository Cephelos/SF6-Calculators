import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Configure the page
st.set_page_config(
    page_title="Throw Loop Calc",
    page_icon="🔁",
    layout="wide"
)





# Add a title and description
st.title("Throw Loop Damage Calculator")
st.write("Input the relative likelihood of using each wakeup option on the left.")

# Sidebar for user inputs
# st.sidebar
options = ["parry", "block", "drive reversal", "dp", "forward jump", "neutral/back jump", "backdash", "jab", "wakeup low", "super"]

outcome = [1.7,1,0,0,0,1,0,1,1,0]
inputs = []
for option in options:
    inputs.append(0)

st.sidebar.header("Parameters:")


inputsDF = pd.DataFrame(data={"weight": inputs, "outcome": outcome}, index=options)
throw_damage = 1200
# Iterate through dataframe index and weight column
for idx in inputsDF.index:

    inputsDF.at[idx, 'weight'] = st.sidebar.number_input(idx,
        value=int(inputsDF.at[idx, 'weight']),
        key=f"weight_{idx}",
        label_visibility="visible"
    )

coloration = ""

escape = inputsDF[inputsDF["outcome"] == 0]
thrown = inputsDF[inputsDF["outcome"] == 1]
thrown_parry = inputsDF[inputsDF["outcome"] == 1.7]

for outcome in list(escape.index):

    coloration += f"""    [aria-label="{outcome}"]{{
            color: green;
        }}
        """
for outcome in list(thrown.index):

    coloration += f"""    [aria-label="{outcome}"]{{
            color: red;
        }}
        """
    
for outcome in list(thrown_parry.index):

    coloration += f"""    [aria-label="{outcome}"]{{
            color: orange;
        }}
        """

st.markdown(f"""
<style>
/* Style all number inputs */
.st-key-weight_* input {{
    color: red;
    font-weight: bold;
}}

/* Style specific element using custom key */
[class*="st-key-weight_"] {{
    padding: -1rem;
    margin: -0.5rem;
}}
{coloration}
</style>
""", unsafe_allow_html=True)
# Main content area with tabs
tab1, tab2 = st.tabs(["Plot", "Data"])

with tab1:
    # st.subheader("Function Visualization")

    # print([inputsDF["outcome"] == 1])
    # print(real_options)
    if sum(inputsDF['weight']) > 0:
        # First calculate the probability of each option being chosen
        probabilities = inputsDF['weight'] / sum(inputsDF['weight'])
        
        # Calculate thrown_rate based on whether the option leads to another throw (binary)
        thrown_rate = sum(probabilities * (inputsDF['outcome'] > 0))
        
        if thrown_rate >= 1:
            EV = "INF"
        else:
            # For the damage calculation, multiply each probability by its outcome value
            # times the throw damage
            base_damage = throw_damage * sum(probabilities * inputsDF['outcome'])
            EV = base_damage / (1-thrown_rate)

            thrown_rate = f"{thrown_rate: .2f}"
            EV = f"{EV: .2f}"
    else:
        thrown_rate = "NaN"
        EV = "NaN"
    
    # Using container for smoother updates
    container = st.container()
    with container:
        st.write(f"Escape Rate: {thrown_rate}")
        st.write(f"Expected Damage: {EV}")

with tab2:
    st.subheader("Data Table")
    st.dataframe(inputsDF)

# Add a footer
st.markdown("---")
st.markdown("Created with Streamlit")