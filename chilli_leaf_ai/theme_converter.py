import os

file_path = r"e:\Projects\chilli_leaf_ai\app\templates\index.html"
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

replacements = {
    # 1. Colors and Variables
    "--ds-bg-dark: #0a0a0a;": "--ds-bg-dark: #071a10;",
    "--ds-bg-light: #1c1816;": "--ds-bg-light: #12291c;",
    "--ds-ember: #e25822;": "--ds-ember: #4ade80;",
    "--ds-ember-glow: #ff7b00;": "--ds-ember-glow: #22c55e;",
    "--ds-gold: #cbb581;": "--ds-gold: #fef08a;",
    "--ds-gold-dim: #8b7952;": "--ds-gold-dim: #b4c58d;",
    "--ds-text: #d4d4d4;": "--ds-text: #f0fdf4;",
    "--ds-text-dim: #8a8a8a;": "--ds-text-dim: #a7f3d0;",
    "--ds-border: rgba(203, 181, 129, 0.2);": "--ds-border: rgba(167, 243, 208, 0.2);",
    "--ds-panel: rgba(20, 18, 17, 0.85);": "--ds-panel: rgba(7, 26, 16, 0.85);",
    # Specific colors inside CSS shadow backgrounds
    "rgba(203, 181, 129, ": "rgba(254, 240, 138, ",
    "rgba(226, 88, 34, ": "rgba(74, 222, 128, ",
    "rgba(255, 123, 0, ": "rgba(34, 197, 94, ",
    "rgba(139, 121, 82, ": "rgba(180, 197, 141, ",
    "rgba(203,181,129,": "rgba(254,240,138,",
    "rgba(226,88,34,": "rgba(74,222,128,",

    # 2. Fonts
    "Dark Souls Theme": "Forest Theme",
    "Dark Souls Vibe": "Forest Vibe",
    "Cinzel:wght@400;600;700;800": "Playfair+Display:ital,wght@0,400;0,500;0,600;0,700;1,400",
    "'Cinzel', serif": "'Playfair Display', serif",

    # 3. Canvas id and function references (keep ID embers-canvas to minimize changes, but change references if wanted? Actually, I'll just change the text mentions and some ID's if possible, or leave ID as is and just change functionality).
    "animateEmbers": "animateFireflies",
    "embers": "fireflies",
    "Ember": "Firefly",
    "ember": "firefly",
    "Embers Background": "Fireflies Background",
    "Embers Background Animation": "Fireflies Background Animation",
    "#ff7b00": "#22c55e", # flame color in canvas
    "#ff4500": "#4ade80", # flame main color

    # 4. Loader
    "bonfire-loader": "nature-loader",
    "flame": "spore",

    # 5. UI Text
    "Behold the Chilli Leaf AI": "Explore the Chilli Leaf AI",
    "Uncover the blight that afflicts your crops": "Discover the health of your crops",
    "Offer Your Leaf Image": "Upload Your Leaf Image",
    "Kindle The Flame (Analyze)": "Analyze Leaf",
    "Gazing into the embers... Loading Image Data": "Listening to nature... Loading Image Data",
    "Soul resonance (Confidence)": "Confidence",
    "Offer Another Soul": "Analyze Another Leaf",
    "Arsenal of Skills": "My Skills",
    "The mastery required to forge the web": "The tools I use to build the web",
    "Unearthed Knowledge": "Research & Discovery",
    "Summon Me": "Contact Me",
    "Leave your sign": "Get in touch",
    "The flames decipher your words but alas, I am merely an echo. Seek the true Chili Leaf AI via the 'AI Models' tab above for analysis.": "Nature's whispers cannot decipher your words. Seek the true Chili Leaf AI via the 'AI Models' tab above for analysis.",
    "The embers scream: // ": "The forest warns: // ",
    "Invalid soul signature.": "Invalid leaf signature.",
    "The soul is too heavy. Maximum offering is 5MB.": "The image is too large. Maximum size is 5MB.",
    "MB Soul Readied": "MB Leaf Readied",
    "An arbitrary error occurred. The flame wanes.": "An arbitrary error occurred. The forest fades.",
    "Offered Leaf": "Uploaded Leaf",
    "Soul resonance": "Health resonance",

    # Chat guide
    "I am the AI construct of this domain.": "I am the Forest Spirit of this domain.",
    "Do you need guidance regarding the Chilli Leaf analysis?": "Do you seek guidance regarding the Chilli Leaf analysis?",
    
    # Specific class modifications for animation
    "transform: translateY(-5px)": "transform: translateY(-10px) rotate(5deg)",
}

for old, new in replacements.items():
    content = content.replace(old, new)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"Successfully updated {file_path}")
