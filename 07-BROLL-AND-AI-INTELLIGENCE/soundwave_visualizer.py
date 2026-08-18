"""
Soundwave Visualizer Overlay Generator for Auto-Editor Pipeline
Generates dynamic audio equalizer bars from a WAV audio track using Python's standard library (wave + struct).
Outputs SVG / Frame coordinates or direct FFmpeg `showwaves` / `showspectrumpic` commands.
"""

import math
import os
import struct
import wave

def generate_svg_waveform_from_wav(wav_path, output_svg_path, num_bars=60, width=1080, height=240):
    """Reads a WAV file and outputs a clean vector audio waveform overlay SVG."""
    with wave.open(wav_path, 'r') as w:
        n_channels = w.getnchannels()
        sampwidth = w.getsampwidth()
        framerate = w.getframerate()
        n_frames = w.getnframes()
        raw_data = w.readframes(n_frames)
        
    # Unpack 16-bit PCM
    total_samples = n_frames * n_channels
    fmt = f"<{total_samples}h"
    samples = struct.unpack(fmt, raw_data)
    
    # If stereo, pick first channel
    mono_samples = samples[::n_channels]
    
    # Calculate RMS amplitude per bar chunk
    chunk_size = len(mono_samples) // num_bars
    bar_heights = []
    
    for i in range(num_bars):
        chunk = mono_samples[i * chunk_size : (i + 1) * chunk_size]
        if not chunk:
            bar_heights.append(10)
            continue
        rms = math.sqrt(sum(s * s for s in chunk) / len(chunk))
        # Normalize and scale
        h = max(8, min(height * 0.9, (rms / 12000.0) * (height * 0.9)))
        bar_heights.append(h)
        
    bar_width = (width - (num_bars * 6)) / num_bars
    
    os.makedirs(os.path.dirname(output_svg_path), exist_ok=True)
    with open(output_svg_path, 'w') as f:
        f.write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">\n')
        f.write('  <defs>\n')
        f.write('    <linearGradient id="waveGrad" x1="0%" y1="0%" x2="100%" y2="0%">\n')
        f.write('      <stop offset="0%" stop-color="#00F0FF" />\n')
        f.write('      <stop offset="50%" stop-color="#7000FF" />\n')
        f.write('      <stop offset="100%" stop-color="#FF007A" />\n')
        f.write('    </linearGradient>\n')
        f.write('  </defs>\n')
        f.write('  <g id="soundwave_bars">\n')
        
        for idx, h in enumerate(bar_heights):
            x = idx * (bar_width + 6) + 3
            y = (height - h) / 2
            f.write(f'    <rect x="{x:.1f}" y="{y:.1f}" width="{bar_width:.1f}" height="{h:.1f}" rx="4" fill="url(#waveGrad)" />\n')
            
        f.write('  </g>\n')
        f.write('</svg>\n')
    print(f"[OK] Generated audio soundwave overlay SVG: {output_svg_path}")

def get_ffmpeg_showwaves_filter(width=1080, height=240, color="0x00F0FF"):
    """Returns direct FFmpeg filter to generate live animated audio visualizer bar overlay."""
    return f"showwaves=s={width}x{height}:mode=line:colors={color}:draw=full[waveout]"

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    sample_wav = os.path.abspath(os.path.join(current_dir, "..", "01-sound-effects-sfx", "wav_files", "whoosh_deep_bass.wav"))
    output_svg = os.path.join(current_dir, "sample_soundwave.svg")
    
    if os.path.exists(sample_wav):
        generate_svg_waveform_from_wav(sample_wav, output_svg)
