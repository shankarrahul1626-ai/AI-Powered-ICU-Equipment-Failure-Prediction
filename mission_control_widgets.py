import streamlit as st
import pandas as pd
import numpy as np

def pulse_monitor():

    pulse = pd.DataFrame(
        np.random.randn(60).cumsum(),
        columns=["ICU Pulse"]
    )

    st.line_chart(
        pulse,
        width='stretch'
    )
