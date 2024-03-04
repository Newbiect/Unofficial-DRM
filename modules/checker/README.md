This Python script uses the `pymediainfo` library to extract and display detailed information about a video file. Here's a breakdown of how it works:

1. **Import `MediaInfo` from `pymediainfo`:** The script starts by importing the necessary class from the library, which will be used to parse the media file.

2. **Define the `get_video_info` function:** This function takes a file path as input and uses `MediaInfo.parse()` to analyze the video file. It then iterates through each track in the media file, categorizing them into video, audio, or subtitle tracks based on their type. For each track, relevant details such as format, codec, bit rate, dimensions (for video tracks), channels and language (for audio tracks), and language (for subtitle tracks) are stored in dictionaries and added to respective lists.

3. **Structure the video information:** After collecting all the track information, it compiles a summary of the video file, including the file name, general format, duration, and details of video, audio, and subtitle tracks.

4. **Execution block:** The script defines a file path for the video file you want to analyze and calls the `get_video_info` function with this file path. It then prints out the collected information in a structured format.

To use this script, ensure you have the `pymediainfo` library installed. If not, you can install it using pip:

```bash
pip install pymediainfo
```

Also, make sure the file path in the script points to an actual video file you want to analyze. The output will provide a comprehensive overview of the video file's properties, including technical details about each of its tracks.
