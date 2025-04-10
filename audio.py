# Gerekli import'lar
import streamlit as st
from audio_recorder_streamlit import audio_recorder
import speech_recognition as sr
import io
import wave
from pydub import AudioSegment
from datetime import datetime
from fpdf import FPDF
import urllib.request
import os
import tempfile

# ------------------ FONT AYARLARI ------------------
FONT_NAME = "NotoSans-Regular"
FONT_FILE = f"{FONT_NAME}.ttf"
if not os.path.exists(FONT_FILE):
    try:
        urllib.request.urlretrieve(
            "https://github.com/googlefonts/noto-fonts/raw/main/hinted/ttf/NotoSans/NotoSans-Regular.ttf",
            FONT_FILE
        )
    except Exception as e:
        st.error(f"❌ Font indirme hatası: {str(e)}")

# ------------------ DİL DESTEĞİ ------------------
LANGUAGES = {
    "🇹🇷 Türkçe": {
        "title": "🎙️ Ses-Metin Dönüştürücü",
        "input_type": "🔊 Ses Kaynağı Seçin:",
        "options": ["📁 Dosya Yükle", "🎤 Canlı Kayıt"],
        "file_uploader": "📤 MP3/WAV dosyası yükleyin",
        "recording": "⏺️ KAYIT DEVAM EDİYOR",
        "duration": "⏱️ Kayıt Süresi",
        "transcript_label": "📝 Transkript",
        "processing": "⚙️ Transkript oluşturuluyor...",
        "error": "❌ Hata:",
        "requirements": "❗ Dikkat Edilmesi Gerekenler",
        "lang_code": "tr-TR",
        "download_txt": "📥 Metin Olarak İndir (.txt)",
        "download_pdf": "📄 PDF Olarak İndir (.pdf)",
        "edit_text": "✏️ Metin",
        "audio_label": "🎧 Ses",
        "output_label": "📤 Çıktı Dosyaları",
        "notes": [
            "🎤 Mikrofon erişimi",
            "🔊 Net ses",
            "🌍 İnternet bağlantısı"
        ],
        "info_title": "📌 Uygulama Kılavuzu",
        "info_content": """
        **🎯 Nasıl Kullanılır?**
        1. 🌐 Dil seçin (Türkçe/English)
        2. 🔊 Ses kaynağını seçin:
           - **📁 Dosya Yükle**: Bilgisayarınızdan MP3/WAV dosyası yükleyin
           - **🎤 Canlı Kayıt**: Mikrofonunuzla anlık ses kaydı yapın
        3. ⏳ Ses dosyasını yükledikten veya kaydettikten sonra transkript otomatik oluşturulacak
        4. 💾 Oluşan metni düzenleyip TXT veya PDF olarak indirebilirsiniz

        **✨ Özellikler**
        - 🌍 Çoklu dil desteği
        - 🔊 Ses önizleme
        - ✏️ Metin düzenleme
        - ⚡ Hızlı indirme seçenekleri
        """
    },
    "🇺🇸 English": {
        "title": "🎙️ Audio-Text Converter",
        "input_type": "🔊 Select Audio Source:",
        "options": ["📁 File Upload", "🎤 Live Recording"],
        "file_uploader": "📤 Upload MP3/WAV file",
        "recording": "⏺️ RECORDING IN PROGRESS",
        "duration": "⏱️ Recording Duration",
        "transcript_label": "📝 Transcript",
        "processing": "⚙️ Processing transcript...",
        "error": "❌ Error:",
        "requirements": "❗ Important Notes",
        "lang_code": "en-US",
        "download_txt": "📥 Download as Text (.txt)",
        "download_pdf": "📄 Download as PDF (.pdf)",
        "edit_text": "✏️ Text",
        "audio_label": "🎧 Audio",
        "output_label": "📤 Output Files",
        "notes": [
            "🎤 Microphone access",
            "🔊 Clear audio",
            "🌍 Internet connection"
        ],
        "info_title": "📌 Application Guide",
        "info_content": """
        **🎯 How to Use?**
        1. 🌐 Select language (English/Turkish)
        2. 🔊 Choose audio source:
           - **📁 File Upload**: Upload MP3/WAV file
           - **🎤 Live Recording**: Record live audio
        3. ⏳ After uploading/recording, transcript will be generated
        4. 💾 Edit text and download as TXT/PDF

        **✨ Features**
        - 🌍 Multi-language support
        - 🔊 Audio preview
        - ✏️ Text editing
        - ⚡ Quick download options
        """
    }
}

# ------------------ PDF FONKSİYONU ------------------
def create_pdf(text):
    """PDF oluşturma"""
    try:
        pdf = FPDF()
        pdf.add_page()
        pdf.add_font(FONT_NAME, '', FONT_FILE, uni=True)
        pdf.set_font(FONT_NAME, size=12)
        pdf.multi_cell(0, 10, text)
        return pdf.output(dest='S')
    
    except Exception as e:
        st.error(f"❌ PDF oluşturma hatası: {str(e)}")
        return b""

# ------------------ SESSION STATE ------------------
if 'recording' not in st.session_state:
    st.session_state.recording = False
if 'audio_data' not in st.session_state:
    st.session_state.audio_data = None
if 'language' not in st.session_state:
    st.session_state.language = "🇹🇷 Türkçe"  # Güncellendi
if 'transcript' not in st.session_state:
    st.session_state.transcript = ""
