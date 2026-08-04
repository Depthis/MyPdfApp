import streamlit as st
import pdf_inspector

st.set_page_config(page_title="📄 Мой PDF Ридер", layout="wide")

st.title("📄 Мой PDF Ридер")
st.write("Анализ и извлечение текста из PDF-файлов")

# Загрузка файла
uploaded_file = st.file_uploader("Выберите PDF с телефона", type=["pdf"])

if uploaded_file is not None:
    # Читаем файлы в байтах (как в твоем примере: process_pdf_bytes)
    pdf_bytes = uploaded_file.read()

    with st.spinner("Обработка документа..."):
        # Полный анализ через pdf_inspector
        result = pdf_inspector.process_pdf_bytes(pdf_bytes)

    st.success("Файл успешно обработан!")

    # --- Сводная информация ---
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Тип PDF", result.pdf_type)
    with col2:
        st.metric("Уверенность", f"{result.confidence * 100:.0f}%")
    with col3:
        st.metric("Количество страниц", result.page_count)

    st.divider()

    # --- Вкладки с результатами ---
    tab1, tab2, tab3 = st.tabs(["📝 Извлечённый Markdown", "📑 Постраничный анализ", "🎯 Позиции текста"])

    # Вкладка 1: Полный Markdown
    with tab1:
        st.subheader("Форматированный текст (Markdown)")
        if result.markdown:
            st.markdown(result.markdown)
            st.download_button(
                label="Скачать Markdown",
                data=result.markdown,
                file_name="extracted_text.md",
                mime="text/markdown"
            )
        else:
            st.warning("Не удалось извлечь Markdown-текст или файл является сканом.")

    # Вкладка 2: Анализ по страницам
    with tab2:
        st.subheader("Информация по каждой странице")
        # Сохраняем во временный файл для функций, работающих с путями
        with open("temp_doc.pdf", "wb") as f:
            f.write(pdf_bytes)

        pages_result = pdf_inspector.extract_pages_markdown("temp_doc.pdf")
        for p in pages_result.pages:
            with st.expander(f"Страница {p.page + 1}"):
                st.write(f"**Символов:** {len(p.markdown)}")
                st.write(f"**Требуется OCR:** {'Да' if p.needs_ocr else 'Нет'}")
                st.text_area("Текст страницы", value=p.markdown, height=150, key=f"page_{p.page}")

    # Вкладка 3: Координаты и шрифты
    with tab3:
        st.subheader("Первые 15 фрагментов с координатами")
        items = pdf_inspector.extract_text_with_positions("temp_doc.pdf")
        
        position_data = []
        for item in items[:15]:
            position_data.append({
                "Текст": item.text,
                "X": round(item.x),
                "Y": round(item.y),
                "Размер шрифта": item.font_size
            })
        
        st.table(position_data)
      
