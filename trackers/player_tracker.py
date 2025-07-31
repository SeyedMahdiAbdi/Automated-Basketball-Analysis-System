from ultralytics import YOLO
import supervision as sv
import sys
import torch

sys.path.append("../")
from utils import save_stub, read_stub

class PlayerTracker:
    def __init__(self, model_path):
        self.model = YOLO(model_path)
        print(f"GPU IS AVAILABLE {torch.cuda.is_available()}")
        self.tracker = sv.ByteTrack()

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
            tracked_detections = self.tracker.update_with_detections(supervision_detections)

            tracks.append({})   #having a dictionary for each frame that key = id of player & value = bouning box

            for frame_detection in tracked_detections:
                bounding_box = frame_detection[0].tolist()
                class_id = frame_detection[3]
                track_id = frame_detection[4]

                #ignores all other class and considers just player class
                if class_id == inv_class_names["player"]:
                    tracks[frame_num][track_id]= {"bbox" : bounding_box}

        save_stub(stub_path, tracks)
            
        return tracks