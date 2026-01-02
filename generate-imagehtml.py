#!/usr/bin/env python3
"""
Generate HTML with srcset for all images
"""

import json
from pathlib import Path

def generate_img_html(image_name, directory, widths, is_icon=False):
    """Generate HTML img tag with srcset"""
    
    if is_icon:
        # For icons, use sizes attribute
        srcset = []
        for width in widths:
            srcset.append(f"/{directory}/resized/{image_name}-{width}x{width}.webp {width}w")
        
        html = f'''<img 
    src="/{directory}/{image_name}.webp" 
    srcset="{', '.join(srcset)}"
    sizes="(max-width: 48px) 48px, (max-width: 96px) 96px, 128px"
    alt="{directory} icon"
    width="512"
    height="512"
    loading="lazy"
    class="responsive-icon"
>'''
    else:
        # For regular images
        srcset = []
        for width in widths:
            srcset.append(f"/{directory}/resized/{image_name}-{width}w.webp {width}w")
        
        # Add original
        srcset.append(f"/{directory}/{image_name}.webp {widths[-1]}w")
        
        html = f'''<img 
    src="/{directory}/resized/{image_name}-640w.webp" 
    srcset="{', '.join(srcset)}"
    sizes="(max-width: 640px) 100vw, (max-width: 1024px) 50vw, 33vw"
    alt="{directory} image"
    width="1024"
    height="auto"
    loading="lazy"
    class="responsive-image"
>'''
    
    return html

def main():
    """Generate HTML files for each directory"""
    
    print("🛠️  Generating HTML with srcset...")
    
    directories = ['dvip1', 'dvip2', 'dvip3', 'dvip4', 'dvipicon']
    
    for directory in directories:
        print(f"\n📁 Generating HTML for {directory}...")
        
        # Find the source image in the directory
        dir_path = Path(directory)
        webp_files = list(dir_path.glob("*.webp"))
        
        if not webp_files:
            print(f"  ⚠️  No WebP files found in {directory}")
            continue
        
        # Use the first WebP file as source
        source_file = webp_files[0]
        image_stem = source_file.stem
        
        # Define widths based on directory type
        if directory == 'dvipicon':
            widths = [48, 72, 96, 128, 180, 192, 256, 512]
            is_icon = True
        else:
            widths = [320, 480, 640, 768, 1024, 1280, 1536]
            is_icon = False
        
        # Generate HTML
        html_content = generate_img_html(image_stem, directory, widths, is_icon)
        
        # Save HTML snippet
        output_file = f"sizes/{directory}-srcset.html"
        Path('sizes').mkdir(exist_ok=True)
        
        with open(output_file, 'w') as f:
            f.write(html_content)
        
        print(f"  ✓ HTML saved: {output_file}")
        
        # Also create a demo HTML file
        demo_html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{directory} - Responsive Image Demo</title>
    <style>
        body {{ 
            font-family: Arial, sans-serif; 
            max-width: 1200px; 
            margin: 0 auto; 
            padding: 20px; 
        }}
        .image-container {{ 
            margin: 40px 0; 
            text-align: center; 
        }}
        .responsive-image, .responsive-icon {{
            max-width: 100%;
            height: auto;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }}
        .responsive-icon {{
            border-radius: 50%;
        }}
        .code-block {{
            background: #f5f5f5;
            padding: 20px;
            border-radius: 8px;
            margin: 20px 0;
            overflow-x: auto;
        }}
    </style>
</head>
<body>
    <h1>{directory} - Responsive Image Demo</h1>
    
    <div class="image-container">
        {html_content}
    </div>
    
    <div class="code-block">
        <h3>HTML Code:</h3>
        <pre><code>{html_content}</code></pre>
    </div>
    
    <p>📁 Files generated in: <code>/{directory}/resized/</code></p>
</body>
</html>'''
        
        demo_file = f"sizes/{directory}-demo.html"
        with open(demo_file, 'w') as f:
            f.write(demo_html)
        
        print(f"  ✓ Demo page: {demo_file}")
    
    print("\n" + "=" * 50)
    print("✅ HTML generation completed!")
    print("📁 Check the 'sizes/' folder for generated HTML files")
    print("🌐 Open *-demo.html files in browser to test")
    print("=" * 50)

if __name__ == "__main__":
    main()
