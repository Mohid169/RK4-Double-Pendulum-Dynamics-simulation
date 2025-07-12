#!/usr/bin/env python3
"""
Convert MP4 demo video to GIF for GitHub README compatibility.
"""

import imageio
import os
import sys

def convert_mp4_to_gif(mp4_path, gif_path, fps=10, scale=0.5):
    """
    Convert MP4 to GIF with optimization for GitHub.
    
    Args:
        mp4_path: Path to input MP4 file
        gif_path: Path to output GIF file
        fps: Target FPS for GIF (lower = smaller file)
        scale: Scale factor (0.5 = half size)
    """
    print(f"🎬 Converting {mp4_path} to {gif_path}...")
    
    # Read the MP4 file
    reader = imageio.get_reader(mp4_path)
    
    # Get video properties
    meta = reader.get_meta_data()
    original_fps = meta.get('fps', 30)
    
    # Calculate frame skip to achieve target FPS
    frame_skip = max(1, int(original_fps / fps))
    
    frames = []
    for i, frame in enumerate(reader):
        if i % frame_skip == 0:  # Skip frames to reduce FPS
            if scale != 1.0:
                # Resize frame
                import numpy as np
                h, w = frame.shape[:2]
                new_h, new_w = int(h * scale), int(w * scale)
                # Simple nearest neighbor resize
                frame = frame[::int(1/scale), ::int(1/scale)]
            frames.append(frame)
    
    reader.close()
    
    # Save as GIF with optimization
    print(f"📁 Saving GIF with {len(frames)} frames...")
    imageio.mimsave(
        gif_path, 
        frames, 
        fps=fps,
        loop=0,  # Infinite loop
        optimize=True,
        palettesize=256
    )
    
    # Check file sizes
    mp4_size = os.path.getsize(mp4_path) / (1024 * 1024)  # MB
    gif_size = os.path.getsize(gif_path) / (1024 * 1024)  # MB
    
    print(f"✅ Conversion complete!")
    print(f"📊 Original MP4: {mp4_size:.1f} MB")
    print(f"📊 Optimized GIF: {gif_size:.1f} MB")
    print(f"📊 Size reduction: {((mp4_size - gif_size) / mp4_size * 100):.1f}%")

def main():
    # Find the most recent demo video
    demo_files = [f for f in os.listdir('.') if f.startswith('pendulum_demo_') and f.endswith('.mp4')]
    
    if not demo_files:
        print("❌ No demo MP4 files found!")
        print("Run 'python scripts/create_demo.py' first to create a demo video.")
        return
    
    # Use the most recent demo file
    demo_files.sort(reverse=True)
    mp4_file = demo_files[0]
    gif_file = mp4_file.replace('.mp4', '.gif')
    
    print(f"🎯 Converting {mp4_file} to {gif_file}")
    
    try:
        convert_mp4_to_gif(mp4_file, gif_file, fps=8, scale=0.8)
        print(f"🎉 Ready for GitHub! Add this to your README:")
        print(f"![Demo]({gif_file})")
        
    except Exception as e:
        print(f"❌ Error during conversion: {e}")
        return

if __name__ == "__main__":
    main() 