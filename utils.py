import os
import wave
import subprocess
from dejavu.logic.recognizer.file_recognizer import FileRecognizer

def recognize_segments(djv, song_path, segment_duration=10):
    results = []
    total_duration = get_wav_duration(song_path)  # Get total duration of the song

    tmp_dir = "segments"  # Directory to store temporary segment files

    # Create the directory if it doesn't exist
    os.makedirs(tmp_dir, exist_ok=True)

    # Create segments
    start_time = 0
    while start_time + segment_duration <= total_duration:
        # Create a temporary file for the segment
        tmp_segment_file = os.path.join(tmp_dir, f"segment_{start_time}.wav")  # Adjust extension based on your requirements
        
        # Extract segment from original song
        extract_segment(song_path, tmp_segment_file, start_time, segment_duration)
        
        # Recognize the segment
        segment_results = djv.recognize(FileRecognizer, tmp_segment_file)
        
        # Extend results with segment_results
        results.append(segment_results['results'][0])
        
        start_time += segment_duration - 5 

    # Sort results by input_confidence and fingerprinted_confidence (both as floats, descending)
    sorted_results = sorted(results, key=lambda x: (float(x['input_confidence']), float(x['fingerprinted_confidence'])), reverse=True)
    
    # Get top 5 song names
    top_song_names = []
    for i, result in enumerate(sorted_results[:5]):
        top_song_names.append(result['song_name'].decode())  # Assuming song_name is in bytes, decode to string
        print(f"{i+1}. {result['input_confidence']}")
    
    return top_song_names
# Function to extract a segment from the original song
def extract_segment(original_file, output_file, start_time, duration):
    # Implement your logic to extract the segment here
    # Example: using ffmpeg to extract the segment
    cmd = [
        "ffmpeg",
        "-i", original_file,
        "-ss", str(start_time),  # Start time
        "-t", str(duration),  # Duration of the segment
        "-acodec", "copy",  # Use 'copy' to avoid re-encoding
        "-avoid_negative_ts", "make_zero",  # This can help avoid timestamp issues
        output_file
    ]
    subprocess.run(cmd, check=True)

def get_wav_duration(filename: str) -> int:
    """Get the time duration of a wav file"""
    with wave.open(filename, 'rb') as f:
        return f.getnframes() // f.getframerate()
    