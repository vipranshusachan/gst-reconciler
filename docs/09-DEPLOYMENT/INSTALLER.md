# Inno Setup Windows Installer Configuration

## 1. Installer Specification

The Windows installer is compiled using **Inno Setup 6**.

### Inno Setup Script (`installer/setup.iss`):
```iss
[Setup]
AppName=GST Reconciler
AppVersion=1.0.0
AppPublisher=Open Source GST Community
DefaultDirName={autopf}\GSTReconciler
DefaultGroupName=GST Reconciler
OutputDir=..\dist
OutputBaseFilename=GSTReconciler-Setup-v1.0.0
Compression=lzma2/ultra64
SolidCompression=yes
ArchitecturesInstallIn64BitMode=x64
PrivilegesRequired=lowest

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"

[Files]
Source: "..\dist\GSTReconciler\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\GST Reconciler"; Filename: "{app}\GSTReconciler.exe"
Name: "{autodesktop}\GST Reconciler"; Filename: "{app}\GSTReconciler.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\GSTReconciler.exe"; Description: "{cm:LaunchProgram,GST Reconciler}"; Flags: nowait postinstall skipifsilent
```
