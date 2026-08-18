"""
Face Tracking Crop Smoother & Deadzone Filter for Auto-Editor Pipeline
Takes raw face-detection bounding boxes across video frames and applies:
1. Deadzone Thresholding (ignores tiny head twitches / camera vibrations).
2. Exponential Moving Average (EMA) smoothing for buttery smooth camera re-framing.
"""

class FaceFramingSmoother:
    def __init__(self, smoothing_factor=0.08, deadzone_px=25):
        """
        smoothing_factor: 0.05 (very smooth/cinematic) to 0.25 (responsive).
        deadzone_px: minimal movement in pixels before camera starts shifting.
        """
        self.alpha = smoothing_factor
        self.deadzone = deadzone_px
        self.current_center_x = None
        self.current_center_y = None
        
    def update(self, detected_face_box):
        """
        detected_face_box: [x1, y1, x2, y2]
        Returns: smoothed [center_x, center_y]
        """
        raw_cx = (detected_face_box[0] + detected_face_box[2]) / 2.0
        raw_cy = (detected_face_box[1] + detected_face_box[3]) / 2.0
        
        if self.current_center_x is None:
            self.current_center_x = raw_cx
            self.current_center_y = raw_cy
            return [self.current_center_x, self.current_center_y]
            
        dx = raw_cx - self.current_center_x
        dy = raw_cy - self.current_center_y
        
        # Apply deadzone filter (prevent jitter on small eye/mouth twitches)
        if abs(dx) < self.deadzone:
            dx = 0
        if abs(dy) < self.deadzone:
            dy = 0
            
        # Exponential moving average filter
        self.current_center_x += self.alpha * dx
        self.current_center_y += self.alpha * dy
        
        return [round(self.current_center_x, 2), round(self.current_center_y, 2)]

if __name__ == "__main__":
    smoother = FaceFramingSmoother(smoothing_factor=0.1, deadzone_px=15)
    # Simulated jittery face detection inputs
    raw_detections = [
        [500, 300, 600, 420],
        [502, 301, 602, 421],  # micro jitter (deadzone will ignore)
        [540, 310, 640, 430],  # genuine head turn
        [580, 315, 680, 435]   # speaker walks right
    ]
    print("Smoothed Face Tracking Centers:")
    for idx, box in enumerate(raw_detections):
        cx, cy = smoother.update(box)
        print(f"  Frame {idx}: ({cx}, {cy})")
