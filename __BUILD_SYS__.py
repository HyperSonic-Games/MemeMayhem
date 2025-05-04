import PyInstaller.__main__
import os
import shutil

ICON_PATH = os.path.join("Assets", "Images", "IconsAndLogos", "MMLogo.ico")
OUTPUT_DIR = "output"
DEV_MODE = True  # Toggle this for dev vs prod

def WriteConfig():
    """Safely updates or writes Config.py with the DEV_MODE setting, preserving the header comment."""
    header = "# NOTE: THIS FILE'S DATA IS AUTO GENERATED\n"
    dev_line = f"DEV_MODE = {DEV_MODE}\n"
    lines = []

    # If file exists, try to preserve the header and replace DEV_MODE
    if os.path.exists("Config.py"):
        with open("Config.py", "r") as f:
            for line in f:
                if line.strip().startswith("DEV_MODE"):
                    continue  # skip old DEV_MODE line
                lines.append(line)

    # Ensure the header is at the top
    if not lines or not lines[0].strip().startswith("# NOTE:"):
        lines.insert(0, header)
    elif lines[0].strip() != header.strip():
        lines[0] = header  # replace outdated header if needed

    # Append updated DEV_MODE line
    lines.append(dev_line)

    # Write back the file
    with open("Config.py", "w") as f:
        f.writelines(lines)


def BuildClient():
    args = [
        '--onefile',
        '--icon', ICON_PATH,
        '--distpath', OUTPUT_DIR,
        'Client.py'
    ]
    if not DEV_MODE:
        args.insert(1, '--windowed')
    PyInstaller.__main__.run(args)

def BuildServer():
    args = [
        '--onefile',
        '--icon', ICON_PATH,
        '--distpath', OUTPUT_DIR,
        'Server.py'
    ]
    PyInstaller.__main__.run(args)  # Server is CLI by default

def BuildMain():
    args = [
        '--onefile',
        '--icon', ICON_PATH,
        '--distpath', OUTPUT_DIR,
        'Main.py'
    ]
    if not DEV_MODE:
        args.insert(1, '--windowed')
    PyInstaller.__main__.run(args)

def CopyFiles():
    """Copies necessary files to the output directory."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    shutil.copy("SETTINGS.toml", OUTPUT_DIR)
    shutil.copytree("Assets", os.path.join(OUTPUT_DIR, "Assets"), dirs_exist_ok=True)

# Write config
WriteConfig()

# Build executables
BuildMain()
BuildClient()
BuildServer()

# Copy files
CopyFiles()
