import PyInstaller.__main__
import os
import shutil
import subprocess
import argparse
import sys


os.environ["PYTHONPATH"] = "."

ICON_PATH = os.path.join("Assets", "Images", "IconsAndLogos", "MMLogo.ico")
OUTPUT_DIR = "output"
DEV_MODE = True  # Overwritten by --prod

def WriteConfig():
    header = "# NOTE: THIS FILE'S DATA IS AUTO GENERATED\n"
    dev_line = f"DEV_MODE = {DEV_MODE}\n"
    lines = []

    if os.path.exists("Config.py"):
        with open("Config.py", "r") as f:
            for line in f:
                if line.strip().startswith("DEV_MODE"):
                    continue
                lines.append(line)

    if not lines or not lines[0].strip().startswith("# NOTE:"):
        lines.insert(0, header)
    elif lines[0].strip() != header.strip():
        lines[0] = header

    # Remove any trailing blank lines before appending
    while lines and lines[-1].strip() == "":
        lines.pop()

    lines.append(dev_line)

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
    PyInstaller.__main__.run(args)

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

def BuildPVE():
    args = [
        '--onefile',
        '--icon', ICON_PATH,
        '--distpath', OUTPUT_DIR,
        'PVE/PVE.py'
    ]
    
    if not DEV_MODE:
        args.insert(1, '--windowed')
    PyInstaller.__main__.run(args)


def CopyFiles():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    shutil.copy("LICENSE", OUTPUT_DIR)
    shutil.copy("LICENSE_Pyinstaller", OUTPUT_DIR)
    shutil.copy("SETTINGS.toml", OUTPUT_DIR)
    shutil.copytree("Assets", os.path.join(OUTPUT_DIR, "Assets"), dirs_exist_ok=True)

def BuildDocs():
    process = subprocess.Popen(
        ["naturaldocs", "-p", "ND Config"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        stdin=subprocess.PIPE
    )
    stdout, stderr = process.communicate()
    if stderr:
        print("Error during Natural Docs execution:", stderr.decode())
    else:
        print("Natural Docs completed successfully.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build system for Meme Mayhem")
    parser.add_argument("--docs-only", action="store_true", help="Build documentation only")
    parser.add_argument("--no-docs", action="store_true", help="Skip documentation generation")
    parser.add_argument("--prod", action="store_true", help="Enable production mode (disables DEV_MODE)")
    args = parser.parse_args()

    # No args = show help and exit
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    # Conflicting flags: --docs-only and --no-docs
    if args.docs_only and args.no_docs:
        print("Error: --docs-only and --no-docs cannot be used together.")
        sys.exit(1)

    if args.prod:
        DEV_MODE = False

    WriteConfig()

    if not args.docs_only:
        BuildPVE()
        BuildMain()
        BuildClient()
        BuildServer()
        CopyFiles()

    if not args.no_docs:
        BuildDocs()
