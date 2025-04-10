# Speech-to-Text Converter Application 🗣️➡️📝

This application is a web-based tool designed to convert audio content into text. Users can upload audio files or record live audio to transcribe them into text. The transcribed text can then be edited and downloaded in `.txt` or `.pdf` formats. 

---

## Required Libraries 📚

To run this application, you will need to install the following Python libraries:

- `streamlit==1.44.0`
- `SpeechRecognition==3.14.2`
- `pydub==0.25.1`
- `audio-recorder-streamlit==0.0.10`
- `fpdf==1.7.2`

### Installing the Required Libraries ⚙️

To install these dependencies, run the following command in your terminal or command prompt:

```bash
pip install streamlit==1.44.0 SpeechRecognition==3.14.2 pydub==0.25.1 audio-recorder-streamlit==0.0.10 fpdf==1.7.2
```

---

## Running the Application 🚀

1. **Python and Streamlit Installation:** If Streamlit is not installed yet, follow the installation steps above.
2. **Run the Code:** Navigate to the directory where the application files are located and run the following command to start the application:

   ```bash
   streamlit run app.py
   ```

   This command will open the application in your web browser. 🌐

---

## Application Features 🛠️

- **Audio Source Selection:** Users can either upload pre-recorded audio files 🎧 or record live audio 🎙️ using the microphone.
- **Multiple Language Support:** The interface and transcription support both Turkish 🇹🇷 and English 🇬🇧 languages.
- **Audio File Conversion:** Uploaded MP3 or WAV files are automatically converted to WAV format for transcription 🔄.
- **Text Editing:** The transcribed text can be edited by users before downloading ✍️.
- **Download Options:** Users can download the transcribed text in `.txt` or `.pdf` formats 💾.

---

## Supported Audio File Formats 🎶

- **MP3** 🎵
- **WAV** 🔊

---

## Application Workflow 🌀

1. **Language Selection:** The application allows you to choose between Turkish and English for both the interface and transcription 🇹🇷🇬🇧.
2. **Audio Source Selection:** You can upload your audio file (MP3/WAV) 📂 or record live audio directly through the app 🎤. For recording, make sure your microphone is enabled and accessible 🔊.
3. **Transcription:** After the audio file is uploaded or the live recording is completed, the application uses the SpeechRecognition library to transcribe the audio into text 📝. This process typically takes a few moments, depending on the length of the audio ⏳.
4. **Text Editing:** The transcribed text is displayed in the app, and you can make any necessary changes or corrections 🖊️. You can add, delete, or modify text as required ✏️.
5. **Download Options:** Once the transcription is completed and edited, you can download the text in either `.txt` or `.pdf` format 📥. The PDF file is formatted neatly with basic styling for readability 📄.

---

## Additional Information ℹ️

- **🎤 Microphone Access:** To record audio directly, the application needs access to your microphone. Make sure to grant the necessary permissions when prompted.
- **🔊 Clear Audio Recording:** The accuracy of transcription depends heavily on the clarity of the audio. Make sure the environment is quiet, and the speaker's voice is clear 🎧.
- **🌍 Internet Connection:** An active internet connection is required to use the transcription service, as it relies on external libraries for processing 🌐.

---

## PDF Support 📑

The application supports PDF exports using the `fpdf` library. When exporting to PDF, the text will be formatted using the **NotoSans-Regular** font. If this font is not already installed on your system, the application will automatically download it from the web. 📥

This feature ensures that the PDF output is both readable and well-structured. If you encounter any issues with the PDF generation, ensure that your system has access to the required fonts or that the internet connection is stable for downloading. 🌐

---

## How It Works 🔍

The core of this application is based on automatic speech recognition (ASR), which is powered by the `SpeechRecognition` library. It processes the audio input and uses various recognition engines, such as Google Web Speech API, to transcribe speech into text 🗣️➡️📝. The `pydub` library is used for audio format conversion (e.g., converting MP3 to WAV for transcription) 🔄. After transcription, users can edit the output text and choose the format in which they want to download the result 💾.

---

## Conclusion 🎉

This application is an ideal tool for quickly and accurately converting audio into text. Whether you're a student transcribing lectures 🎓, a journalist working with interviews 📰, or a professional needing transcription services 💼, this tool provides a fast, easy-to-use solution for all your speech-to-text needs.

