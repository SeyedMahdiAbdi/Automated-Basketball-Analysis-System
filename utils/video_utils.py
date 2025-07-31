import cv2
import os   #use to get directories and file names

#function for getting video 
def get_video(video_path):
    frames = []
    capture = cv2.VideoCapture(video_path)

    while (True):
        is_returned, frame = capture.read()

        if not is_returned:
            break
        frames.append(frame)
    return frames
        
#function for saving video
def save_video(output_frames, output_path):
    if not os.path.exists(os.path.dirname(output_path)):
        os.mkdir(os.path.dirname(output_path))

    codec = cv2.VideoWriter_fourcc('X', 'V', 'I', 'D')
    #codec = cv2.VideoWriter_fourcc(*"XVID")
    output = cv2.VideoWriter(output_path, codec, 24, (output_frames[0].shape[1], output_frames[0].shape[0]))

    for frame in output_frames:
        output.write(frame)
    output.release()