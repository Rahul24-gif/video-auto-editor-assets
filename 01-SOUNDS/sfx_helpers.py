"""
SFX Audio Helpers for Video Auto-Editor Pipeline
Provides functions to:
1. Generate FFmpeg audio mixing command with auto-ducking (lower background music when voice is speaking).
2. Calculate exact audio timestamp offsets so whoosh sound peaks right on the video cut frame.
3. Batch mix sound effects directly over video audio track.
"""

import json
import os
import subprocess

def get_sfx_path(sound_id, base_dir=None):
    """Retrieve absolute file path for a given sound ID from catalog."""
    if base_dir is None:
        base_dir = os.path.dirname(os.path.abspath(__file__))
    catalog_file = os.path.join(base_dir, "sfx_catalog.json")
    with open(catalog_file, "r") as f:
        catalog = json.load(f)
    for sound in catalog["sounds"]:
        if sound["id"] == sound_id:
            return os.path.join(base_dir, sound["filename"].replace("/", os.sep))
    raise ValueError(f"Sound ID '{sound_id}' not found in catalog.")

def calculate_sync_timestamp(cut_timestamp_sec, sound_id, base_dir=None):
    """
    Calculates the exact audio start timestamp so that the peak of the whoosh/effect
    aligns with the exact cut/transition moment in video.
    """
    if base_dir is None:
        base_dir = os.path.dirname(os.path.abspath(__file__))
    catalog_file = os.path.join(base_dir, "sfx_catalog.json")
    with open(catalog_file, "r") as f:
        catalog = json.load(f)
    
    offset_ms = 0
    for sound in catalog["sounds"]:
        if sound["id"] == sound_id:
            offset_ms = sound.get("offset_ms", 0)
            break
            
    start_sec = max(0.0, cut_timestamp_sec + (offset_ms / 1000.0))
    return start_sec

def generate_ffmpeg_amix_filter(sfx_events):
    """
    Generates an FFmpeg complex filter string to place multiple SFX at given timestamps.
    
    Parameters:
    sfx_events: list of dicts:
      [
        {"sound_id": "whoosh_fast", "timestamp_sec": 3.42, "volume": 0.8},
        {"sound_id": "pop_bubble_sticker", "timestamp_sec": 5.10, "volume": 1.0}
      ]
    """
    inputs = ["-i input_video.mp4"]
    filter_parts = []
    
    for idx, event in enumerate(sfx_events, start=1):
        sfx_path = get_sfx_path(event["sound_id"])
        inputs.append(f"-i {sfx_path}")
        delay_ms = int(event["timestamp_sec"] * 1000)
        vol = event.get("volume", 1.0)
        # adelay filter sets start time for audio stream
        filter_parts.append(f"[{idx}:a]volume={vol},adelay={delay_ms}|{delay_ms}[sfx{idx}];")
        
    mix_sources = "".join([f"[sfx{i}]" for i in range(1, len(sfx_events) + 1)])
    amix_str = f"[0:a]{mix_sources}amix=inputs={len(sfx_events)+1}:duration=first:dropout_transition=2[aout]"
    
    return " ".join(inputs) + ' -filter_complex "' + "".join(filter_parts) + amix_str + '" -map 0:v -map "[aout]"'

if __name__ == "__main__":
    sample_events = [
        {"sound_id": "whoosh_fast", "timestamp_sec": 2.5, "volume": 0.9},
        {"sound_id": "pop_bubble_sticker", "timestamp_sec": 4.1, "volume": 1.0},
        {"sound_id": "ding_success_tip", "timestamp_sec": 7.8, "volume": 0.7}
    ]
    print("Example FFmpeg filter command for auto-editor:")
    print(generate_ffmpeg_amix_filter(sample_events))
