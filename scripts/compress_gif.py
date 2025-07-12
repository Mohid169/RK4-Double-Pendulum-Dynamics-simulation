#!/usr/bin/env python3
"""
Compress a large GIF file to make it suitable for GitHub display.
GitHub has a ~10MB limit for inline image display.
"""

import os
import sys
from PIL import Image, ImageSequence
import argparse

def compress_gif(input_path, output_path, target_size_mb=8, quality=85):
    """
    Compress a GIF file by reducing quality, frame rate, and size.
    
    Args:
        input_path: Path to input GIF
        output_path: Path to output compressed GIF
        target_size_mb: Target size in MB
        quality: Quality setting (1-100, lower = more compression)
    """
    print(f"📦 Compressing {input_path}...")
    
    # Open the original GIF
    with Image.open(input_path) as img:
        frames = []
        durations = []
        
        # Get original info
        original_size = os.path.getsize(input_path) / (1024 * 1024)
        print(f"Original size: {original_size:.1f} MB")
        print(f"Original dimensions: {img.size}")
        print(f"Original frames: {getattr(img, 'n_frames', 1)}")
        
        # Calculate new dimensions (reduce by 50% if too large)
        new_width = min(img.width, 500)  # Max width 500px
        new_height = int(img.height * (new_width / img.width))
        
        print(f"New dimensions: {new_width}x{new_height}")
        
        # Process frames (skip every other frame for smaller size)
        frame_skip = 2 if getattr(img, 'n_frames', 1) > 100 else 1
        frame_count = 0
        
        for i, frame in enumerate(ImageSequence.Iterator(img)):
            if i % frame_skip == 0:  # Skip frames to reduce size
                # Convert to RGB if necessary
                if frame.mode != 'RGB':
                    frame = frame.convert('RGB')
                
                # Resize frame
                frame = frame.resize((new_width, new_height), Image.Resampling.LANCZOS)
                
                # Reduce colors for smaller file size
                frame = frame.quantize(colors=128, method=Image.Quantize.MEDIANCUT)
                
                frames.append(frame)
                
                # Get duration (default 100ms if not available)
                duration = getattr(frame, 'info', {}).get('duration', 100)
                durations.append(duration * frame_skip)  # Adjust for skipped frames
                
                frame_count += 1
                
                if frame_count % 10 == 0:
                    print(f"Processed {frame_count} frames...")
        
        print(f"Final frame count: {len(frames)}")
        
        # Save compressed GIF
        if frames:
            frames[0].save(
                output_path,
                save_all=True,
                append_images=frames[1:],
                duration=durations,
                loop=0,
                optimize=True,
                quality=quality
            )
            
            # Check final size
            final_size = os.path.getsize(output_path) / (1024 * 1024)
            compression_ratio = (1 - final_size / original_size) * 100
            
            print(f"✅ Compressed GIF saved: {output_path}")
            print(f"Final size: {final_size:.1f} MB")
            print(f"Compression: {compression_ratio:.1f}%")
            
            if final_size <= target_size_mb:
                print(f"🎉 Success! File is under {target_size_mb}MB and will display on GitHub!")
            else:
                print(f"⚠️  File is still over {target_size_mb}MB. Consider further compression.")
        else:
            print("❌ No frames processed!")

def main():
    parser = argparse.ArgumentParser(description='Compress a GIF file for GitHub display')
    parser.add_argument('input', nargs='?', default='assets/demos/Demo.gif', 
                       help='Input GIF file path')
    parser.add_argument('output', nargs='?', default='assets/demos/Demo_compressed.gif',
                       help='Output GIF file path')
    parser.add_argument('--target-size', type=float, default=8.0,
                       help='Target size in MB (default: 8.0)')
    parser.add_argument('--quality', type=int, default=85,
                       help='Quality setting 1-100 (default: 85)')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.input):
        print(f"❌ Input file not found: {args.input}")
        sys.exit(1)
    
    # Create output directory if needed
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    
    try:
        compress_gif(args.input, args.output, args.target_size, args.quality)
    except Exception as e:
        print(f"❌ Error compressing GIF: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 