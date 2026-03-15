with open("README.md", "r") as f:
    content = f.read()

# Make sure we don't duplicate
if "## UI Previews" not in content:
    print("UI previews not found")
else:
    print("README has images, no need to update since images are overwritten in place.")
