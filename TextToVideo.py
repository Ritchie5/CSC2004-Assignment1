import os
from moviepy.editor import *
from PIL import Image 

def get_frames():
        video_object = VideoFileClip("10.mp4")
        base_filename = os.path.splitext(os.path.basename("10.mp4"))[0]
        """Returns all frames in the video object"""
        directory = "output\\" + base_filename + '_frames\\'
        if not os.path.isdir(directory):# Checks if output Directory Exists, otherwise Create It
            os.makedirs(directory)
        for index, frame in enumerate(video_object.iter_frames()):
            img = Image.fromarray(frame, 'RGB')
            img.save(f'{directory}{index}.png')

def main():
    # Menu
    print("\n1: Video Splitter")
    print("2: Hide Data in Frames")
    print("3: Recover Data in Frames")

    # User Selection
    try:
        start_step = int(input("\nSelect the Program to Run: "))

        if start_step == 1:
            print("Starting Program...\n")
            #video_path = input("Enter a video path: ")
            #frames.get_frames(video_path)   
            get_frames()

        elif start_step == 2:
            print("Starting Program...\n")
            print("=== Hide Data in Frames ===")
            os.system("python Encoder.py")

        elif start_step == 3:
            print("Starting Program...\n")
            print("=== Recover Data in Frames ===")
            os.system("python Decoder.py")

        else:
            print("\nInvalid Input! Exiting...\n")
            quit()

    except ValueError:
        print("Non-Integer Input Entered. Exiting...\n")
    except KeyboardInterrupt:
	    print("\nUser canceled, exiting...")
	    quit()


if __name__ == '__main__':
    main()
