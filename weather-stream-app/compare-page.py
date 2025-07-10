import streamlit as st
import numpy as np

st.set_page_config(layout="wide")

col1, col2 = st.columns(2, border=True)



with col1:
    st.header("Location A")
    with st.expander("See explanation"):
        st.text_input( label="City name", placeholder="Type City name")

        svg_content = """<svg height="100" width="100">
        <circle cx="50" cy="50" r="40" stroke="black" stroke-width="3" fill="red" />
        </svg>
        """
        st.markdown(svg_content, unsafe_allow_html=True)
    with st.container():
        st.write("This is inside the container")

        # You can call any Streamlit command, including custom components:
        st.bar_chart(np.random.randn(50, 3), use_container_width=True)

        st.write("This is outside the container")

        

with col2:
    st.header("Location B")
    with st.expander("See explanation"):
        st.write('''
        The chart above shows some numbers I picked for you.
        I rolled actual dice for these, so they're *guaranteed* to
        be random.
        ''')
        st.image("https://static.streamlit.io/examples/dice.jpg")

