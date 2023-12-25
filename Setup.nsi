Unicode true
SetCompress off

; Script başlığı ve dosya adı
Name "Game Control Setup"
OutFile "GameControlSetup.exe"

; Kurulum dosyalarının nereye yerleştirileceği
InstallDir "$PROGRAMFILES32\GameControl" ; Program Files (x86) klasörüne kurulum yapacak

; Kurulum bölümü
Section
    ; Dosyaların kopyalanması
    SetOutPath $INSTDIR
    File "Game Control.exe"
    File "Game Control.exe.manifest"
    File "game.ico"
    File "/_internal\*" ; Yeni eklenen dosyaları dahil et

    ; Kısayolun oluşturulması
    CreateShortCut "$DESKTOP\Game Control.lnk" "$INSTDIR\Game Control.exe"

    ; Başlangıç klasörüne kısayolun eklenmesi
    CreateShortCut "$SMPROGRAMS\Startup\Game Control.lnk" "$INSTDIR\Game Control.exe"

    ; Kaldırma işlemi için gerekli dosyayı oluştur
    WriteUninstaller "$INSTDIR\Uninstall.exe"

    ; Otomatik başlatma
    Call autorun
SectionEnd

Function autorun
    ; Otomatik başlatma girdisinin eklenmesi
    WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Run" "Game Control" '"$INSTDIR\Game Control.exe"'

    ; Uygulama simgesinin gösterilmesi için başlangıç klasörüne kısayolun eklenmesi
    CreateShortCut "$SMPROGRAMS\Startup\Game Control.lnk" "$INSTDIR\Game Control.exe"

    ; Uygulamanın başlatılması
    ExecShell "open" '"$INSTDIR\Game Control.exe"'
FunctionEnd

Section "Uninstall"
    ; Kayıt Defteri Girdilerinin Kaldırılması
    DeleteRegKey /ifempty HKCU "Software\Microsoft\Windows\CurrentVersion\Run"

    ; Uygulama çalışıyorsa kapat
    nsExec::ExecToStack 'tasklist /FI "IMAGENAME eq Game Control.exe" /NH'
    Pop $0
    StrCmp $0 "" endCheckRunningApp
    MessageBox MB_ICONEXCLAMATION|MB_OK "Application running. I need to close the app before continuing..."
    nsExec::Exec 'taskkill /F /IM "Game Control.exe"'
    endCheckRunningApp:

    ; Kurulum klasörünün silinmesi
    RMDir /r "$INSTDIR"

    ; Kısayolun kaldırılması
    Delete "$DESKTOP\Game Control.lnk"

    ; Başlangıç klasöründeki kısayolun kaldırılması
    Delete "$SMPROGRAMS\Startup\Game Control.lnk"

    ; Documents/Game Control klasörünün silinmesi
    Delete "$DOCUMENTS\Game Control\*.*"
    RMDir "$DOCUMENTS\Game Control"
SectionEnd
