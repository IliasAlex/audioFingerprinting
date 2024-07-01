import json
import sys
import os
import argparse
from argparse import RawTextHelpFormatter
from os.path import isdir
from dejavu import Dejavu
from dejavu.logic.recognizer.file_recognizer import FileRecognizer
from dejavu.logic.recognizer.microphone_recognizer import MicrophoneRecognizer
from utils import get_wav_duration, recognize_segments
from yt_downloader import YoutubeDownloader

DEFAULT_CONFIG_FILE = "dejavu.cnf.SAMPLE"

def init(configpath):
    """
    Load config from a JSON file
    """
    try:
        with open(configpath) as f:
            config = json.load(f)
    except IOError as err:
        print(f"Cannot open configuration: {str(err)}. Exiting")
        sys.exit(1)

    # create a Dejavu instance
    return Dejavu(config)

def main():
    parser = argparse.ArgumentParser(
        description="Dejavu: Audio Fingerprinting library",
        formatter_class=RawTextHelpFormatter)
    parser.add_argument('-c', '--config', nargs='?',
                        help='Path to configuration file\n'
                             'Usages: \n'
                             '--config /path/to/config-file\n')
    parser.add_argument('-f', '--fingerprint', nargs='*',
                        help='Fingerprint files in a directory\n'
                             'Usages: \n'
                             '--fingerprint /path/to/directory extension\n'
                             '--fingerprint /path/to/directory')
    parser.add_argument('-r', '--recognize', nargs=2,
                        help='Recognize what is '
                             'playing through the microphone or in a file.\n'
                             'Usage: \n'
                             '--recognize mic number_of_seconds \n'
                             '--recognize file path/to/file \n')
    parser.add_argument('-yt', '--youtube_link', help='YouTube link to download and recognize')
    parser.add_argument('-d', '--duplicate',
                        help='Find duplicates in a directory of WAV files\n'
                             'Usage: \n'
                             '--duplicate /path/to/directory\n')

    args = parser.parse_args()

    if not args.config:
        parser.print_help()
        sys.exit(0)

    config_file = args.config
    if config_file is None:
        config_file = DEFAULT_CONFIG_FILE

    djv = init(config_file)

    if args.youtube_link:
        curr_path = os.getcwd()
        tmp_dir = os.path.join(curr_path, "yt_songs")
            
        yt = YoutubeDownloader()
        song_path = yt.download(tmp_dir, args.youtube_link)
        print(f"Downloaded and converted to wav: {song_path}")

        # Recognize audio source in segments
        top_song_names = recognize_segments(djv, song_path)
        print("Top 5 Song Names with Highest Confidence:")
        for i, song_name in enumerate(top_song_names, start=1):
            print(f"{i}. {song_name}")

    elif args.fingerprint:
        # Fingerprint all files in a directory
        if len(args.fingerprint) == 2:
            directory = args.fingerprint[0]
            extension = args.fingerprint[1]
            print(f"Fingerprinting all .{extension} files in the {directory} directory")
            djv.fingerprint_directory(directory, ["." + extension], 4)

        elif len(args.fingerprint) == 1:
            filepath = args.fingerprint[0]
            if isdir(filepath):
                print("Please specify an extension if you'd like to fingerprint a directory!")
                sys.exit(1)
            djv.fingerprint_file(filepath)

    elif args.recognize:
        # Recognize audio source
        songs = None
        source = args.recognize[0]
        opt_arg = args.recognize[1]

        if source in ('mic', 'microphone'):
            songs = djv.recognize(MicrophoneRecognizer, seconds=opt_arg)
        elif source == 'file':
            songs = djv.recognize(FileRecognizer, opt_arg)
        print(songs)
    elif args.duplicate:
        directory = args.duplicate
        if not isdir(directory):
            print(f"Error: The path {directory} is not a directory.")
            sys.exit(1)

        print(f"Checking for duplicates in the directory: {directory}")

        # Fingerprint all files in the directory
        djv.fingerprint_directory(directory, [".wav"], 4)

        # Dictionary to store potential duplicates
        duplicates = {}

        # Recognize each file to find duplicates
        for filename in os.listdir(directory):
            if filename.endswith(".wav"):
                file_path = os.path.join(directory, filename)
                print(f"Recognizing file: {file_path}")

                result = djv.recognize(FileRecognizer, file_path)
                if result and 'results' in result:
                    for match in result['results']:
                        if match['input_confidence'] >= 0.95 and match['fingerprinted_confidence'] >= 0.95:
                            song_name = match['song_name'].decode('utf-8')
                            if song_name not in duplicates:
                                duplicates[song_name] = []
                            duplicates[song_name].append({
                                "file": filename,
                                "confidence": match['input_confidence'],
                                "fingerprint_confidence": match['fingerprinted_confidence']
                            })

        # Display results
        if duplicates:
            print("Duplicate files found:")
            for song, dup_info in duplicates.items():
                print(f"Song: {song}")
                for dup in dup_info:
                    print(f" - File: {dup['file']}, Input Confidence: {dup['confidence']}, Fingerprint Confidence: {dup['fingerprint_confidence']}")
        else:
            print("No duplicates found.")

if __name__ == '__main__':
    main()
