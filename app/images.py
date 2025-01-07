import streamlit as st

def generate_boxes(status, labels, colors, width, height): 
    num = len(labels) + 1
    labels = ['TOTAL'] + labels  # Prefix TOTAL to the labels list
    label_count = [
        status.count(label) if label != 'TOTAL' else len(status) for label in labels
    ]   
    
    # Estilo CSS para os quadrados com bordas arredondadas
    st.markdown(f"""
        <style>
            .container {{
                display: flex;
                justify-content: space-between;
                width: {(width + 20)*num}px;
                margin: 0 auto;
                gap: 20px;
            }}
            .box {{
                width: {width}px;
                height: {height}px;
                background-color: green;
                border-radius: 20px;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                text-align: center;
                padding: 10px;
            }}
            .label {{
                font-size: 30px;
                color: black;
            }}
            .number {{
                font-size: 70px;
                color: black;
            }}
        </style>
        <div class="container">
            {"".join([f"<div style='background-color: {colors[_]};' class='box'>"
                      f"<div class='label'>{labels[_]}</div>"
                      f"<div class='number'>{label_count[_]}</div>"
                      f"</div>" for _ in range(num)])}
        </div>
    """, unsafe_allow_html=True)