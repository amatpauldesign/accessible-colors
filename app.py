import streamlit as st
from accessible_colors import contrast_ratio, pill

with open("styles.css", "r", encoding="utf-8") as f:
    css = f.read()

st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

col1, col2 = st.columns([11, 1])
with col1:
    st.title("Accessible Colors")
with col2:
    if st.button("", icon=":material/info:", type="tertiary", help="About"):
        with open(f"README.md", "r", encoding="utf-8") as f:
            md_text = f.read()
        # Display it in Streamlit
        @st.dialog("About", width="medium")
        def about_dialog():
            st.markdown(md_text)
        about_dialog()

st.caption("A simple tool for evaluating color contrast and accessibility. Created by [Paul Amat](https://paulamatdesign.github.io/).")

st.space()

st.header("Contrast Ratio Checker")

# Single row: left = color controls + preview, right = compliance
left_col, right_col = st.columns([4, 3], gap="large")

with left_col:
    colA, colB, colC = st.columns([1, 1, 1])
    with colA:
        hex_front = st.color_picker("Front", "#1A1A1A")
    with colB:
        hex_back = st.color_picker("Back", "#E6E6E6")
    st.markdown("")
    st.html(
        f"""
            <div class='exemple' style='background-color:{hex_back}; color:{hex_front};'>Preview</div>
        """
        )

with right_col:
    level = st.segmented_control("Compliance levels", ["AA", "AAA"], label_visibility="collapsed", default="AA")

    ratio = contrast_ratio(hex_front, hex_back)
    AA_met = ratio >= 4.5
    AAA_met = ratio >= 7.0

    AA_met_color = "green" if AA_met else "red"
    AAA_met_color = "green" if AAA_met else "red"

    if level == "AA":
        pill("Met" if AA_met else "Not Met", AA_met_color)

        colA, colB = st.columns(2)
        with colA:
            st.caption("Contrast Ratio")
        with colB:
            st.write(round(ratio, 1))

        colA, colB = st.columns(2)
        with colA:
            st.caption("Needed Ratio")
        with colB:
            st.write(4.5)
    else:
        pill("Met" if AAA_met else "Not Met", AAA_met_color)
        
        colA, colB = st.columns(2)
        with colA:
            st.caption("Contrast Ratio")
        with colB:
            st.write(round(ratio, 1))

        colA, colB = st.columns(2)
        with colA:
            st.caption("Needed Ratio")
        with colB:
            st.write(7.0)

st.space()
