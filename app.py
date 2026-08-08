import streamlit as st
from access_colors import contrast_ratio, pill, preview
from color_contrast import modulate, ModulationMode

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
        @st.dialog("About", width="medium")
        def about_dialog():
            st.markdown(md_text)
        about_dialog()

st.caption("A simple homemade tool for evaluating color contrast and accessibility.")

st.space()

st.header("Contrast Ratio Checker")

left_col, right_col = st.columns([4, 3], gap="large")

with left_col:
    colA, colB, colC = st.columns([1, 1, 1])
    with colA:
        hex_front = st.color_picker("Front", "#1A1A1A")
    with colB:
        hex_back = st.color_picker("Back", "#E6E6E6")
    st.markdown("")
    preview(hex_front, hex_back)

with right_col:
    with st.container(border=True):
        level = st.segmented_control("Compliance levels", ["AA", "AAA"], label_visibility="collapsed", default="AA")

        ratio = contrast_ratio(hex_front, hex_back)
        AA_level = 4.5
        AAA_level = 7.0
        AA_met = ratio >= AA_level
        AAA_met = ratio >= AAA_level
    
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
                st.write(AA_level)
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
                st.write(AAA_level)

st.space()

st.header("Suggested Colors")

new_back = modulate(hex_front, hex_back, mode=ModulationMode.BACKGROUND, level=AA_level if level == "AA" else AAA_level)[1]
new_front = modulate(hex_front, hex_back, mode=ModulationMode.FOREGROUND, level=AA_level if level == "AA" else AAA_level)[0]

left_col, right_col = st.columns(2, gap="large")

with left_col:
    with st.container(border=True):
        colA, colB = st.columns(2)
        with colA:
            st.caption("New Background Color")
            st.write(new_back)
        with colB:
            preview(hex_front, new_back)

with right_col:
    with st.container(border=True):
        colA, colB = st.columns(2)
        with colA:
            st.caption("New Foreground Color")
            st.write(new_front)
        with colB:
            preview(new_front, hex_back)
