#!/usr/bin/env python3
"""
Generate responsive images from default images for each directory
"""

import os
import sys
from pathlib import Path
from PIL import Image
import json

# Responsive sizes (width only, height auto)
RESPONSIVE_SIZES = [180, 320, 480, 640, 768, 1024, 1280, 1536, 1920, 2560]

# Icon sizes for dvipicon
ICON_SIZES = [16, 32, 48, 72, 96, 128, 180, 192, 256, 512]

# WebP quality
WEBP_QUALITY = 85

def generate_responsive_images(source_image, output_dir, is_icon=False):
    """Generate responsive images from source"""
    
    if not Path(source_image).exists():
        print(f"⚠️  Source image not found: {source_image}")
        return []
    
    sizes = ICON_SIZES if is_icon else RESPONSIVE_SIZES
    
    generated_files = []
    
    try:
        with Image.open(source_image) as img:
            # Convert to RGB if necessary
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            original_width, original_height = img.size
            
            for size in sizes:
                if size > original_width and not is_icon:
                    continue  # Don't upscale regular images
                
                # Calculate proportional height
                ratio = size / original_width
                new_height = int(original_height * ratio)
                
                # Resize image
                resized = img.resize((size, new_height), Image.Resampling.LANCZOS)
                
                # Generate filename
                source_stem = Path(source_image).stem
                if is_icon:
                    filename = f"{source_stem}-{size}x{size}.webp"
                else:
                    filename = f"{source_stem}-{size}w.webp"
                
                output_path = Path(output_dir) / 'resized' / filename
                
                # Save as WebP
                resized.save(
                    output_path,
                    'WEBP',
                    quality=WEBP_QUALITY,
                    optimize=True,
                    method=6
                )
                
                generated_files.append({
                    'size': size,
                    'width': size,
                    'height': new_height,
                    'filename': filename,
                    'path': str(output_path)
                })
                
                print(f"  ✓ Generated: {filename} ({size}x{new_height})")
    
    except Exception as e:
        print(f"❌ Error processing {source_image}: {e}")
    
    return generated_files

def main():
    """Main function to process all directories"""
    
    print("🚀 Starting responsive image generation...")
    print("=" * 50)
    
    # Directory configuration
    directories = {
        'dvip1': 'dvip1.webp',
        'dvip2': 'dvip2.webp',
        'dvip3': 'dvip3.webp',
        'dvip4': 'dvip4.webp',
        'dvipicon': 'dvipicon512.webp'  # Using largest icon as source
    }
    
    all_generated = {}
    
    for dir_name, source_file in directories.items():
        print(f"\n📁 Processing {dir_name}...")
        
        # Check if source exists in root
        if Path(source_file).exists():
            source_path = source_file
        elif Path(dir_name) / source_file.split('/')[-1]:
            # Check in directory
            source_path = Path(dir_name) / source_file.split('/')[-1]
        else:
            print(f"  ⚠️  Source not found for {dir_name}")
            continue
        
        # Generate images
        is_icon = dir_name == 'dvipicon'
        generated = generate_responsive_images(
            source_path,
            dir_name,
            is_icon=is_icon
        )
        
        # Copy original to directory if not already there
        if Path(source_file).exists() and not (Path(dir_name) / Path(source_file).name).exists():
            import shutil
            shutil.copy2(source_file, dir_name)
            print(f"  ✓ Copied original to {dir_name}/")
        
        all_generated[dir_name] = generated
    
    # Generate manifest file
    manifest = {
        'generated': all_generated,
        'directories': list(directories.keys()),
        'timestamp': str(Path(__file__).stat().st_mtime)
    }
    
    with open('image-manifest.json', 'w') as f:
        json.dump(manifest, f, indent=2)
    
    print("\n" + "=" * 50)
    print("✅ Image generation completed!")
    print(f"📁 Check the 'resized' folder in each directory")
    print("📄 Manifest saved: image-manifest.json")
    print("=" * 50)

if __name__ == "__main__":
    main()
