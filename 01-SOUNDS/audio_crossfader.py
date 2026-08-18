"""
Audio Crossfader & Cut De-Clicker for Auto-Editor Pipeline
Prevents audio clipping / pops at jump cut boundaries by applying rapid 15ms equal-power cosine crossfades.
"""

import math
import os
import struct
import wave

def crossfade_wav_segments(wav1_path, wav2_path, output_path, crossfade_ms=20):
    """Smoothly merges two audio segments with equal-power cosine crossfade."""
    with wave.open(wav1_path, 'r') as w1, wave.open(wav2_path, 'r') as w2:
        sr = w1.getframerate()
        ch = w1.getnchannels()
        sw = w1.getsampwidth()
        
        raw1 = w1.readframes(w1.getnframes())
        raw2 = w2.readframes(w2.getnframes())
        
    s1 = list(struct.unpack(f"<{len(raw1)//2}h", raw1))
    s2 = list(struct.unpack(f"<{len(raw2)//2}h", raw2))
    
    fade_samples = int((crossfade_ms / 1000.0) * sr * ch)
    fade_samples = min(fade_samples, len(s1), len(s2))
    
    # Body of segment 1 before crossfade
    merged = s1[:-fade_samples]
    
    # Equal-power crossfade zone
    for i in range(fade_samples):
        progress = i / fade_samples
        w_fade_out = math.cos(progress * (math.pi / 2))
        w_fade_in = math.sin(progress * (math.pi / 2))
        
        sample_out = s1[len(s1) - fade_samples + i] * w_fade_out
        sample_in = s2[i] * w_fade_in
        val = int(max(-32768, min(32767, sample_out + sample_in)))
        merged.append(val)
        
    # Body of segment 2 after crossfade
    merged.extend(s2[fade_samples:])
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with wave.open(output_path, 'w') as out_w:
        out_w.setnchannels(ch)
        out_w.setsampwidth(sw)
        out_w.setframerate(sr)
        out_w.writeframes(struct.pack(f"<{len(merged)}h", *merged))
        
    print(f"[OK] Crossfaded {wav1_path} + {wav2_path} -> {output_path} ({crossfade_ms}ms fade)")

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    sfx_dir = os.path.abspath(os.path.join(current_dir, "..", "01-sound-effects-sfx", "wav_files"))
    w1 = os.path.join(sfx_dir, "pop_crisp_caption.wav")
    w2 = os.path.join(sfx_dir, "whoosh_subtle.wav")
    out = os.path.join(current_dir, "test_crossfade.wav")
    if os.path.exists(w1) and os.path.exists(w2):
        crossfade_wav_segments(w1, w2, out, crossfade_ms=15)
