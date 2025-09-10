# build/windows_installer.ps1

dir dist

param(
    [string]$AppName = "Secan",
    [string]$AppVersion = "0.1.0", 
    [string]$Publisher = "Secan",
    [string]$AppExe = "secan.exe"
)

# Create NSIS script content
$nsisScript = @"
!define APP_NAME "$AppName"
!define APP_VERSION "$AppVersion"
!define APP_PUBLISHER "$Publisher"
!define APP_EXE "$AppExe"

Name "`${APP_NAME}"
OutFile "secan-installer.exe"
InstallDir "`$PROGRAMFILES\`${APP_NAME}"
RequestExecutionLevel admin

# Modern UI
!include "MUI2.nsh"

# Pages
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_LICENSE "build\gpl-3.0.rtf"
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_UNPAGE_WELCOME
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES
!insertmacro MUI_UNPAGE_FINISH

# Languages
!insertmacro MUI_LANGUAGE "English"

# Version Info
VIProductVersion "$AppVersion.0"
VIAddVersionKey "ProductName" "`${APP_NAME}"
VIAddVersionKey "CompanyName" "`${APP_PUBLISHER}"
VIAddVersionKey "FileVersion" "$AppVersion"

Section "Install"
    SetOutPath "`$INSTDIR"
    File /r "dist\secan\*"
    
    # Create desktop shortcut
    CreateShortCut "`$DESKTOP\`${APP_NAME}.lnk" "`$INSTDIR\`${APP_EXE}"
    
    # Create start menu shortcut
    CreateDirectory "`$SMPROGRAMS\`${APP_NAME}"
    CreateShortCut "`$SMPROGRAMS\`${APP_NAME}\`${APP_NAME}.lnk" "`$INSTDIR\`${APP_EXE}"
    CreateShortCut "`$SMPROGRAMS\`${APP_NAME}\Uninstall.lnk" "`$INSTDIR\uninstaller.exe"
    
    # Create uninstaller
    WriteUninstaller "`$INSTDIR\uninstaller.exe"
    
    # Registry entries for Add/Remove Programs
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\`${APP_NAME}" "DisplayName" "`${APP_NAME}"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\`${APP_NAME}" "UninstallString" "`$INSTDIR\uninstaller.exe"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\`${APP_NAME}" "Publisher" "`${APP_PUBLISHER}"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\`${APP_NAME}" "DisplayVersion" "`${APP_VERSION}"
    WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\`${APP_NAME}" "NoModify" 1
    WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\`${APP_NAME}" "NoRepair" 1
SectionEnd

Section "Uninstall"
    Delete "`$INSTDIR\*.*"
    RMDir /r "`$INSTDIR"
    Delete "`$DESKTOP\`${APP_NAME}.lnk"
    RMDir /r "`$SMPROGRAMS\`${APP_NAME}"
    DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\`${APP_NAME}"
SectionEnd
"@

# Write NSIS script to file
$nsisScript | Out-File -FilePath "installer.nsi" -Encoding UTF8

# Build installer
Write-Host "Building installer..."
makensis installer.nsi

if ($LASTEXITCODE -eq 0) {
    Write-Host "Windows installer created successfully: secan-installer.exe"
} else {
    Write-Error "Failed to create Windows installer"
    exit 1
}