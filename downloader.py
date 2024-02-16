import re
import requests
from PIL import Image, ImageTk
import os
import ffmpeg
from pytube import YouTube
import utils
from utils import check_valid_filename
from tkinter import filedialog


class YouTubeDownloader:
    def __init__(self, url, callback=None):
        self.url = url
        self.callback = callback
        try:
            self.yt = YouTube(self.url)
        except Exception as e:
            print(f"Error: {e}")
            if self.callback:
                callback('Access Error')
        self.streams_dict = {}
        self.thumbnail = None
        self.format_box_values = None

    def fetch_video_info(self):
        try:
            cover_url = self.yt.thumbnail_url
            res = requests.get(cover_url)
            if res.status_code != 200:
                return False
            else:
                with open('thumbnail.jpg', 'wb') as file:
                    file.write(res.content)
                self.thumbnail = Image.open("thumbnail.jpg").resize((240, 135))
                self.thumbnail = ImageTk.PhotoImage(image=self.thumbnail)
                filtered_streams = self.yt.streams.filter(adaptive=True, subtype='mp4')
                filtered_streams_str = filtered_streams.__repr__()

                pattern_res = r'res=\"([\d]+p)\"'
                resolutions = re.findall(pattern_res, filtered_streams_str)
                resolutions = ['mp4 ' + res for res in resolutions]
                pattern_abr = r'abr=\"([\d]+kbps)\"'
                bitrates = re.findall(pattern_abr, filtered_streams_str)
                bitrates = ['mp3 ' + abr for abr in bitrates]
                format_box_values = resolutions + bitrates
                if self.streams_dict:
                    self.streams_dict.clear()
                for i in range(len(filtered_streams)):
                    self.streams_dict[format_box_values[i]] = filtered_streams[i].itag

                video_info = {'thumbnail': self.thumbnail, 'format_box_values': format_box_values, 'title': self.yt.title}
                if self.callback:
                    self.callback('Interface Update', video_info)
        except Exception as e:
            print(f"Error while fetching video: {e}")
            return False

    def save_file(self, selected_format):
        fixed_title = check_valid_filename(self.yt.title)
        itag = self.streams_dict[selected_format]
        stream = self.yt.streams.get_by_itag(itag)

        file_extension = selected_format.split(' ')[0]
        filetypes = [('MP4 files', '*.mp4')] if file_extension == 'mp4' else [('MP3 files', '*.mp3')]

        file_path = filedialog.asksaveasfilename(
            title="Save as",
            filetypes=filetypes,
            defaultextension=file_extension,
            initialdir='/',
            initialfile=f"{fixed_title}"
        )

        if file_path:
            output_path = os.path.dirname(file_path)
            filename = os.path.basename(file_path)
            if file_extension == 'mp4':
                tmp_video_filename = "tmp.mp4"
                tmp_audio_filename = "tmp.mp3"
                stream.download(output_path=output_path, filename=tmp_video_filename, skip_existing=False)
                tmp_video_path = f"{output_path}/{tmp_video_filename}"

                highest_audio_format = self.format_box_values[-1]
                audio_itag = self.streams_dict[highest_audio_format]
                audio_stream = self.yt.streams.get_by_itag(audio_itag)
                audio_stream.download(output_path=output_path, filename=tmp_audio_filename, skip_existing=False)
                tmp_audio_path = f"{output_path}/{tmp_audio_filename}"

                input_audio = ffmpeg.input(tmp_audio_path)
                input_video = ffmpeg.input(tmp_video_path)

                ffmpeg.concat(input_video, input_audio, v=1, a=1).output(f"{output_path}/{filename}").run()
                os.remove(tmp_audio_path)
                os.remove(tmp_video_path)
            else:
                stream.download(output_path=output_path, filename=filename, skip_existing=False)
