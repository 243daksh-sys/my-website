import os

file_path = r"e:\Projects\chilli_leaf_ai\app\templates\index.html"
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

replacements = {
    # File refs
    "vines.png": "cave_vines.png",
    
    # Text
    "Forest Theme": "Lush Cave Theme",
    "Forest Vibe": "Lush Cave Vibe",
    "the forest warns": "the cave echoes",
    "the forest fades": "the cave goes dark",
    "Forest Spirit": "Cave Spirit",
    "Listening to nature": "Listening to the cave's echoes",
    "Explore the Chilli Leaf AI": "Delve into the Chilli Leaf AI",
    
    # Colors
    "--ds-bg-dark: #071a10;": "--ds-bg-dark: #0f1412;",
    "--ds-bg-light: #12291c;": "--ds-bg-light: #16201d;",
    "--ds-firefly: #4ade80;": "--ds-firefly: #10b981;",
    "--ds-firefly-glow: #22c55e;": "--ds-firefly-glow: #06b6d4;",
    "--ds-gold: #fef08a;": "--ds-gold: #34d399;",
    "--ds-gold-dim: #b4c58d;": "--ds-gold-dim: #059669;",
    "--ds-text: #f0fdf4;": "--ds-text: #f4fdfc;",
    "--ds-text-dim: #a7f3d0;": "--ds-text-dim: #99f6e4;",
    "--ds-border: rgba(167, 243, 208, 0.2);": "--ds-border: rgba(153, 246, 228, 0.2);",
    "--ds-panel: rgba(7, 26, 16, 0.85);": "--ds-panel: rgba(15, 20, 18, 0.85);",
    
    # Canvas and shadow colors
    "#4ade80": "#10b981", # spore main background / canvas
    "#22c55e": "#06b6d4", # canvas shadow / glows
    "rgba(254, 240, 138, ": "rgba(52, 211, 153, ",
    "rgba(74, 222, 128, ": "rgba(16, 185, 129, ",
    "rgba(34, 197, 94, ": "rgba(6, 182, 212, ",
    "rgba(180, 197, 141, ": "rgba(5, 150, 105, ",
    "rgba(254,240,138,": "rgba(52,211,153,",
    "rgba(74,222,128,": "rgba(16,185,129,",
    
    # Animation/Name Refs
    "fireflies-canvas": "glowworms-canvas",
    "animateFireflies": "animateGlowworms",
    "fireflies": "glowworms",
    "Firefly": "Glowworm",
    "Fireflys Background": "Glowworms Background"
}

for old, new in replacements.items():
    content = content.replace(old, new)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"Successfully converted to Lush Cave theme in {file_path}")
