"""
Expanded SFX Batch Generator for Video Auto-Editor Pipeline
Generates 40+ studio-grade 16-bit 44.1kHz WAV sound effects using Python standard library:
- 7 Whoosh Variations (Fast, Deep, Airy, Subtle, Reverse, Laser, Stutter)
- 8 UI & Micro-Interactions (Bubble pop, Crisp text pop, Cork pop, Click, Mouse tap, Card swipe, Water drop, iPhone ping)
- 7 Emphasis & Alerts (Success chime, Level up fanfare, Error buzzer, Pro-tip bell, Wrong buzz, Censor bleep 1000Hz, Record scratch)
- 7 Impacts & Risers (Bass drop boom, Sub rumble, Cinematic braam, Heartbeat, Tension riser, White noise sweep, Clock tick loop)
- 6 Meme & Comedy Sounds (Awkward crickets, Spring boing, Punch boxing hit, Car skid brake, Sad trombone fail, Crowd applause cheer)
- 5 Sci-Fi / Cyber FX (Glitch hit, Glitch stutter, Hologram scan, Power down, Shield deflect)
- 4 Ambient & Audio Bed Fillers (Room tone noise floor, Vinyl crackle, Lo-Fi chill drone, Cyber drone tension)
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
    """Write mono 16-bit PCM WAV file."""
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        clipped = [max(-1.0, min(1.0, s)) for s in samples]
        raw_data = struct.pack(f"<{len(clipped)}h", *[int(s * 32767) for s in clipped])
        wav_file.writeframes(raw_data)

# --- 1. WHOOSHES ---
def generate_whoosh_fast():
    duration = 0.28
    num_samples = int(duration * SAMPLE_RATE)
    noise_buffer = [random.uniform(-1, 1) for _ in range(num_samples)]
    samples = []
    for i in range(num_samples):
        t = i / SAMPLE_RATE
        progress = i / num_samples
        env = math.sin(progress * (math.pi / 1.2)) ** 2 if progress < 0.6 else math.cos(((progress - 0.6) / 0.4) * (math.pi / 2)) ** 2
        sub_bass = math.sin(2 * math.pi * (80 + 120 * progress) * t) * 0.3
        samples.append((noise_buffer[i] * 0.7 + sub_bass) * env * 0.9)
    return samples

def generate_whoosh_deep():
    duration = 0.45
    num_samples = int(duration * SAMPLE_RATE)
    samples = []
    for i in range(num_samples):
        t = i / SAMPLE_RATE
        progress = i / num_samples
        env = math.sin(progress * math.pi) ** 1.8
        freq = 280 * (1.0 - 0.7 * progress)
        sine = math.sin(2 * math.pi * freq * t)
        noise = random.uniform(-1, 1) * 0.35 * (1.0 - progress)
        samples.append((sine * 0.7 + noise) * env * 0.95)
    return samples

def generate_whoosh_airy():
    duration = 0.20
    num_samples = int(duration * SAMPLE_RATE)
    samples = []
    for i in range(num_samples):
        t = i / SAMPLE_RATE
        progress = i / num_samples
        env = math.sin(progress * math.pi) ** 2
        noise = random.uniform(-1, 1) * 0.8
        sine = math.sin(2 * math.pi * (1200 - 600 * progress) * t) * 0.2
        samples.append((noise + sine) * env * 0.8)
    return samples

def generate_whoosh_subtle():
    duration = 0.15
    num_samples = int(duration * SAMPLE_RATE)
    samples = []
    for i in range(num_samples):
        t = i / SAMPLE_RATE
        progress = i / num_samples
        env = math.sin(progress * math.pi) ** 2.5
        noise = random.uniform(-1, 1) * 0.6
        sine = math.sin(2 * math.pi * (400 + 400 * progress) * t) * 0.3
        samples.append((noise + sine) * env * 0.8)
    return samples

def generate_whoosh_reverse():
    duration = 0.50
    num_samples = int(duration * SAMPLE_RATE)
    samples = []
    for i in range(num_samples):
        t = i / SAMPLE_RATE
        progress = i / num_samples
        env = (progress ** 2.5)
        freq = 100 + 900 * (progress ** 2)
        sine = math.sin(2 * math.pi * freq * t)
        noise = random.uniform(-1, 1) * 0.6
        samples.append((sine * 0.6 + noise * 0.4) * env * 0.9)
    return samples

def generate_whoosh_laser():
    duration = 0.25
    num_samples = int(duration * SAMPLE_RATE)
    samples = []
    for i in range(num_samples):
        t = i / SAMPLE_RATE
        progress = i / num_samples
        freq = 2800 * math.exp(-progress * 10) + 180
        env = math.sin(progress * math.pi) ** 1.5
        saw = 2.0 * (t * freq - math.floor(t * freq + 0.5))
        samples.append(saw * env * 0.8)
    return samples

def generate_whoosh_stutter():
    duration = 0.35
    num_samples = int(duration * SAMPLE_RATE)
    samples = []
    for i in range(num_samples):
        t = i / SAMPLE_RATE
        progress = i / num_samples
        gate = 1.0 if int(t * 40) % 2 == 0 else 0.1
        env = math.sin(progress * math.pi) ** 1.8 * gate
        noise = random.uniform(-1, 1) * 0.7
        sine = math.sin(2 * math.pi * (300 + 600 * progress) * t) * 0.3
        samples.append((noise + sine) * env * 0.85)
    return samples

# --- 2. UI & MICRO-INTERACTIONS ---
def generate_pop_bubble():
    duration = 0.12
    num_samples = int(duration * SAMPLE_RATE)
    samples = []
    for i in range(num_samples):
        t = i / SAMPLE_RATE
        progress = i / num_samples
        env = math.exp(-progress * 18)
        freq = 300 + 600 * (progress ** 0.5)
        samples.append(math.sin(2 * math.pi * freq * t) * env * 0.9)
    return samples

def generate_pop_crisp():
    duration = 0.08
    num_samples = int(duration * SAMPLE_RATE)
    samples = []
    for i in range(num_samples):
        t = i / SAMPLE_RATE
        progress = i / num_samples
        env = math.exp(-progress * 35)
        freq = 650 * math.exp(-progress * 8)
        sine = math.sin(2 * math.pi * freq * t)
        click = random.uniform(-1, 1) * math.exp(-progress * 60) * 0.5
        samples.append((sine + click) * env * 0.95)
    return samples

def generate_pop_cork():
    duration = 0.14
    num_samples = int(duration * SAMPLE_RATE)
    samples = []
    for i in range(num_samples):
        t = i / SAMPLE_RATE
        progress = i / num_samples
        env = math.exp(-progress * 22)
        freq = 180 + 520 * (1.0 - progress)
        samples.append(math.sin(2 * math.pi * freq * t) * env * 0.95)
    return samples

def generate_pop_mouse_click():
    duration = 0.05
    num_samples = int(duration * SAMPLE_RATE)
    samples = []
    for i in range(num_samples):
        t = i / SAMPLE_RATE
        env = math.exp(-t * 220)
        noise = random.uniform(-1, 1) * 0.8
        sine = math.sin(2 * math.pi * 3200 * t) * 0.4
        samples.append((noise + sine) * env * 0.85)
    return samples

def generate_pop_water_drip():
    duration = 0.18
    num_samples = int(duration * SAMPLE_RATE)
    samples = []
    for i in range(num_samples):
        t = i / SAMPLE_RATE
        progress = i / num_samples
        env = math.exp(-progress * 14)
        freq = 600 + 1200 * (progress ** 2)
        samples.append(math.sin(2 * math.pi * freq * t) * env * 0.85)
    return samples

def generate_swipe_card():
    duration = 0.16
    num_samples = int(duration * SAMPLE_RATE)
    samples = []
    for i in range(num_samples):
        t = i / SAMPLE_RATE
        progress = i / num_samples
        env = math.sin(progress * math.pi) ** 2
        noise = random.uniform(-1, 1) * 0.7
        samples.append(noise * env * 0.75)
    return samples

def generate_notification_iphone_ping():
    duration = 0.65
    num_samples = int(duration * SAMPLE_RATE)
    samples = []
    f1, f2 = 1318.51, 1760.0  # E6, A6 two-tone chime
    for i in range(num_samples):
        t = i / SAMPLE_RATE
        if t < 0.12:
            s = math.sin(2 * math.pi * f1 * t) * math.exp(-t * 15)
        else:
            t2 = t - 0.12
            s = math.sin(2 * math.pi * f2 * t2) * math.exp(-t2 * 6)
        samples.append(s * 0.85)
    return samples

def generate_typing_keyboard():
    duration = 0.04
    num_samples = int(duration * SAMPLE_RATE)
    samples = []
    for i in range(num_samples):
        t = i / SAMPLE_RATE
        env = math.exp(-t * 180)
        noise = random.uniform(-1, 1) * 0.7
        sine = math.sin(2 * math.pi * 1800 * t) * 0.3
        samples.append((noise + sine) * env * 0.85)
    return samples

# --- 3. EMPHASIS & ALERTS ---
def generate_ding_success():
    duration = 0.85
    num_samples = int(duration * SAMPLE_RATE)
    samples = []
    f1, f2, f3 = 1046.5, 2093.0, 3135.96
    for i in range(num_samples):
        t = i / SAMPLE_RATE
        progress = i / num_samples
        env = math.exp(-progress * 5.0)
        s = (
            math.sin(2 * math.pi * f1 * t) * 0.6 +
            math.sin(2 * math.pi * f2 * t) * 0.3 * math.exp(-progress * 8) +
            math.sin(2 * math.pi * f3 * t) * 0.15 * math.exp(-progress * 12)
        )
        samples.append(s * env * 0.9)
    return samples

def generate_fanfare_level_up():
    duration = 0.65
    num_samples = int(duration * SAMPLE_RATE)
    samples = []
    notes = [523.25, 659.25, 783.99, 1046.50]
    note_dur = 0.12
    for i in range(num_samples):
        t = i / SAMPLE_RATE
        note_idx = min(int(t / note_dur), len(notes) - 1)
        freq = notes[note_idx]
        note_t = t - (note_idx * note_dur)
        env = math.exp(-note_t * 8)
        samples.append(math.sin(2 * math.pi * freq * t) * env * 0.85)
    return samples

def generate_error_buzzer():
    duration = 0.35
    num_samples = int(duration * SAMPLE_RATE)
    samples = []
    freq = 140
    for i in range(num_samples):
        t = i / SAMPLE_RATE
        env = math.exp(-(i / num_samples) * 3)
        vibrato = math.sin(2 * math.pi * 25 * t) * 15
        val = 1.0 if math.sin(2 * math.pi * (freq + vibrato) * t) > 0 else -1.0
        samples.append(val * env * 0.7)
    return samples

def generate_censor_bleep():
    duration = 0.50
    num_samples = int(duration * SAMPLE_RATE)
    samples = []
    for i in range(num_samples):
        t = i / SAMPLE_RATE
        samples.append(math.sin(2 * math.pi * 1000 * t) * 0.75)
    return samples

def generate_record_scratch():
    duration = 0.40
    num_samples = int(duration * SAMPLE_RATE)
    samples = []
    for i in range(num_samples):
        t = i / SAMPLE_RATE
        progress = i / num_samples
        env = math.sin(progress * math.pi) ** 1.2
        freq = 3200 * math.sin(progress * 18) + 800
        noise = random.uniform(-1, 1) * 0.6
        sine = math.sin(2 * math.pi * freq * t) * 0.4
        samples.append((noise + sine) * env * 0.85)
    return samples

# --- 4. IMPACTS & RISERS ---
def generate_bass_drop_boom():
    duration = 0.95
    num_samples = int(duration * SAMPLE_RATE)
    samples = []
    for i in range(num_samples):
        t = i / SAMPLE_RATE
        progress = i / num_samples
        env = math.exp(-progress * 3.5)
        freq = 120 * math.exp(-progress * 3) + 35
        sine = math.sin(2 * math.pi * freq * t)
        distortion = math.tanh(sine * 2.5) * 0.8
        samples.append(distortion * env * 0.95)
    return samples

def generate_sub_rumble():
    duration = 1.2
    num_samples = int(duration * SAMPLE_RATE)
    samples = []
    for i in range(num_samples):
        t = i / SAMPLE_RATE
        progress = i / num_samples
        env = math.sin(progress * math.pi) ** 1.5
        freq = 45 + 10 * math.sin(t * 8)
        sine = math.sin(2 * math.pi * freq * t)
        samples.append(sine * env * 0.95)
    return samples

def generate_cinematic_braam():
    duration = 1.8
    num_samples = int(duration * SAMPLE_RATE)
    samples = []
    for i in range(num_samples):
        t = i / SAMPLE_RATE
        progress = i / num_samples
        env = (1.0 - math.exp(-progress * 30)) * math.exp(-progress * 2.0)
        freq = 55.0  # Deep A1
        # Heavy distorted saw
        saw = 2.0 * (t * freq - math.floor(t * freq + 0.5))
        saw_sub = math.sin(2 * math.pi * (freq / 2) * t)
        dist = math.tanh((saw + saw_sub * 0.8) * 3.0) * 0.7
        samples.append(dist * env * 0.9)
    return samples

def generate_heartbeat():
    duration = 0.8
    num_samples = int(duration * SAMPLE_RATE)
    samples = []
    for i in range(num_samples):
        t = i / SAMPLE_RATE
        # Thump 1 at 0.0s, Thump 2 at 0.25s
        t1 = t
        env1 = math.exp(-t1 * 18) if t1 < 0.2 else 0
        s1 = math.sin(2 * math.pi * 55 * t1) * env1
        
        t2 = max(0, t - 0.22)
        env2 = math.exp(-t2 * 16) if t >= 0.22 else 0
        s2 = math.sin(2 * math.pi * 48 * t2) * env2 * 0.85
        
        samples.append((s1 + s2) * 0.95)
    return samples

def generate_riser_tension():
    duration = 1.5
    num_samples = int(duration * SAMPLE_RATE)
    samples = []
    for i in range(num_samples):
        t = i / SAMPLE_RATE
        progress = i / num_samples
        env = progress ** 2.2
        freq = 100 + 1200 * (progress ** 2)
        sine = math.sin(2 * math.pi * freq * t)
        noise = random.uniform(-1, 1) * (progress ** 1.5) * 0.4
        samples.append((sine * 0.7 + noise) * env * 0.9)
    return samples

def generate_riser_white_noise():
    duration = 1.2
    num_samples = int(duration * SAMPLE_RATE)
    samples = []
    for i in range(num_samples):
        t = i / SAMPLE_RATE
        progress = i / num_samples
        env = progress ** 2.0
        noise = random.uniform(-1, 1)
        samples.append(noise * env * 0.8)
    return samples

def generate_clock_tick_loop():
    duration = 1.0
    num_samples = int(duration * SAMPLE_RATE)
    samples = []
    for i in range(num_samples):
        t = i / SAMPLE_RATE
        # Tick at 0.0 and 0.5
        t_rel = t % 0.5
        env = math.exp(-t_rel * 140)
        freq = 2400 if t < 0.5 else 1800
        sine = math.sin(2 * math.pi * freq * t_rel) * 0.5
        click = random.uniform(-1, 1) * 0.5
        samples.append((sine + click) * env * 0.8)
    return samples

# --- 5. MEME & COMEDY ---
def generate_awkward_crickets():
    duration = 1.5
    num_samples = int(duration * SAMPLE_RATE)
    samples = []
    for i in range(num_samples):
        t = i / SAMPLE_RATE
        # Chirp pulses every 0.15s
        pulse = int(t * 8)
        t_p = (t * 8) - pulse
        env = math.sin(t_p * math.pi) ** 3 if t_p < 0.6 else 0
        freq = 4500 + 300 * math.sin(t * 60)
        sine = math.sin(2 * math.pi * freq * t)
        samples.append(sine * env * 0.55)
    return samples

def generate_spring_boing():
    duration = 0.65
    num_samples = int(duration * SAMPLE_RATE)
    samples = []
    for i in range(num_samples):
        t = i / SAMPLE_RATE
        progress = i / num_samples
        env = math.exp(-progress * 5)
        # Fast frequency modulation
        mod = math.sin(2 * math.pi * 18 * t) * 120
        freq = 320 + mod + (progress * 250)
        sine = math.sin(2 * math.pi * freq * t)
        samples.append(sine * env * 0.85)
    return samples

def generate_punch_boxing():
    duration = 0.25
    num_samples = int(duration * SAMPLE_RATE)
    samples = []
    for i in range(num_samples):
        t = i / SAMPLE_RATE
        progress = i / num_samples
        env = math.exp(-progress * 20)
        noise = random.uniform(-1, 1) * math.exp(-progress * 30) * 0.7
        bass = math.sin(2 * math.pi * 90 * math.exp(-progress * 8) * t) * 0.8
        samples.append((noise + bass) * env * 0.95)
    return samples

def generate_car_skid_brake():
    duration = 0.8
    num_samples = int(duration * SAMPLE_RATE)
    samples = []
    for i in range(num_samples):
        t = i / SAMPLE_RATE
        progress = i / num_samples
        env = math.sin(progress * math.pi) ** 1.5
        freq = 1800 + 400 * math.sin(t * 80)
        noise = random.uniform(-1, 1) * 0.6
        saw = (2.0 * (t * freq - math.floor(t * freq + 0.5))) * 0.4
        samples.append((noise + saw) * env * 0.8)
    return samples

def generate_sad_trombone():
    duration = 1.8
    num_samples = int(duration * SAMPLE_RATE)
    samples = []
    # 4 descending notes: D4 -> C#4 -> C4 -> B3(slide down)
    notes = [293.66, 277.18, 261.63, 246.94]
    dur_per_note = 0.42
    for i in range(num_samples):
        t = i / SAMPLE_RATE
        idx = min(int(t / dur_per_note), 3)
        freq = notes[idx]
        if idx == 3:
            # Final sad slide down + vibrato
            t_slide = t - (3 * dur_per_note)
            freq = 246.94 * math.exp(-t_slide * 0.8) + math.sin(t * 22) * 6
            
        t_note = t - (idx * dur_per_note)
        env = (1.0 - math.exp(-t_note * 20)) * math.exp(-t_note * 2.5)
        saw = 2.0 * (t * freq - math.floor(t * freq + 0.5))
        samples.append(saw * env * 0.75)
    return samples

def generate_crowd_cheer():
    duration = 2.0
    num_samples = int(duration * SAMPLE_RATE)
    samples = []
    for i in range(num_samples):
        t = i / SAMPLE_RATE
        progress = i / num_samples
        env = math.sin(progress * math.pi) ** 1.2
        noise = random.uniform(-1, 1) * 0.7
        sine = math.sin(2 * math.pi * (600 + 150 * math.sin(t * 3)) * t) * 0.15
        samples.append((noise + sine) * env * 0.8)
    return samples

# --- 6. SCI-FI / CYBER ---
def generate_glitch_cyber():
    duration = 0.22
    num_samples = int(duration * SAMPLE_RATE)
    samples = []
    for i in range(num_samples):
        t = i / SAMPLE_RATE
        progress = i / num_samples
        env = math.exp(-progress * 8)
        step = int(progress * 16)
        freq = 150 + ((step * 383) % 1800)
        square = 1.0 if math.sin(2 * math.pi * freq * t) > 0 else -1.0
        noise = random.uniform(-1, 1) if (i % 7 == 0) else 0
        samples.append((square * 0.6 + noise * 0.4) * env * 0.85)
    return samples

def generate_glitch_stutter():
    duration = 0.30
    num_samples = int(duration * SAMPLE_RATE)
    samples = []
    stutter_rate = 32
    for i in range(num_samples):
        t = i / SAMPLE_RATE
        progress = i / num_samples
        env = math.exp(-progress * 4)
        stutter_gate = 1.0 if (int(t * stutter_rate) % 2 == 0) else 0.05
        freq = 400 + 300 * math.sin(t * 50)
        saw = 2.0 * (t * freq - math.floor(t * freq + 0.5))
        samples.append(saw * stutter_gate * env * 0.8)
    return samples

def generate_hologram_scan():
    duration = 0.60
    num_samples = int(duration * SAMPLE_RATE)
    samples = []
    for i in range(num_samples):
        t = i / SAMPLE_RATE
        progress = i / num_samples
        env = math.sin(progress * math.pi) ** 1.5
        freq = 1400 + 800 * math.sin(t * 65)
        sine = math.sin(2 * math.pi * freq * t)
        samples.append(sine * env * 0.75)
    return samples

def generate_power_down():
    duration = 0.75
    num_samples = int(duration * SAMPLE_RATE)
    samples = []
    for i in range(num_samples):
        t = i / SAMPLE_RATE
        progress = i / num_samples
        env = (1.0 - progress) ** 1.5
        freq = 800 * math.exp(-progress * 4.5) + 30
        saw = 2.0 * (t * freq - math.floor(t * freq + 0.5))
        samples.append(saw * env * 0.85)
    return samples

def generate_shield_deflect():
    duration = 0.35
    num_samples = int(duration * SAMPLE_RATE)
    samples = []
    for i in range(num_samples):
        t = i / SAMPLE_RATE
        progress = i / num_samples
        env = math.exp(-progress * 9)
        freq = 1200 + 400 * math.sin(t * 120)
        sine = math.sin(2 * math.pi * freq * t)
        samples.append(sine * env * 0.8)
    return samples

# --- 7. AMBIENT & AUDIO BEDS ---
def generate_room_tone():
    duration = 2.5
    num_samples = int(duration * SAMPLE_RATE)
    samples = []
    for i in range(num_samples):
        # Soft low-frequency pink/brown noise
        noise = random.uniform(-1, 1) * 0.08
        sine = math.sin(2 * math.pi * 60 * (i / SAMPLE_RATE)) * 0.03
        samples.append(noise + sine)
    return samples

def generate_vinyl_crackle():
    duration = 2.5
    num_samples = int(duration * SAMPLE_RATE)
    samples = []
    for i in range(num_samples):
        pop = random.uniform(-1, 1) * 0.4 if random.random() < 0.003 else 0
        hiss = random.uniform(-1, 1) * 0.04
        samples.append(pop + hiss)
    return samples

def generate_lofi_drone():
    duration = 3.0
    num_samples = int(duration * SAMPLE_RATE)
    samples = []
    # Smooth warm major chord: F3 (174.61), A3 (220.0), C4 (261.63), E4 (329.63)
    for i in range(num_samples):
        t = i / SAMPLE_RATE
        s1 = math.sin(2 * math.pi * 174.61 * t) * 0.25
        s2 = math.sin(2 * math.pi * 220.00 * t) * 0.22
        s3 = math.sin(2 * math.pi * 261.63 * t) * 0.20
        s4 = math.sin(2 * math.pi * 329.63 * t) * 0.18
        wobble = 1.0 + 0.05 * math.sin(t * 2)
        samples.append((s1 + s2 + s3 + s4) * wobble * 0.6)
    return samples

def generate_camera_shutter():
    duration = 0.18
    num_samples = int(duration * SAMPLE_RATE)
    samples = []
    for i in range(num_samples):
        t = i / SAMPLE_RATE
        click1 = random.uniform(-1, 1) * math.exp(-t * 120) * 0.8
        t2 = max(0, t - 0.06)
        click2 = random.uniform(-1, 1) * math.exp(-t2 * 90) * 0.9 if t >= 0.06 else 0
        sine = math.sin(2 * math.pi * 180 * t) * math.exp(-t * 25) * 0.3
        samples.append((click1 + click2 + sine) * 0.9)
    return samples

def generate_laser_zap():
    duration = 0.18
    num_samples = int(duration * SAMPLE_RATE)
    samples = []
    for i in range(num_samples):
        t = i / SAMPLE_RATE
        progress = i / num_samples
        freq = 2400 * math.exp(-progress * 14) + 120
        env = math.exp(-progress * 8)
        saw = 2.0 * (t * freq - math.floor(t * freq + 0.5))
        samples.append(saw * env * 0.8)
    return samples

def generate_retro_coin():
    duration = 0.30
    num_samples = int(duration * SAMPLE_RATE)
    samples = []
    for i in range(num_samples):
        t = i / SAMPLE_RATE
        freq = 987.77 if t < 0.08 else 1318.51
        square = 1.0 if math.sin(2 * math.pi * freq * t) > 0 else -1.0
        env = math.exp(-((t % 0.08) if t < 0.08 else (t - 0.08)) * 12)
        samples.append(square * env * 0.6)
    return samples

def build_all_sfx(output_dir):
    os.makedirs(output_dir, exist_ok=True)
    generators = {
        # Whooshes
        "whoosh_fast.wav": generate_whoosh_fast,
        "whoosh_deep_bass.wav": generate_whoosh_deep,
        "whoosh_airy.wav": generate_whoosh_airy,
        "whoosh_subtle.wav": generate_whoosh_subtle,
        "whoosh_reverse.wav": generate_whoosh_reverse,
        "whoosh_laser.wav": generate_whoosh_laser,
        "whoosh_stutter.wav": generate_whoosh_stutter,
        # UI & Micro-interactions
        "pop_bubble_sticker.wav": generate_pop_bubble,
        "pop_crisp_caption.wav": generate_pop_crisp,
        "pop_cork.wav": generate_pop_cork,
        "pop_mouse_click.wav": generate_pop_mouse_click,
        "pop_water_drip.wav": generate_pop_water_drip,
        "swipe_card.wav": generate_swipe_card,
        "notification_iphone_ping.wav": generate_notification_iphone_ping,
        "typing_keyboard_click.wav": generate_typing_keyboard,
        # Emphasis & Alerts
        "ding_success_tip.wav": generate_ding_success,
        "fanfare_level_up.wav": generate_fanfare_level_up,
        "error_buzzer_wrong.wav": generate_error_buzzer,
        "censor_bleep_1000hz.wav": generate_censor_bleep,
        "record_scratch.wav": generate_record_scratch,
        "camera_shutter_snapshot.wav": generate_camera_shutter,
        "laser_zap_pointer.wav": generate_laser_zap,
        "coin_collect_arcade.wav": generate_retro_coin,
        # Impacts & Risers
        "bass_drop_boom.wav": generate_bass_drop_boom,
        "sub_rumble_drop.wav": generate_sub_rumble,
        "cinematic_braam_horn.wav": generate_cinematic_braam,
        "heartbeat_thump.wav": generate_heartbeat,
        "riser_tension_build.wav": generate_riser_tension,
        "riser_white_noise.wav": generate_riser_white_noise,
        "clock_tick_loop.wav": generate_clock_tick_loop,
        # Meme & Comedy
        "awkward_crickets.wav": generate_awkward_crickets,
        "spring_boing.wav": generate_spring_boing,
        "punch_boxing_hit.wav": generate_punch_boxing,
        "car_skid_brake.wav": generate_car_skid_brake,
        "sad_trombone_fail.wav": generate_sad_trombone,
        "crowd_cheer_applause.wav": generate_crowd_cheer,
        # Sci-Fi / Cyber
        "glitch_cyber_hit.wav": generate_glitch_cyber,
        "glitch_stutter_cut.wav": generate_glitch_stutter,
        "hologram_scan_beam.wav": generate_hologram_scan,
        "power_down_shutdown.wav": generate_power_down,
        "shield_deflect.wav": generate_shield_deflect,
        # Ambient Fillers
        "ambient_room_tone.wav": generate_room_tone,
        "vinyl_crackle_lofi.wav": generate_vinyl_crackle,
        "lofi_drone_bed.wav": generate_lofi_drone,
    }
    
    print(f"Generating {len(generators)} studio SFX audio files into: {output_dir}")
    for filename, func in generators.items():
        filepath = os.path.join(output_dir, filename)
        samples = func()
        write_wav(filepath, samples)
        print(f"  [OK] Created: {filename}")

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    build_all_sfx(os.path.join(current_dir, "wav_files"))
