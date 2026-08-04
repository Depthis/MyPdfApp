import streamlit as st
import tempfile
import os
import pdf_inspector

st.set_page_config(page_title="PDF Reader", layout="wide")
st.title("📄 Мой PDF Ридер")

uploaded_file = st.file_uploader("Выберите PDF с телефона", type=["pdf"])

if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(uploaded_file.getbuffer())
        tmp_path = tmp_file.name

    try:
        result = pdf_inspector.process_pdf(tmp_path)
        st.info(f"Тип документа: {result.pdf_type}")
        
        if result.markdown:
            st.markdown("---")
            st.markdown(result.markdown)
        else:
            st.warning("В файле не найден текст.")
    except Exception as e:
        st.error(f"Ошибка при обработке файла: {e}")
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
          
