import os
import unittest
from unittest.mock import patch, MagicMock, Mock, call
from YouTubeDownloader.downloader import Downloader
import pytube


class TestDownloader(unittest.TestCase):
    @patch('YouTubeDownloader.downloader.YouTube')
    def setUp(self, mock_youtube):
        self.mock_youtube = mock_youtube

        self.mock_stream = MagicMock()
        self.mock_youtube.return_value.streams.get_by_itag.return_value = self.mock_stream
        self.mock_stream.download.return_value = None

        url = "https://www.youtube.com/watch?v=test_channel=Test"
        self.mock_youtube.return_value.title = "Mocked video title"
        self.mock_youtube.return_value.thumbnail_url = "Mocked thumbnail url"
        test_streams = [
            '<Stream: itag="137" mime_type="video/mp4" res="1080p" fps="30fps" vcodec="avc1.640028" progressive="False" type="video">',
            '<Stream: itag="140" mime_type="audio/mp4" abr="128kbps" acodec="mp4a.40.2" progressive="False" type="audio">']

        mock_youtube_filtered = MagicMock()
        self.mock_youtube.return_value.streams.filter.return_value = mock_youtube_filtered
        mock_youtube_filtered.__str__.return_value = ' '.join(test_streams)
        mock_youtube_filtered.__len__.return_value = 2

        def generate_mock_stream(index):
            mock_stream = MagicMock(spec=pytube.StreamQuery)
            mock_stream.itag = str(index)
            return mock_stream

        mock_youtube_filtered.__getitem__.side_effect = generate_mock_stream

        self.downloader = Downloader(url)
        self.downloader.streams_dict = {'mp4 1080p': '0', 'mp3 128kbps': '1'}
        self.downloader.format_box_values = ['mp4 1080p', 'mp3 128kbps']

    def tearDown(self):
        if os.path.exists("thumbnail.jpg"):
            os.remove("thumbnail.jpg")

    def test_init(self):
        self.assertIsNotNone(self.downloader.yt, msg="downloader should be initialized")

    @patch('requests.get')
    @patch('PIL.ImageTk.PhotoImage')
    @patch('PIL.Image.open')
    @patch('builtins.open', autospec=True)
    def test_fetch_video_info(self, mock_open, mock_image, mock_photo_image, mock_response):
        mock_open.return_value.__enter__.return_value = Mock()

        mock_image.return_value = Mock()

        mock_photo_image.return_value = 'mocked_thumbnail_processed'
        mock_response.return_value = MagicMock()
        mock_response.return_value.content = b'thumbnail mocked content'
        mock_response.return_value.status_code = 200

        video_info, streams_dict = self.downloader.fetch_video_info()
        self.assertIsNotNone(video_info['thumbnail'])
        self.assertIsNotNone(video_info['format_box_values'])
        self.assertIsNotNone(video_info['title'])

    @patch('tkinter.filedialog.asksaveasfilename')
    def test_save_file_mp3(self, mock_file_path):
        selected_format = 'mp3 128kbps'

        output_path = os.path.join(os.environ['USERPROFILE'], 'Desktop')
        mock_file_path.return_value = os.path.join(output_path, f'{self.mock_youtube.return_value.title}')
        self.downloader.save_file(selected_format)
        self.mock_stream.download.assert_called_with(output_path=output_path,
                                                     filename='Mocked video title', skip_existing=False)

    @patch('ffmpeg.concat')
    @patch('ffmpeg.input')
    @patch('tkinter.filedialog.asksaveasfilename')
    def test_save_file_mp4(self, mock_file_path, mock_ffmpeg_input, mock_ffmpeg_concat):
        selected_format = 'mp4 1080p'

        output_path = os.path.join(os.environ['USERPROFILE'], 'Desktop')
        mock_file_path.return_value = os.path.join(output_path, f'{self.mock_youtube.return_value.title}')

        mock_ffmpeg_input.return_value = None
        mock_ffmpeg_concat.return_value = Mock()
        self.downloader.save_file(selected_format)
        calls = [call.download(output_path=output_path, filename='tmp.mp4', skip_existing=False),
                 call.download(output_path=output_path, filename='tmp.mp3', skip_existing=False)]
        self.mock_stream.download.assert_has_calls(calls)


if __name__ == '__main__':
    unittest.main()
