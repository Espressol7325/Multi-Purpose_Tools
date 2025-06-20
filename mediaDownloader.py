import os
import yt_dlp 
from urllib.parse import urlparse
from datetime import datetime 

class MediaDownloader:
    def __init__(self, output_dir=r'E:\\Media_Downloader'):
        self.set_output_dir(output_dir)

    def set_output_dir(self, output_dir):
        """Sets the output directory and creates it if it doesn't exist."""
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        print(f"Output directory set to: {self.output_dir}")

    def download_media(self, url):
        """Downloads the media from the given URL to the specified output directory."""
        try:
            media_type = self.detect_media_type(url)
            if media_type == 'video':
                self.download_video(url)
            elif media_type == 'audio':
                self.download_audio(url)
            else:
                print("⚠️ Unsupported media type.")
        except Exception as e:
            print(f"❌ Error processing {url}: {e}")

    def detect_media_type(self, url):
        """Detects the media type based on the URL or content."""
        path = urlparse(url).path
        ext = os.path.splitext(path)[1].lower()
        if ext in ['.mp3', '.wav', '.aac', '.flac', '.ogg', '.m4a']:
            return 'audio'
        elif ext in ['.mp4', '.mkv', '.webm', '.flv', '.avi', '.mov']:
            return 'video'
        else:
            # Use yt_dlp to extract info and determine media type
            with yt_dlp.YoutubeDL({'quiet': True, 'no_warnings': True}) as ydl:
                try:
                    info_dict = ydl.extract_info(url, download=False)
                    if info_dict.get('extractor') == 'youtube':
                        return 'video' if info_dict.get('duration', 0) > 0 else 'audio'
                except:
                    pass
            return 'video'  # Default to video if unsure

    def download_video(self, url):
        """Downloads the video from the given URL to the specified output directory."""
        self._download(url, 'bestvideo+bestaudio/best')  # More reliable format selection

    def download_audio(self, url):
        """Downloads the audio from the given URL to the specified output directory."""
        self._download(url, 'bestaudio/best', postprocessors=[{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }])

    def _download(self, url, format_str, postprocessors=None):
        """Generic download method for both video and audio."""
        # Generate a timestamp for the filename
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        
        # Update the output template to include the timestamp
        ydl_opts = {
            'outtmpl': os.path.join(self.output_dir, f'{timestamp}_%(title)s.%(ext)s'),
            'format': format_str,
            'quiet': False,
            'noplaylist': True,
            'nocheckcertificate': True,  # Bypass HTTPS certificate validation
            'ignoreerrors': False,       # Stop on errors
            'no_warnings': False,        # Show warnings
            'verbose': False,            # Not too verbose
            'updatetime': True,          # Update file modification time
            # Use aria2c as external downloader for better performance
            # 'external_downloader': 'aria2c',
        }
        if postprocessors:
            ydl_opts['postprocessors'] = postprocessors

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                ydl.download([url])
                print(f"✅ Download completed: {url}")
            except Exception as e:
                print(f"❌ Failed to download {url}: {e}")
                
    def list_formats(self, url):
        """Lists all available formats for the given URL."""
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'listformats': True
        }
        
        print(f"Available formats for {url}:")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                info = ydl.extract_info(url, download=False)
                if 'formats' in info:
                    formats = info['formats']
                    print(f"{'ID':<5} {'EXT':<6} {'RESOLUTION':<15} {'FPS':<4} {'FILESIZE':<10} {'NOTE'}")
                    print("-" * 60)
                    for f in formats:
                        if f.get('acodec') != 'none' and f.get('vcodec') != 'none':
                            note = 'video+audio'
                        elif f.get('acodec') != 'none':
                            note = 'audio only'
                        elif f.get('vcodec') != 'none':
                            note = 'video only'
                        else:
                            note = ''
                        
                        filesize = f"{f.get('filesize')/1024/1024:.1f}MB" if f.get('filesize') else 'N/A'
                        resolution = f.get('resolution', 'N/A')
                        fps = f.get('fps', 'N/A')
                        
                        print(f"{f.get('format_id', 'N/A'):<5} {f.get('ext', 'N/A'):<6} "
                              f"{resolution:<15} {fps:<4} {filesize:<10} {note}")
                return True
            except Exception as e:
                print(f"❌ Error listing formats: {e}")
                return False

if __name__ == "__main__":
    downloader = MediaDownloader()

    while True:
        print("\n1. Download media")
        print("2. List available formats")
        print("Else. Exit")
        choice = input("Enter your choice: ").strip()
        
        if choice == '1':
            url = input("Enter the media URL: ").strip()
            if url:
                downloader.download_media(url)
            
        elif choice == '2':
            url = input("Enter the media URL: ").strip()
            if url:
                downloader.list_formats(url)
                
                # After showing formats, ask if user wants to download with specific format
                download = input("Download this media? (y/n): ").strip().lower()
                if download == 'y':
                    format_id = input("Enter format ID (leave blank for best quality): ").strip()
                    if format_id:
                        # Custom format with specific ID
                        ydl_opts = {
                            'outtmpl': os.path.join(downloader.output_dir, 
                                                   f'{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}_%(title)s.%(ext)s'),
                            'format': format_id,
                            'quiet': False,
                            'noplaylist': True,
                        }
                        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                            try:
                                ydl.download([url])
                                print(f"✅ Download completed: {url}")
                            except Exception as e:
                                print(f"❌ Failed to download {url}: {e}")
                    else:
                        # Regular download with best quality
                        downloader.download_media(url)
        
        else:
            break