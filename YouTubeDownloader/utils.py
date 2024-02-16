import re


def check_valid_url(url):
    pattern = r"^(https?:\/\/)?(www\.)?(youtube\.com\/watch\?v=|youtu\.be\/)[\w-]{11}(&[^\s]+)?$"
    return re.match(pattern, url) is not None


def check_valid_filename(title):
    pattern = r'[\\/*?:"<>|]'
    return re.sub(pattern, '_', title)
