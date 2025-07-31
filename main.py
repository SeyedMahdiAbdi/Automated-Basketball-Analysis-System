from utils import get_video, save_video
from trackers import PlayerTracker, BallTracker
from drawers import (PlayerTracksDrawer, BallTracksDrawer)

def main():
  
  video_frames = get_video("input_videos/extra.mp4")
  
  #tracking
  player_tracker = PlayerTracker("models/player_detector.pt")
  ball_tracker = BallTracker("models/ball_detector.pt")
  
  player_tracks = player_tracker.object_tracker(video_frames, use_stub=True, stub_path="stubs/player_track_stubs.pkl")
  ball_tracks = ball_tracker.object_tracker(video_frames, use_stub=True, stub_path="stubs/ball_track_stubs.pkl")

  #removing wrong detections
  ball_tracks = ball_tracker.miss_detection_removal(ball_tracks)
  
  print(player_tracks)
  
  #drawing
  player_tracks_drawer = PlayerTracksDrawer()
  ball_tracks_drawer = BallTracksDrawer()
  output_frames = player_tracks_drawer.draw(video_frames, player_tracks)
  output_frames = ball_tracks_drawer.draw(output_frames, ball_tracks)
  
  save_video(output_frames, "output_videos/output_video.avi")
  
if __name__ == "__main__":
  main()