from .utils import draw_triangle

class BallTracksDrawer:
    def __init__(self):
        self.pointer_color = (0, 255, 0)

    def draw(self, video_frames, tracks):
        output_frames = []

        for frame_num, frame in enumerate(video_frames):
            frame = frame.copy()
            ball_dict = tracks[frame_num]

            for _, ball in ball_dict.items():
                bounding_box = ball["bbox"]
                if bounding_box is None:
                    continue

                frame = draw_triangle(frame, ball["bbox"], self.pointer_color)

            output_frames.append(frame)

        return output_frames