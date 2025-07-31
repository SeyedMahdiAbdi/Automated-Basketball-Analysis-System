import numpy as np
from ultralytics import YOLO
import supervision as sv
import sys

sys.path.append("../")
from utils import save_stub, read_stub

class BallTracker:
    def __init__(self,model_path):
        self.model = YOLO(model_path)

    def detect_frames(self, frames):
        detections = []
        batch_size = 100 #process 20 frames each time

        for i in range (0, len(frames), batch_size):
            batch_frames = frames[i:i+batch_size] 
            batch_detection = self.model.predict(batch_frames, conf=0.5, device=0)
            detections += batch_detection

        return detections
    
    def object_tracker(self, frames, use_stub=False, stub_path=None):
        tracks = read_stub(use_stub, stub_path)

        if tracks is not None:
            if len(tracks) == len(frames):
                return tracks
            
        tracks = []
        detections = self.detect_frames(frames)

        for frame_num, detection in enumerate(detections): 
            class_names = detection.names
            #inv_class_names = {v:k for k,v in class_names.items()}
            inv_class_names = {} #for using name instead of id 
            for key, value in class_names.items():
                inv_class_names[value] = key
            
            supervision_detections = sv.Detections.from_ultralytics(detection)

            tracks.append({})   #having a dictionary for each frame that key = id of player & value = bouning box

            high_conf_box = None    #for saving the the ball detection with the highest confidence score
            max_conf = 0

            for frame_detection in supervision_detections:
                bounding_box = frame_detection[0].tolist()
                class_id = frame_detection[3]
                conf_score = frame_detection[2]
                
                #for finding the bounding box of the ball detection with the highest confidence score
                if class_id == inv_class_names["basketball"]:
                    if max_conf < conf_score:
                        high_conf_box = bounding_box
                        max_conf = conf_score

            if high_conf_box is not None:
                tracks[frame_num][1] = {"bbox":high_conf_box}
            
        save_stub(stub_path, tracks)
            
        return tracks
    
    def miss_detection_removal(self, ball_positions):
        threshold = 25
        prev_detect_frame = -1

        for i in range(len(ball_positions)):
            current_bounding_box = ball_positions[i].get(1,{}).get('bbox',[])

            if len(current_bounding_box) == 0:
                continue

            if prev_detect_frame == -1: #for first detection
                prev_detect_frame = i
                continue

            correct_detection = ball_positions[prev_detect_frame].get(1,{}).get('bbox',[])
            num_miss_detect_frame = i - prev_detect_frame
            weighted_threshold = threshold * num_miss_detect_frame
            distance = np.linalg.norm(np.array(correct_detection[:2]) - np.array(current_bounding_box[:2]))
            if distance > weighted_threshold:
                ball_positions[i] = {}
            else:
                prev_detect_frame = i

        return ball_positions







