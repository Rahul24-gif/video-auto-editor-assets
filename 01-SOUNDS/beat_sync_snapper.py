"""
Beat-Sync Snapper for Video Auto-Editor Pipeline
Snaps cut timestamps to the nearest musical downbeat or 8th note grid based on BGM track BPM.
"""

def snap_timestamps_to_bpm_grid(raw_cut_timestamps, bpm=90, snap_grid=0.25, offset_sec=0.0):
    """
    raw_cut_timestamps: list of float seconds [2.31, 5.82, 9.14]
    bpm: beats per minute of the background music (e.g. 90, 120, 128)
    snap_grid: 1.0 (whole beat), 0.5 (half beat / 8th note), 0.25 (16th note)
    Returns: list of snapped timestamps aligned to music rhythm.
    """
    seconds_per_beat = 60.0 / bpm
    grid_interval = seconds_per_beat * snap_grid
    
    snapped = []
    for t in raw_cut_timestamps:
        rel_t = t - offset_sec
        # Find nearest grid step
        nearest_step = round(rel_t / grid_interval)
        snapped_t = max(0.0, (nearest_step * grid_interval) + offset_sec)
        snapped.append(round(snapped_t, 3))
        
    return snapped

if __name__ == "__main__":
    raw_cuts = [1.82, 3.45, 6.12, 8.94]
    snapped_90bpm = snap_timestamps_to_bpm_grid(raw_cuts, bpm=90, snap_grid=0.5)
    print("Raw cuts:      ", raw_cuts)
    print("Snapped (90BPM):", snapped_90bpm)
