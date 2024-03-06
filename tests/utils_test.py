import unittest
from YouTubeDownloader import utils

class TestUtils(unittest.TestCase):
    def test_vaild_url(self):
        self.assertTrue(utils.check_valid_url("https://www.youtube.com/watch?v=nhwKOni6Aqw&ab_channel=Outperform"))
        self.assertTrue(utils.check_valid_url("https://www.youtube.com/watch?v=nhwKOni6Aqw&ab"))
        self.assertTrue(utils.check_valid_url("https://www.youtube.com/watch?v=nhwKOni6Aqw&ab_channel=O"))
        self.assertTrue(utils.check_valid_url("www.youtube.com/watch?v=nhwKOni6Aqw&ab_channel=Outperform"))
        self.assertTrue(utils.check_valid_url("youtube.com/watch?v=nhwKOni6Aqw&ab_channel=Outperform"))
        self.assertTrue(utils.check_valid_url("https://www.youtube.com/watch?v=nhwKOni6Aqw&ab"))
        self.assertFalse(utils.check_valid_url("watch?v=nhwKOni6Aqw&ab_channel=Outperform"))
        self.assertFalse(utils.check_valid_url("https://www.youtube.com/watch?v=nhwK&ab"))

    def test_valid_filename(self):
        self.assertEqual(utils.check_valid_filename("file*"), "file_")
        self.assertEqual(utils.check_valid_filename("file*&"), "file_&")
        self.assertEqual(utils.check_valid_filename("file\\"), "file_")


if __name__ == '__main__':
    unittest.main()