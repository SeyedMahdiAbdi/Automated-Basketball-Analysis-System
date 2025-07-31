import numpy as np
import cv2
import sys
sys.path.append("../")
from utils import find_center_bounding_box, find_bounding_box_width

def draw_ellipse(frame, bounding_box, color, track_id=None):
  y2 = int(bounding_box[3])
  x_center, _ = find_center_bounding_box(bounding_box)
  width = find_bounding_box_width(bounding_box)
  rectangle_width = 40
  rectangle_height = 20
  x1_rectangle = x_center - rectangle_width // 2
  x2_rectangle = x_center + rectangle_width // 2
  y1_rectangle = (y2 - rectangle_height // 2) + 15
  y2_rectangle = (y2 + rectangle_height // 2) + 15
  
  cv2.ellipse(frame, center=(x_center, y2), axes=(int(width), int(0.35*width)), angle=0, startAngle=-45, endAngle=235, color=color, thickness=2, lineType=cv2.LINE_4)
  
  if track_id is not None:
    x1_text = x1_rectangle + 12
    
    cv2.rectangle(frame, (int(x1_rectangle), int(y1_rectangle)), (int(x2_rectangle), int(y2_rectangle)), color, cv2.FILLED)
    
    if track_id > 99:
      x1_text -= 10
      
    cv2.putText(frame, str(track_id), (int(x1_text), int(y1_rectangle+15)), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
    
  return frame

def draw_triangle(frame, bounding_box, color):
  y = int(bounding_box[1])
  x, _ = find_center_bounding_box(bounding_box)
  triangle_vertices = np.array([[x,y], [x-10,y-20], [x+10,y-20]])

  cv2.drawContours(frame, [triangle_vertices], 0, color, cv2.FILLED)
  cv2.drawContours(frame, [triangle_vertices], 0, (0,0,0), 2)

  return frame

    
  