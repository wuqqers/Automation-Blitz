import os
import subprocess
import time
import psutil
import pystray
from PIL import Image
from dotenv import load_dotenv
import threading
from pathlib import Path
import sys
processes = []  # Başlatılan süreçlerin PID'lerini saklamak için liste
is_running = False  # Süreçlerin çalışıp çalışmadığını kontrol etmek için değişken

def on_quit_clicked(icon):
    icon.stop()
    os._exit(0)  # sys.exit(0) olarak değiştirilebilir

def create_tray_icon():
    global icon
    app_directory = sys.argv[0]  # Uygulamanın çalıştığı yolu al
    icon_path = os.path.join(os.path.dirname(app_directory), "game.ico")
    image = Image.open(icon_path)

    menu = (pystray.MenuItem("Exit", on_quit_clicked),)

    icon = pystray.Icon("Game Control", image, "Game Control", menu)
    icon.run()

def start_process(path):
    process = subprocess.Popen(path, shell=True, creationflags=subprocess.DETACHED_PROCESS)
    processes.append(process.pid)

def main():
    global is_running
    global processes
    threading.Thread(target=create_tray_icon).start()
    # Kullanıcının OneDrive yolunu bulma
    onedrive_path = os.path.join(os.path.expanduser('~'), 'OneDrive')
    # Belgeler klasörünün yolu
    documents_path = os.path.join(onedrive_path, 'Documents')

    # Game Control klasörünü oluşturma
    game_control_path = Path(os.path.join(documents_path, "Game Control"))
    game_control_path.mkdir(parents=True, exist_ok=True)

    # .env dosyasının yolu
    env_file_path = game_control_path / '.env'

    # .env dosyasından yolları yükle
    load_dotenv(dotenv_path=env_file_path)

    lol_path = os.getenv("LOL_PATH")
    blitz_path = os.getenv("BLITZ_PATH")

    if not lol_path or not blitz_path:
        lol_path, blitz_path = get_paths(lol_path, blitz_path)

    is_running = True

    while is_running:
        if is_process_running(lol_path) and not is_process_running(blitz_path):
            start_process(blitz_path)
            print("Blitz uygulaması başlatıldı.")

        elif not is_process_running(lol_path) and is_process_running(blitz_path):
            stop_process(blitz_path)
            print("Blitz uygulaması durduruldu.")

        time.sleep(35)  # 40 saniyede bir kontrol et

def is_process_running(path):
    try:
        for process in psutil.process_iter(['pid', 'name']):
            if process.info['name'] == os.path.basename(path):
                return True
        return False
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
        return False

# stop_process fonksiyonunu aşağıdaki gibi güncelliyoruz
def stop_process(path):
    for proc in psutil.process_iter():
        try:
            if proc.name() == os.path.basename(path):
                proc.terminate()
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

def get_paths(lol_path, blitz_path):
    if not lol_path:
        lol_path = os.getenv("LOL_PATH")
        if not lol_path:
            lol_path = get_path("League of Legends launcher", "LOL_PATH")

    if not blitz_path:
        blitz_path = os.getenv("BLITZ_PATH")
        if not blitz_path:
            blitz_path = get_path("Blitz uygulaması", "BLITZ_PATH")

    return lol_path, blitz_path

def get_path(app_name, env_var):
    saved_path = os.getenv(env_var)
    if saved_path:
        return saved_path
    
    layout = [
        [sg.Text(f"Lütfen {app_name} uygulamasının path'ini seçin:")],
        [sg.InputText(key='-FILEPATH-'), sg.FileBrowse(), sg.OK()]
    ]
    window = sg.Window(f"{app_name} Path", layout, finalize=True)
    selected_path = None  # Seçilen yolun başlangıçta None olması

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        if event == 'OK':
            selected_path = values['-FILEPATH-']
            if selected_path:  # Dosya seçildiyse
                sg.popup(f"{app_name} dosyası seçildi: {selected_path}", title="Bilgi")
                break  # Dosya seçildiğinde döngüden çık
            else:
                sg.popup("Lütfen bir dosya seçin!", title="Uyarı")

    window.close()

    if selected_path:  # Eğer dosya seçildiyse, yolun .env dosyasına kaydedilmesi
        save_path_to_file(selected_path, env_var)

    return selected_path

def save_path_to_file(path, env_var):
    # Kullanıcının OneDrive yolunu bulma
    onedrive_path = os.path.join(os.path.expanduser('~'), 'OneDrive')

    # Belgeler klasörünün yolu
    documents_path = os.path.join(onedrive_path, 'Documents')

    # Game Control klasörünü oluşturma
    game_control_path = Path(os.path.join(documents_path, "Game Control"))
    game_control_path.mkdir(parents=True, exist_ok=True)

    # .env dosyasının yolu
    env_file_path = os.path.join(game_control_path, '.env')

    # Dosyaya yazma işlemi
    with open(env_file_path, "a") as file:
        file.write(f"{env_var}={path}\n")

if __name__ == "__main__":
    main()
