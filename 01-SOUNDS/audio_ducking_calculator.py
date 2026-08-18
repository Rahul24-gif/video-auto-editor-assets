"""
Automated Audio Ducking Calculator for Auto-Editor Pipeline
Takes detected voice timestamps (speech activity intervals) and calculates smooth volume
automation curves for background music/beats (dips background music when voice is talking).
"""

import json

def calculate_ducking_keyframes(speech_intervals, total_duration_sec, duck_db=-14.0, ramp_ms=250):
    """
    speech_intervals: list of (start_sec, end_sec) tuples where speaker is talking.
    Returns: list of volume keyframes: [{"time": 0.0, "gain_db": 0.0}, ...]
    """
    ramp_sec = ramp_ms / 1000.0
    keyframes = []
    
    current_t = 0.0
    is_ducked = False
    
    for start, end in speech_intervals:
        # Music plays normal before speech starts
        pre_duck_t = max(0.0, start - ramp_sec)
        keyframes.append({"time_sec": round(pre_duck_t, 3), "gain_db": 0.0})
        # Ducked down by the time speech starts
        keyframes.append({"time_sec": round(start, 3), "gain_db": duck_db})
        # Stays ducked until speech ends
        keyframes.append({"time_sec": round(end, 3), "gain_db": duck_db})
        # Ramps back up to 0dB after speech ends
        post_duck_t = min(total_duration_sec, end + ramp_sec)
        keyframes.append({"time_sec": round(post_duck_t, 3), "gain_db": 0.0})
        
    return keyframes

def generate_ffmpeg_sidechain_ducking_filter():
    """
    Returns the industry standard FFmpeg sidechaincompress filter:
    Automatically compresses audio track 1 (music) whenever audio track 0 (voice) speaks!
    """
    return "[1:a][0:a]sidechaincompress=threshold=0.08:ratio=6:attack=20:release=300[ducked_music];[0:a][ducked_music]amix=inputs=2[aout]"

if __name__ == "__main__":
    sample_speech = [(1.2, 4.5), (6.0, 9.8), (12.0, 15.5)]
    kf = calculate_ducking_keyframes(sample_speech, total_duration_sec=20.0)
    print("Calculated Audio Ducking Keyframes:")
    print(json.dumps(kf, indent=2))
    print("\nFFmpeg Live Sidechain Compression Filter:")
    print(generate_ffmpeg_sidechain_ducking_filter())
