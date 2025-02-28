<div align="center">

<h1>KISS_DLC_Checker</h1>
  
A minimalist DLC verification tool for CM3D2/COM3D2/CR EditSystem.<br><br>
  
[![License](https://img.shields.io/badge/LICENSE-MIT-green.svg?style=for-the-badge)](https://github.com/echoesofanelusiveage/KISS_DLC_Checker/blob/main/LICENSE)

</div>

---

## How to use

将 kiss_dlc.txt 和 kiss_dlc_checker.py 放入游戏根目录（含 CM3D2.exe、COM3D2.exe 或 CR EditSystem.exe 的文件夹），双击 kiss_dlc_checker.py 或通过命令行运行。

kiss_dlc.txt と kiss_dlc_checker.py をゲームのルートフォルダ（CM3D2.exe、COM3D2.exe または CR EditSystem.exe があるフォルダ）に配置し、kiss_dlc_checker.py をダブルクリックするか、コマンドラインから実行してください。

Place kiss_dlc.txt and kiss_dlc_checker.py in the game root folder (where CM3D2.exe, COM3D2.exe, or CR EditSystem.exe is located), then double-click kiss_dlc_checker.py or run it via command line.

```bash
python kiss_dlc_check.py
```

## Script functions

列出已安装和未安装的 DLC。将无法读取的文件记录到 kiss_dlc_unknown.txt。

インストール済みおよび未インストールの DLC をリスト表示。読み取れないファイルを kiss_dlc_unknown.txt に記録。

List installed and uninstalled DLCs.Write unreadable files to kiss_dlc_unknown.txt.

## Credits
Special thanks to the following projects:
- [COM3D2_DLC_Checker](https://github.com/Tankerch/COM3D2_DLC_Checker)
- [COM3D2_DLC_Checker](https://github.com/krypto5863/COM3D2_DLC_Checker)
