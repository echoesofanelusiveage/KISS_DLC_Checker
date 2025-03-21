import os
import sys
import re
from collections import defaultdict

GAME_CONFIG = {
    'CM3D2': {
        'dirs': ['GameData'],
        'extension': '.arc',
        'sections': [('cm3d2plg', 'GameData')]
    },
    'COM3D2': {
        'dirs': ['GameData', 'GameData_20'],
        'extension': '.arc',
        'sections': [('com3d2plg', 'GameData'), ('cm3d2plg', 'GameData_20')]
    },
    'CREditSystem': {
        'dirs': [os.path.join('GameData', 'dlc')],
        'extension': '.aba',
        'sections': [('creplg', os.path.join('GameData', 'dlc'))]
    }
}

EXE_MAP = {k.lower(): v for k, v in {
    'cm3d2.exe': 'CM3D2',
    'com3d2.exe': 'COM3D2',
    'cr editsystem.exe': 'CREditSystem'
}.items()}

SECTION_MAPPING = {f"#{k}": k for k in ['cm3d2plg', 'com3d2plg', 'creplg']}

LINE_FORMAT = re.compile(r'^[^,\n]+,\s*\S+.*$')
COLOR_CODES = {"red": "\033[91m", "yellow": "\033[93m", "cyan": "\033[96m", "reset": "\033[0m"}

def print_color(text, color):
    print(f"{COLOR_CODES[color]}{text}{COLOR_CODES['reset']}")

def normalize_filename(filename, target_ext=None):
    norm_name = os.path.normcase(filename).strip()
    if not norm_name or (target_ext and not norm_name.lower().endswith(target_ext.lower())):
        return None, False
    return norm_name, True

def detect_game_type():
    return next((EXE_MAP[entry.name.lower()] for entry in os.scandir() 
                if entry.is_file() and entry.name.lower() in EXE_MAP), None)

def parse_kiss_dlc():
    sections = defaultdict(list)
    version = current_section = None
    
    try:
        with open("kiss_dlc.txt", "r", encoding="utf-8") as f:
            for ln, line in enumerate(f, 1):
                if not (line := line.strip()):
                    continue
                if line.startswith('#Ver.'):
                    version = line[5:].strip()
                    current_section = None
                elif line.startswith('#'):
                    current_section = SECTION_MAPPING.get(line)
                elif current_section and LINE_FORMAT.match(line):
                    if len(parts := line.split(',', 1)) == 2:
                        if all(parts := list(map(str.strip, parts))):
                            sections[current_section].append(tuple(parts))
                            continue
                    print_color(f"Line {ln}: Invalid entry - '{line}'", "yellow")
    except Exception as e:
        print_color(f"{getattr(e, 'strerror', str(e))}", "red")
        raise
    
    return dict(sections), version

def read_dlc_list(game_type):
    if (config := GAME_CONFIG.get(game_type)) is None:
        raise ValueError(f"Unsupported game: {game_type}")
    target_ext = config['extension'].lower()
    sections, version = parse_kiss_dlc()
    return {
        dk: {fn: dn for fn, dn in (
            (normalize_filename(fn, target_ext)[0], dn) 
            for fn, dn in sections.get(sk, [])
        ) if fn}
        for sk, dk in config['sections']
    }, version

def scan_gamedata(game_type):
    config = GAME_CONFIG.get(game_type)
    suffix = f'_2{config["extension"].lower()}'
    return [
        (d, entry.name, nf)
        for d in config['dirs']
        for entry in os.scandir(os.path.join(os.getcwd(), d))
        if entry.is_file()
        and (nf := normalize_filename(entry.name, config["extension"])[0]) is not None
        and not nf.endswith(suffix)
    ]

def analyze_dlc(dlc_map, game_files):
    file_map = {k: set(v.keys()) for k, v in dlc_map.items()}
    installed = set()
    unknown = []
    
    for d, original_name, nf in game_files:
        if nf in file_map.get(d, set()):
            installed.add(dlc_map[d][nf])
        else:
            unknown.append(os.path.join(d, original_name))
    
    all_dlc = {dn for sm in dlc_map.values() for dn in sm.values()}
    return sorted(installed), sorted(all_dlc - installed), sorted(unknown)

def print_results(version, installed, missing, unknown):
    if version:
        print_color(f"GitHub: https://github.com/echoesofanelusiveage/KISS_DLC_Checker\nVersion: {version}\n", "cyan")
        for title, items in [("Installed DLCs", installed), ("Missing DLCs", missing)]:
            print_color(f"\n{title}:", "cyan")
            print('\n'.join(f"  {i}" for i in items))
    
    if unknown:
        try:
            with open("kiss_dlc_unknown.txt", "w", encoding="utf-8") as f:
                f.write('\n'.join(unknown))
            print_color("\nUnknown files saved to kiss_dlc_unknown.txt", "yellow")
        except OSError as e:
            print_color(f"\nWrite error: {e}", "red")

if __name__ == "__main__":
    try:
        os.path.exists("kiss_dlc.txt") or (print_color("Error: kiss_dlc.txt missing", "red") and sys.exit(1))
        game_type = detect_game_type()
        if not game_type:
            print_color("Error: Game not detected", "red")
            sys.exit(1)
        dlc_map, version = read_dlc_list(game_type)
        results = analyze_dlc(dlc_map, scan_gamedata(game_type))
        print_results(version, *results)
    except Exception as e:
        print_color(f"\nError: {e}", "red")
        sys.exit(1)
    finally:
        input("\nPress Enter to exit...")