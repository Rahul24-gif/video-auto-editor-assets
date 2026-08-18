"""
Automated Silence Detector & Dead-Air Remover for Video Auto-Editor Pipeline
Uses FFmpeg `silencedetect` to find pauses in voiceover (silence > 0.4s) and generate
a cut list or FFmpeg filter_complex command to automatically chop dead air!
"""

import subprocess
import re
import json

def detect_silence_intervals(video_or_audio_path, noise_db=-30.0, min_duration_sec=0.4):
    """
    Runs FFmpeg silencedetect filter and parses silence_start and silence_end timestamps.
    """
    cmd = [
        "ffmpeg", "-i", video_or_audio_path,
        "-af", f"silencedetect=noise={noise_db}dB:d={min_duration_sec}",
        "-f", "null", "-"
    ]
    
    # Run and capture stderr
    res = subprocess.run(cmd, stderr=subprocess.PIPE, text=True, errors="replace")
    
    starts = []
    ends = []
    
    for line in res.stderr.splitlines():
        start_match = re.search(r"silence_start:\s*([0-9.]+)", line)
        if start_match:
            starts.append(float(start_match.group(1)))
            
        end_match = re.search(r"silence_end:\s*([0-9.]+)", line)
        if end_match:
            ends.append(float(end_match.group(1)))
            
    silence_ranges = list(zip(starts, ends))
    return silence_ranges

def generate_keep_segments(silence_ranges, total_duration_sec):
    """
    Inverts silence intervals to return speech segments that should be kept in the edit.
    """
    keep = []
    last_end = 0.0
    for s_start, s_end in silence_ranges:
        if s_start > last_end + 0.05:
            keep.append({"start": round(last_end, 3), "end": round(s_start, 3)})
        last_end = s_end
        
    if last_end < total_duration_sec - 0.05:
        keep.append({"start": round(last_end, 3), "end": round(total_duration_sec, 3)})
        
    return keep

if __name__ == "__main__":
    sample_silences = [(2.1, 2.8), (5.4, 6.2), (10.1, 11.0)]
    speech_chunks = generate_keep_segments(sample_silences, total_duration_sec=15.0)
    print("Detected Speech Chunks (Dead Air Removed):")
    print(json.dumps(speech_chunks, indent=2))
