"""
Procedural Background Music (BGM) Generator for Video Auto-Editor Pipeline
Generates seamless looping background music beds using Python standard library:
1. Lo-Fi Chill Hop Groove (90 BPM)
2. Tech Upbeat Synth Pulse (120 BPM)
3. Cinematic Tension Bed (100 BPM)
4. Inspiring Corporate Harmony (110 BPM)
"""

import math
import os
import random
import struct
import sys
import wave

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

SAMPLE_RATE = 44100

def write_wav(filename, samples, sample_rate=SAMPLE_RATE):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        clipped = [max(-1.0, min(1.0, s)) for s in samples]
        raw_data = struct.pack(f"<{len(clipped)}h", *[int(s * 32767) for s in clipped])
        wav_file.writeframes(raw_data)

# 1. Lo-Fi Chill Groove (90 BPM -> 1 beat = 0.667s, 4 bars = 10.667s)
def generate_lofi_bgm():
    duration = 10.667
    num_samples = int(duration * SAMPLE_RATE)
    samples = []
    
    # 4-Chord Lo-Fi Progression: Dm7 -> G7 -> Cmaj7 -> Am7
    chords = [
        [146.83, 174.61, 220.00, 261.63], # Dm7
        [196.00, 246.94, 293.66, 349.23], # G7
        [130.81, 164.81, 196.00, 246.94], # Cmaj7
        [110.00, 130.81, 164.81, 196.00]  # Am7
    ]
    chord_dur = duration / 4.0
    
    for i in range(num_samples):
        t = i / SAMPLE_RATE
        chord_idx = min(int(t / chord_dur), 3)
        current_chord = chords[chord_idx]
        
        # Soft Rhodes-style sine chord with slight detune
        chord_val = 0.0
        for note_f in current_chord:
            sine = math.sin(2 * math.pi * note_f * t)
            sine_detune = math.sin(2 * math.pi * (note_f * 1.002) * t) * 0.5
            chord_val += (sine + sine_detune)
        chord_val *= 0.08
        
        # Lo-Fi Drum Beat (Kick on 1 & 3, Snare on 2 & 4, Hi-hat every 8th)
        beat_t = t % 0.6667
        beat_num = int((t / 0.6667) % 4)
        drum_val = 0.0
        
        # Kick drum
        if beat_num in [0, 2] and beat_t < 0.15:
            k_env = math.exp(-beat_t * 35)
            drum_val += math.sin(2 * math.pi * (80 * math.exp(-beat_t * 20)) * beat_t) * k_env * 0.4
            
        # Soft Snare / Rimshot
        if beat_num in [1, 3] and beat_t < 0.12:
            s_env = math.exp(-beat_t * 40)
            drum_val += (random.uniform(-1, 1) * 0.25 + math.sin(2 * math.pi * 220 * beat_t) * 0.15) * s_env
            
        # Vinyl crackle ambience
        vinyl = (random.uniform(-1, 1) * 0.15 if random.random() < 0.004 else 0.0) + random.uniform(-1, 1) * 0.015
        
        sample = chord_val + drum_val + vinyl
        samples.append(sample * 0.85)
    return samples

# 2. Tech Upbeat Synth Pulse (120 BPM -> 1 beat = 0.5s, 4 bars = 8.0s)
def generate_tech_synth_bgm():
    duration = 8.0
    num_samples = int(duration * SAMPLE_RATE)
    samples = []
    
    # Fast 16th note arpeggio: A minor scale (A2, C3, E3, A3, G3, E3, C3, B2)
    arp_notes = [110.0, 130.81, 164.81, 220.0, 196.0, 164.81, 130.81, 123.47]
    sixteenth_dur = 0.125
    
    for i in range(num_samples):
        t = i / SAMPLE_RATE
        note_idx = int((t / sixteenth_dur) % len(arp_notes))
        freq = arp_notes[note_idx]
        note_t = t % sixteenth_dur
        
        env = math.exp(-note_t * 16)
        # Resonant Saw synth
        saw = (2.0 * (t * freq - math.floor(t * freq + 0.5))) * 0.18
        
        # 4-on-the-floor kick
        beat_t = t % 0.5
        k_env = math.exp(-beat_t * 30) if beat_t < 0.18 else 0
        kick = math.sin(2 * math.pi * (110 * math.exp(-beat_t * 18)) * beat_t) * k_env * 0.4
        
        samples.append((saw * env + kick) * 0.85)
    return samples

# 3. Cinematic Tension Bed (100 BPM -> 1 beat = 0.6s, 4 bars = 9.6s)
def generate_tension_bed_bgm():
    duration = 9.6
    num_samples = int(duration * SAMPLE_RATE)
    samples = []
    
    for i in range(num_samples):
        t = i / SAMPLE_RATE
        # Deep pulsing sub bass in D (73.42 Hz)
        pulse = 0.5 * (1.0 + math.sin(2 * math.pi * (100 / 60) * t))
        sub = math.sin(2 * math.pi * 73.42 * t) * pulse * 0.35
        
        # Soft clock tick every 0.6s
        t_tick = t % 0.6
        tick_env = math.exp(-t_tick * 120)
        tick = (random.uniform(-1, 1) * 0.1 + math.sin(2 * math.pi * 2800 * t_tick) * 0.1) * tick_env
        
        # Atmospheric dark string drone
        drone = (math.sin(2 * math.pi * 146.83 * t) + math.sin(2 * math.pi * 220.00 * t)) * 0.12
        
        samples.append((sub + tick + drone) * 0.85)
    return samples

def build_all_bgm(output_dir):
    os.makedirs(output_dir, exist_ok=True)
    tracks = {
        "bgm_lofi_chill_groove_90bpm.wav": generate_lofi_bgm,
        "bgm_tech_upbeat_pulse_120bpm.wav": generate_tech_synth_bgm,
        "bgm_cinematic_tension_bed_100bpm.wav": generate_tension_bed_bgm
    }
    print(f"Generating {len(tracks)} background music WAV tracks into: {output_dir}")
    for filename, func in tracks.items():
        filepath = os.path.join(output_dir, filename)
        samples = func()
        write_wav(filepath, samples)
        print(f"  [OK] Created: {filename}")

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    build_all_bgm(os.path.join(current_dir, "bgm_tracks"))
