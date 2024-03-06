# YouTubeDownloader
This is a GUI application which allows you to download a mp4/mp3 files from YouTube by url.

<p align="center" width="100%">
    <img width="70%" src="https://github.com/eumorin/YouTubeDownloader/assets/98094128/327ae1a0-8232-4105-9f49-db6add594cfa"> 
</p>


## Description
The application features a GUI that simplifies the downloading process. Here's how it works:

- **URL Submission:** Paste the URL of the YouTube video you wish to download.
- **Format Selection:** After submitting the URL, the application processes the available media streams and presents the user with a dropdown list of available formats. Choose one you prefer

## Quickstart
Current app doesn't work without ffmpeg lib, so you have to download it locally first. https://ffmpeg.org/download.html
To run the application locally, follow these steps:

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/YouTubeDownloader.git
   cd YouTubeDownloader
2. **Set Up a Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate 
3. **Install dependencies**
    ```bash
    pip install -r requirements.txt
4. **Run the application**
   ```bash
   python main.py

## Stack
Tkinter, PIL, [pytube](https://github.com/pytube/pytube), requests, unittest.
