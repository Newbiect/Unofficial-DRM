from pymediainfo import MediaInfo

def get_video_info(file_path):
    media_info = MediaInfo.parse(file_path)

    # Initialize lists to store track information
    video_tracks = []
    audio_tracks = []
    subtitle_tracks = []

    # Extract information for each track
    for track in media_info.tracks:
        if track.track_type == "Video":
            video_tracks.append({
                "format": track.format,
                "codec": track.codec,
                "bit_rate": track.bit_rate,
                "width": track.width,
                "height": track.height,
                "frame_rate": track.frame_rate,
                "duration": track.duration,
            })
        elif track.track_type == "Audio":
            audio_tracks.append({
                "format": track.format,
                "codec": track.codec,
                "bit_rate": track.bit_rate,
                "channels": track.channel_s,
                "language": track.language,
                "duration": track.duration,
            })
        elif track.track_type == "Text":
            subtitle_tracks.append({
                "format": track.format,
                "codec": track.codec,
                "language": track.language,
            })

    # Prepare video information
    video_info = {
        "filename": media_info.tracks[0].track_name,
        "general_format": media_info.tracks[0].format,
        "general_duration": media_info.tracks[0].duration,
        "video_tracks": video_tracks,
        "audio_tracks": audio_tracks,
        "subtitle_tracks": subtitle_tracks,
    }

    return video_info

if __name__ == "__main__":
    file_path = "FILE NAME HERE"
    
    video_info = get_video_info(file_path)

    print("Video Information:")
    print("Filename:", video_info["filename"])
    print("General Format:", video_info["general_format"])
    print("General Duration:", video_info["general_duration"])

    print("\nVideo Tracks:")
    for index, track in enumerate(video_info["video_tracks"], start=1):
        print(f"Track {index}:")
        for key, value in track.items():
            print(f"\t{key}: {value}")

    print("\nAudio Tracks:")
    for index, track in enumerate(video_info["audio_tracks"], start=1):
        print(f"Track {index}:")
        for key, value in track.items():
            print(f"\t{key}: {value}")

    print("\nSubtitle Tracks:")
    for index, track in enumerate(video_info["subtitle_tracks"], start=1):
        print(f"Track {index}:")
        for key, value in track.items():
            print(f"\t{key}: {value}")
