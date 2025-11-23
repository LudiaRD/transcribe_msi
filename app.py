%%writefile app.py
import streamlit as st
import whisper
import tempfile
from docx import Document
 
@st.cache_resource
def load_model(model_name: str):
     return whisper.load_model(model_name)
 
st.set_page_config(page_title = "Audio to Text (Whisper)", layout = "wide")
st.title("🎧 Transkripsi Audio ke Teks dengan Whisper")
 
st.markdown("""
             Upload file audio / video, sistem akan mengubahnya menjadi teks.
             Hasil bisa diunduh sebagai **.txt** atau **.docx (Word)**.
            """
            )
 
col1, col2 = st.columns(2)
with col1:
    model_name = st.selectbox("Pilih model Whisper",
                              ["tiny", "base", "small", "medium"],
                              index = 2,
                              help = "Semakin besar model, makin akurat tapi lebih lambat."
                             )
with col2:
    language = st.text_input("Kode bahasa audio (mis. 'id', 'en')", value = "id")
 
uploaded_file = st.file_uploader("Upload file audio / video", type = ["mp3", "wav", "m4a", "mp4", "mov", "mkv"])
 
if uploaded_file is not None:
    st.write(f"📁 File terpilih: **{uploaded_file.name}**")
 
    if st.button("Mulai Transkripsi"):
        with tempfile.NamedTemporaryFile(delete = False, suffix = uploaded_file.name) as tmp:
            tmp.write(uploaded_file.read())
            temp_path = tmp.name
 
        st.info("Memuat model, mohon tunggu...")
        model = load_model(model_name)
 
        st.info("Sedang mentranskripsi audio...")
        with st.spinner("Proses transkripsi sedang berjalan..."):
            result = model.transcribe(temp_path, language = language if language.strip() != ""else None)

        text = result.get("text", "").strip()
 
        if not text:
            st.error("Transkripsi kosong/gagal. Coba model lain atau cek file.")
        else:
            st.success("Transkripsi selesai!")

            st.subheader("Hasil Transkripsi")
            st.text_area("Teks", text, height = 300)

            # TXT
            txt_filename = (uploaded_file.name.rsplit(".", 1)[0] or "transkripsi") + ".txt"

            # DOCX
            doc = Document()
            doc.add_paragraph(text)
            import io
            docx_buffer = io.BytesIO()
            doc.save(docx_buffer)
            docx_buffer.seek(0)
            docx_filename = (uploaded_file.name.rsplit(".", 1)[0] or "transkripsi") + ".docx"

             st.subheader("Unduh Hasil")
             st.download_button("⬇️ Download .txt",
                                data = text,
                                file_name = txt_filename,
                                mime = "text/plain"
                               )
             st.download_button("⬇️ Download .docx (Word)",
                                data = docx_buffer,
                                file_name = docx_filename,
                                mime = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                               )
 else:
     st.info("Silakan upload file audio atau video terlebih dahulu.")
