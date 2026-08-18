"""
Cinematic Ken Burns Pan & Zoom Generator for Auto-Editor Pipeline
Generates smooth keyframe coordinates or FFmpeg zoompan filter strings for static images or B-roll footage.
"""

import math

def generate_ken_burns_ffmpeg_filter(direction="zoom_in", duration_sec=3.0, fps=30, width=1080, height=1920):
    """
    Returns an optimized FFmpeg zoompan filter string for 9:16 vertical video.
    """
    total_frames = int(duration_sec * fps)
    
    if direction == "zoom_in":
        # Zooms from 1.0 to 1.15 focused on center
        zoom_expr = f"'min(zoom+0.0015,1.15)'"
        x_expr = "'iw/2-(iw/zoom/2)'"
        y_expr = "'ih/2-(ih/zoom/2)'"
    elif direction == "zoom_out":
        # Zooms from 1.18 down to 1.02
        zoom_expr = f"'if(lte(zoom,1.0),1.18,max(1.02,zoom-0.0015))'"
        x_expr = "'iw/2-(iw/zoom/2)'"
        y_expr = "'ih/2-(ih/zoom/2)'"
    elif direction == "pan_left_to_right":
        zoom_expr = "'1.12'"
        x_expr = f"'min((in_w-in_w/zoom)*(on/{total_frames}),in_w-in_w/zoom)'"
        y_expr = "'ih/2-(ih/zoom/2)'"
    else:
        zoom_expr = "'1.05'"
        x_expr = "'iw/2-(iw/zoom/2)'"
        y_expr = "'ih/2-(ih/zoom/2)'"
        
    filter_str = f"zoompan=z={zoom_expr}:x={x_expr}:y={y_expr}:d={total_frames}:s={width}x{height}:fps={fps}"
    return filter_str

def calculate_ken_burns_box(frame_idx, total_frames, src_w, src_h, target_aspect=9/16, motion_type="zoom_in"):
    """
    Calculates crop box [x1, y1, x2, y2] for frame_idx for OpenCV / PIL / Canvas pipelines.
    """
    progress = frame_idx / max(1, total_frames - 1)
    # Smooth cosine ease in-out
    ease = 0.5 * (1.0 - math.cos(progress * math.pi))
    
    if motion_type == "zoom_in":
        scale = 1.0 + 0.15 * ease
    elif motion_type == "zoom_out":
        scale = 1.18 - 0.15 * ease
    else:
        scale = 1.08
        
    crop_w = src_w / scale
    crop_h = crop_w / target_aspect
    
    if crop_h > src_h:
        crop_h = src_h / scale
        crop_w = crop_h * target_aspect
        
    center_x = src_w / 2.0
    center_y = src_h / 2.0
    
    x1 = max(0, center_x - crop_w / 2.0)
    y1 = max(0, center_y - crop_h / 2.0)
    x2 = min(src_w, x1 + crop_w)
    y2 = min(src_h, y1 + crop_h)
    
    return [int(x1), int(y1), int(x2), int(y2)]

if __name__ == "__main__":
    print("Example FFmpeg Ken Burns Filter:")
    print(generate_ken_burns_ffmpeg_filter("zoom_in", duration_sec=3.0))
    print("\nCalculated Frame Crop Box (Frame 30 of 90):")
    print(calculate_ken_burns_box(30, 90, 1920, 1080, motion_type="zoom_in"))
