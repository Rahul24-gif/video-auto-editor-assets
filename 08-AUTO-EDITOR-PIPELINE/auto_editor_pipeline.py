"""
Automated Video Editing Pipeline Controller (Reorganized Clean Structure)
Connects all 8 category folders into a unified video editing workflow:
- 01-SOUNDS (SFX, BGM, Audio Ducking, Crossfading)
- 02-ANIMATIONS (Camera Zooms, Impact Shakes, Ken Burns, Face Tracking, Speed Ramping)
- 03-TRANSITIONS (FFmpeg Filters, GLSL Shaders, Bezier Curves)
- 04-EFFECTS-AND-FILTERS (3D LUTs, Color Matrix, Particle Overlays, VHS OSD)
- 05-TEXT-AND-CAPTIONS (ASS Subtitles, Caption Styles, Lower Thirds, Social Mockups)
- 06-OVERLAYS-AND-STICKERS (Reaction Badges, Pointers, 50/50 Split Screens)
- 07-BROLL-AND-AI-INTELLIGENCE (Keyword Matching, Soundwave Visualizers, Backdrops)
"""

import json
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

class AutoVideoEditorPipeline:
    def __init__(self, asset_root_dir):
        self.root_dir = os.path.abspath(asset_root_dir)
        self.sounds_dir = os.path.join(self.root_dir, "01-SOUNDS")
        self.animations_dir = os.path.join(self.root_dir, "02-ANIMATIONS")
        self.transitions_dir = os.path.join(self.root_dir, "03-TRANSITIONS")
        self.effects_dir = os.path.join(self.root_dir, "04-EFFECTS-AND-FILTERS")
        self.captions_dir = os.path.join(self.root_dir, "05-TEXT-AND-CAPTIONS")
        self.overlays_dir = os.path.join(self.root_dir, "06-OVERLAYS-AND-STICKERS")
        self.broll_dir = os.path.join(self.root_dir, "07-BROLL-AND-AI-INTELLIGENCE")
        
        # Load Catalogs
        with open(os.path.join(self.sounds_dir, "sfx_catalog.json"), "r") as f:
            self.sfx_catalog = json.load(f)["sounds"]
            
        with open(os.path.join(self.transitions_dir, "ffmpeg_transitions.json"), "r") as f:
            self.transitions = json.load(f)["transitions"]
            
        with open(os.path.join(self.captions_dir, "caption_styles.json"), "r") as f:
            self.caption_styles = json.load(f)["styles"]
            
        with open(os.path.join(self.animations_dir, "camera_zooms.json"), "r") as f:
            self.zoom_presets = json.load(f)["presets"]

        with open(os.path.join(self.broll_dir, "broll_keywords_dictionary.json"), "r") as f:
            self.keyword_dict = json.load(f)["dictionary"]

    def build_editing_recipe(self, raw_video_path, cut_events, output_recipe_json="timeline_recipe.json"):
        timeline = []
        for event in cut_events:
            event_type = event.get("type")
            t = event.get("timestamp_sec")
            word = event.get("keyword", "").lower()
            
            # Check intelligent keyword trigger
            matched_broll = self.keyword_dict.get(word, None)
            
            if matched_broll:
                timeline.append({
                    "time": t,
                    "action": "trigger_broll",
                    "keyword": word,
                    "broll_tags": matched_broll["broll_tags"],
                    "motion": matched_broll["motion"],
                    "sfx": os.path.join(self.sounds_dir, "sfx-wav-files", f"{matched_broll['sfx']}.wav"),
                    "sticker": matched_broll.get("sticker")
                })
            elif event_type == "jump_cut":
                timeline.append({
                    "time": t,
                    "action": "cut_with_zoom",
                    "zoom_factor": 1.20,
                    "sfx": os.path.join(self.sounds_dir, "sfx-wav-files", "whoosh_fast.wav"),
                    "sfx_start_time": max(0, t - 0.08)
                })
            elif event_type == "important_tip":
                timeline.append({
                    "time": t,
                    "action": "highlight_tip",
                    "caption_style": self.caption_styles["hormozi_bold"],
                    "sfx": os.path.join(self.sounds_dir, "sfx-wav-files", "ding_success_tip.wav"),
                    "sfx_start_time": t
                })
            elif event_type == "meme_punchline":
                timeline.append({
                    "time": t,
                    "action": "impact_shake",
                    "sfx": os.path.join(self.sounds_dir, "sfx-wav-files", "bass_drop_boom.wav"),
                    "sfx_start_time": t
                })
                
        recipe = {
            "source_video": raw_video_path,
            "target_resolution": [1080, 1920],
            "color_grading_lut": os.path.join(self.effects_dir, "3d-luts-cube-files", "cinematic_teal_orange.cube"),
            "bgm_track": os.path.join(self.sounds_dir, "bgm-music-tracks", "bgm_lofi_chill_groove_90bpm.wav"),
            "events": timeline
        }
        
        with open(output_recipe_json, "w") as f:
            json.dump(recipe, f, indent=2)
            
        print(f"[OK] Timeline recipe generated with {len(timeline)} automated edits!")
        return recipe

    def generate_ffmpeg_command(self, raw_video, output_video, lut_name="cinematic_teal_orange.cube"):
        lut_path = os.path.join(self.effects_dir, "3d-luts-cube-files", lut_name).replace("\\", "/")
        cmd = f'ffmpeg -i "{raw_video}" -vf "lut3d=file=\'{lut_path}\'" -c:v libx264 -crf 18 -preset fast -c:a aac -b:a 192k "{output_video}"'
        return cmd

if __name__ == "__main__":
    asset_base = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    pipeline = AutoVideoEditorPipeline(asset_base)
    
    sample_analysis_events = [
        {"type": "jump_cut", "timestamp_sec": 2.45, "keyword": "fast"},
        {"type": "important_tip", "timestamp_sec": 5.80, "keyword": "money"},
        {"type": "meme_punchline", "timestamp_sec": 9.20, "keyword": "warning"}
    ]
    
    recipe = pipeline.build_editing_recipe(
        raw_video_path="raw_footage.mp4",
        cut_events=sample_analysis_events,
        output_recipe_json=os.path.join(asset_base, "sample_timeline_recipe.json")
    )
    
    print("\nGenerated FFmpeg Command:")
    print(pipeline.generate_ffmpeg_command("input.mp4", "output_color_graded.mp4"))
