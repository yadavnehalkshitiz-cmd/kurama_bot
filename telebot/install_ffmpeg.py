import os
import zipfile
import urllib.request
import shutil
import sys

FFMPEG_URL = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
ZIP_NAME = "ffmpeg.zip"
EXTRACT_FOLDER = "ffmpeg_temp"

def install_ffmpeg():
    print(f"Downloading FFmpeg from {FFMPEG_URL}...")
    try:
        # Download the file
        urllib.request.urlretrieve(FFMPEG_URL, ZIP_NAME)
        print("Download complete.")

        # Extract the zip file
        print("Extracting...")
        with zipfile.ZipFile(ZIP_NAME, 'r') as zip_ref:
            zip_ref.extractall(EXTRACT_FOLDER)
        
        # Find ffmpeg.exe
        ffmpeg_exe_path = None
        for root, dirs, files in os.walk(EXTRACT_FOLDER):
            if "ffmpeg.exe" in files:
                ffmpeg_exe_path = os.path.join(root, "ffmpeg.exe")
                break
        
        if ffmpeg_exe_path:
            # Move ffmpeg.exe to current directory
            destination = os.path.join(os.getcwd(), "ffmpeg.exe")
            if os.path.exists(destination):
                print(f"ffmpeg.exe already exists at {destination}")
            else:
                shutil.move(ffmpeg_exe_path, destination)
                print(f"ffmpeg.exe installed to {destination}")
                
            # Clean up
            print("Cleaning up temporary files...")
            if os.path.exists(ZIP_NAME):
                os.remove(ZIP_NAME)
            if os.path.exists(EXTRACT_FOLDER):
                shutil.rmtree(EXTRACT_FOLDER)
                
            print("FFmpeg installation successful!")
        else:
            print("Error: Could not find ffmpeg.exe in the downloaded archive.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if os.path.exists("ffmpeg.exe"):
        print("ffmpeg.exe is already present in the current directory.")
    else:
        install_ffmpeg()
