import os
import sys
import re

def detect_game_type():
    exe_map = {'cm3d2.exe': 'CM3D2', 'com3d2.exe': 'COM3D2', 'cr editsystem.exe': 'CREditSystem'}
    for f in os.listdir(os.getcwd()):
        if f.lower() in exe_map and f.endswith('.exe'):
            return exe_map[f.lower()]
    return None

def get_target_extension(game_type):
    return {'CM3D2': '.arc', 'COM3D2': '.arc', 'CREditSystem': '.aba'}.get(game_type, '')

def read_dlc_list(game_type):
    dlc_map = {}
    version = None
    target_ext = get_target_extension(game_type)
    try:
        with open("kiss_dlc.txt", "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f]
            if lines and lines[0].startswith('#'):
                version = lines[0][1:].strip()
                lines = lines[1:]
            lines = [line for line in lines if line and not line.startswith("#")]
    except FileNotFoundError:
        print_color("Error: kiss_dlc.txt not found", "red")
        sys.exit(1)

    for line in lines:
        if ',' not in line:
            print_color(f"Warning: Malformed line - {line}", "yellow")
            continue
        filename, dlc_name = line.split(',', 1)
        filename_lower = filename.lower()
        if target_ext and not filename_lower.endswith(target_ext.lower()):
            continue
        if game_type == "CM3D2":
            match = re.match(r'^parts_(dlc|cas)(\d+)\.arc$', filename_lower)
            if match:
                for prefix in ['material', 'menu', 'model', 'texture']:
                    new_name = f"{prefix}_{match.group(1)}{match.group(2)}.arc".lower()
                    dlc_map[new_name] = dlc_name
            else:
                dlc_map[filename_lower] = dlc_name
        else:
            dlc_map[filename_lower] = dlc_name
    return dlc_map, version

def scan_gamedata(game_type):
    dir_map = {
        'CM3D2': ['GameData', 'GameData_20'],
        'COM3D2': ['GameData', 'GameData_20'],
        'CREditSystem': [os.path.join('GameData', 'dlc')]
    }
    target_ext = get_target_extension(game_type)
    files = []
    for directory in dir_map.get(game_type, []):
        full_path = os.path.join(os.getcwd(), directory)
        if not os.path.isdir(full_path):
            print_color(f"Warning: {directory} not found", "yellow")
            continue
        try:
            files.extend(f for f in os.listdir(full_path) if os.path.isfile(os.path.join(full_path, f)))
        except Exception:
            continue
    if target_ext:
        target_ext = target_ext.lower()
        files = [f for f in files if f.lower().endswith(target_ext)]
    if game_type == 'CREditSystem':
        files = [f for f in files if not f.lower().endswith('_2.aba')]
    return files

def analyze_dlc(dlc_map, game_files):
    installed = set()
    unknown = []
    for f in game_files:
        f_lower = f.lower()
        if f_lower in dlc_map:
            installed.add(dlc_map[f_lower])
        else:
            unknown.append(f)
    missing = set(dlc_map.values()) - installed
    return sorted(installed), sorted(missing), sorted(unknown)

def print_results(version, installed, missing, unknown):
    def print_section(title, items):
        print_color(f"\n{title}:", "cyan")
        for item in items:
            print(item)
    
    if version:
        print_color(f"Version: {version}", "cyan")
    print_section("Installed", installed)
    print_section("Not Installed", missing)
    
    if unknown:
        try:
            with open("kiss_dlc_unknown.txt", "w", encoding="utf-8") as f:
                f.write("\n".join(unknown))
            print_color("\nUnknown files saved to kiss_dlc_unknown.txt", "yellow")
        except Exception as e:
            print_color(f"\nWrite error: {str(e)}", "red")

def print_color(text, color):
    codes = {"red": "\033[91m", "yellow": "\033[93m", "cyan": "\033[96m", "reset": "\033[0m"}
    print(f"{codes.get(color, '')}{text}{codes['reset']}")

if __name__ == "__main__":
    game_type = detect_game_type()
    if not game_type:
        print_color("Error: No supported game detected", "red")
        input("\nPress Enter to exit...")
        sys.exit(1)
    try:
        dlc_map, version = read_dlc_list(game_type)
        game_files = scan_gamedata(game_type)
    except Exception as e:
        print_color(f"Error: {str(e)}", "red")
        sys.exit(1)
    installed, missing, unknown = analyze_dlc(dlc_map, game_files)
    print_results(version, installed, missing, unknown)
    input("\nPress Enter to exit...")