
import os
import re
import shutil

# Explicit paths mapping across your NVMe SSD and 1TB HDD storage
source_dir = os.path.dirname(os.path.abspath(__file__))
build_dir = os.path.join(os.path.dirname(source_dir), "dist")
assets_src = os.path.join(source_dir, "assets")  # In-repo media (committed to git); Cloudflare R2 planned for a later release
assets_dst = os.path.join(build_dir, "assets")

# Ensure the workspace directory exists
os.makedirs(os.path.dirname(build_dir), exist_ok=True)

# Clean and rebuild target distribution folder
if os.path.exists(build_dir):
    shutil.rmtree(build_dir)
os.makedirs(os.path.join(build_dir, "en"), exist_ok=True)
os.makedirs(os.path.join(build_dir, "ta"), exist_ok=True)

# Constructing regex with concatenation so chat UIs cannot mistakenly hide it
pattern_str = "<!" + "--#\\s*include\\s+virtual=[\"']([^\"']+)[\"']\\s*--" + ">"
ssi_pattern = re.compile(pattern_str)

def find_file(virtual_path):
    """Finds include files relative to the development source structure."""
    clean_path = virtual_path.lstrip('/')
    
    candidates = [
        os.path.join(source_dir, clean_path),
        os.path.join(source_dir, "parts", os.path.basename(clean_path)),
        os.path.join(source_dir, os.path.basename(clean_path))
    ]
    
    for candidate in candidates:
        if os.path.exists(candidate) and os.path.isfile(candidate):
            return candidate
    return None

def process_file(file_path):
    """Recursively parses HTML components, converting dynamic SSI to static layouts."""
    if not os.path.exists(file_path):
        print(f"⚠️ Warning: Component missing: {file_path}")
        return f""
        
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    def replace_match(match):
        if len(match.groups()) > 0:
            virtual_path = match.group(1)
            inc_file = find_file(virtual_path)
            if inc_file:
                print(f"  -> Merging component: {virtual_path}")
                return process_file(inc_file)
            else:
                print(f"  ❌ Error: Could not resolve component: {virtual_path}")
                return f""
        return match.group(0)
            
    # Bounded iteration safety net - completely prevents any chance of terminal hanging
    for _ in range(10):
        if not ssi_pattern.search(content):
            break
        content = ssi_pattern.sub(replace_match, content)
        
    return content

print("🚀 Starting Production Build Pipeline...")
print(f"📄 Code Directory:   {source_dir}")
print(f"🖼️ Media Directory:  {assets_src}")
print(f"📦 Output Target:     {build_dir}\n")

# 1. Compile English Page from its subfolder path
print("Compiling en/index.html...")
en_html = process_file(os.path.join(source_dir, "en", "index.html"))
with open(os.path.join(build_dir, "en", "index.html"), "w", encoding="utf-8") as f:
    f.write(en_html)

# 2. Compile Tamil Page from its subfolder path
print("\nCompiling ta/index.html...")
ta_html = process_file(os.path.join(source_dir, "ta", "index.html"))
with open(os.path.join(build_dir, "ta", "index.html"), "w", encoding="utf-8") as f:
    f.write(ta_html)

# 3. Compile English Gallery page
print("\nCompiling en/gallery.html...")
en_gallery_html = process_file(os.path.join(source_dir, "en", "gallery.html"))
with open(os.path.join(build_dir, "en", "gallery.html"), "w", encoding="utf-8") as f:
    f.write(en_gallery_html)

# 4. Compile Tamil Gallery page
print("\nCompiling ta/gallery.html...")
ta_gallery_html = process_file(os.path.join(source_dir, "ta", "gallery.html"))
with open(os.path.join(build_dir, "ta", "gallery.html"), "w", encoding="utf-8") as f:
    f.write(ta_gallery_html)

# 5. Create Root Redirect File
root_index_content = """<!DOCTYPE html>
<html>
<head>
    <meta http-equiv="refresh" content="0; url=/en/">
    <script type="text/javascript">
        window.location.href = "/en/"
    </script>
    <title>International Educational Foundation</title>
</head>
<body>
    <p>Redirecting to the main page... If you are not forwarded, <a href="/en/">click here</a>.</p>
</body>
</html>
"""
with open(os.path.join(build_dir, "index.html"), "w", encoding="utf-8") as f:
    f.write(root_index_content)

# 6. Pull media assets from the 1TB HDD volume
if os.path.exists(assets_src):
    print(f"\n📦 Copying production media assets from HDD vault ({assets_src})...")
    shutil.copytree(assets_src, assets_dst)
    print(f"✅ Successfully compiled {len(os.listdir(assets_dst))} media assets.")
else:
    print(f"\n⚠️  Media directory not found at {assets_src}")
    print(f"   Skipping assets — existing Cloudflare CDN assets will be preserved.")
    print(f"   (Run deploy.sh locally to do a full asset deploy)")

print(f"\n🎉 Build Complete! Clean production distribution compiled at: {build_dir}")