if 'file_uploaded' not in st.session_state:
    st.session_state.file_uploaded = False

# ------------------ YARDIMCI FONKSİYONLAR ------------------
def convert_to_wav(uploaded_file):
    file_type = uploaded_file.name.split('.')[-1].lower()
    with tempfile.NamedTemporaryFile(delete=False, suffix=f'.{file_type}') as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        tmp_path = tmp_file.name
    
    audio = AudioSegment.from_file(tmp_path)
    with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as wav_file:
        audio.export(wav_file.name, format="wav")
        return wav_file.name

def process_audio(file_path, language):
    r = sr.Recognizer()
    with sr.AudioFile(file_path) as source:
        audio_data = r.record(source)
        return r.recognize_google(audio_data, language=LANGUAGES[language]["lang_code"])

# ------------------ ANA UYGULAMA ------------------
def main():
    try:
        current_lang = LANGUAGES[st.session_state.language]
    except KeyError:
        # Eski dil değeriyle çalışanlar için otomatik düzeltme
        st.session_state.language = "🇹🇷 Türkçe"
        current_lang = LANGUAGES[st.session_state.language]
    
    # Dil seçimi
    lang = st.sidebar.selectbox("🌐 Dil / Language", list(LANGUAGES.keys()))
    st.session_state.language = lang
    current_lang = LANGUAGES[lang]
    
    # Bilgi penceresi (sidebar'da)
    with st.sidebar.expander(current_lang["info_title"], expanded=True):
        st.markdown(current_lang["info_content"])
    
    st.title(current_lang["title"])
    
    # Giriş tipi seçimi
    input_type = st.radio(
        current_lang["input_type"], 
        current_lang["options"],
        horizontal=True
    )
    
    audio_path = None
    audio_data = None

    if input_type == current_lang["options"][0]:  # Dosya Yükle / File Upload
        uploaded_file = st.file_uploader(
            current_lang["file_uploader"], 
            type=["wav", "mp3"]
        )
        if uploaded_file:
            audio_path = convert_to_wav(uploaded_file)
            st.session_state.file_uploaded = True
            
            # Ses kaydı başlığı ve oynatıcı
            st.subheader(current_lang["audio_label"])
            with open(audio_path, "rb") as f:
                audio_bytes = f.read()
            st.audio(audio_bytes, format="audio/wav")

    else:  # Canlı Kayıt / Live Recording
        col1, col2 = st.columns(2)
        with col1:
            if st.button(f"🎤 {current_lang['options'][1]}", disabled=st.session_state.recording):
                st.session_state.recording = True
                st.session_state.audio_data = None
        with col2:
            stop_text = "⏹️ Durdur" if st.session_state.language == "🇹🇷 Türkçe" else "⏹️ Stop"
            if st.button(stop_text, disabled=not st.session_state.recording):
                st.session_state.recording = False

        if st.session_state.recording:
            audio_data = audio_recorder(
                energy_threshold=(-1.0, 1.0),
                pause_threshold=300,
                sample_rate=16000,
                text=current_lang["recording"],
                recording_color="#ff0000"
            )
            if audio_data:
                st.session_state.audio_data = audio_data
                with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp_file:
                    tmp_file.write(audio_data)
                    audio_path = tmp_file.name
                # Ses kaydı başlığı ve oynatıcı
                st.subheader(current_lang["audio_label"])
                st.audio(st.session_state.audio_data, format="audio/wav")

            
    # İşlemler
    if audio_path or st.session_state.file_uploaded:
        try:
            # Ses analizi ve transkripsiyon
            if input_type == current_lang["options"][0]:  # Dosya yükleme durumu
                with st.spinner(current_lang["processing"]):
                    text = process_audio(audio_path, lang)
            else:  # Canlı kayıt durumu
                with wave.open(io.BytesIO(st.session_state.audio_data)) as wav:
                    duration = wav.getnframes() / wav.getframerate()
                    st.write(f"{current_lang['duration']}: {duration:.2f}s")
                
                with st.spinner(current_lang["processing"]):
                    text = process_audio(audio_path, lang)

            st.session_state.transcript = text
            
            # Transkript başlığı ve editör
            st.subheader(current_lang["transcript_label"])
            edited_text = st.text_area(
                current_lang["edit_text"], 
                st.session_state.transcript, 
                height=300,
                label_visibility="collapsed"
            )
            
            # Çıktı dosyaları başlığı ve indirme butonları
            st.subheader(current_lang["output_label"])
            col1, col2 = st.columns(2)
            with col1:
                st.download_button(
                    label=current_lang["download_txt"],
                    data=edited_text.encode('utf-8'),
                    file_name=f"transcript_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                    mime="text/plain"
                )
            with col2:
                pdf = create_pdf(edited_text)
                st.download_button(
                    label=current_lang["download_pdf"],
                    data=bytes(pdf),
                    file_name=f"transcript_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
                    mime="application/pdf"
                )

        except Exception as e:
            st.error(f"{current_lang['error']} {str(e)}")
        
        finally:
            if audio_path and os.path.exists(audio_path):
                os.unlink(audio_path)
            st.session_state.file_uploaded = False

    # Yan çubuk bilgilendirme
    st.sidebar.markdown(f"### {current_lang['requirements']}")
    for note in current_lang["notes"]:
        st.sidebar.write(f"- {note}")

if __name__ == "__main__":
    main()
