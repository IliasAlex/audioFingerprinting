import os

class YoutubeDownloader:        
    def download(self, path, link: str, custom_name : bool = True):
        os.chdir(path)
        if custom_name:
            custom_name = os.path.basename(path)
            filename = f'{custom_name}.wav'
            os.system(f'yt-dlp -x --audio-format wav --audio-quality 0 -o "{filename}" "{link}"')
        else:
            filename = None
            os.system(f'yt-dlp -x --audio-format wav --audio-quality 0 "{link}"')
        return filename
