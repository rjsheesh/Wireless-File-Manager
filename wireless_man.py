import sys
import os
import re
import subprocess
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                               QPushButton, QLabel, QInputDialog, QFileDialog, QTextEdit, QMessageBox)
from PySide6.QtCore import Qt, QThread, Signal

# --- ব্যাকগ্রাউন্ড টাস্ক চালানোর জন্য থ্রেড ক্লাস ---
class BackgroundWorker(QThread):
    log_signal = Signal(str)
    finished_signal = Signal()

    def __init__(self, cmd_list):
        super().__init__()
        self.cmd_list = cmd_list

    def run(self):
        creationflags = 0
        if sys.platform == "win32":
            creationflags = subprocess.CREATE_NO_WINDOW
        
        # Popen দিয়ে কমান্ড রান করানো যাতে রিয়েল-টাইম আউটপুট পাওয়া যায়
        process = subprocess.Popen(
            self.cmd_list, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.STDOUT, 
            text=True, 
            bufsize=1, 
            universal_newlines=True, 
            creationflags=creationflags
        )
        
        # রিয়েল-টাইম লাইন বাই লাইন লগ পড়া
        for line in process.stdout:
            if line.strip():
                self.log_signal.emit(line.strip())
        
        process.wait()
        self.finished_signal.emit()


class FabiTechManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("fabiTECH - Wireless Scrcpy & File Manager")
        self.resize(550, 500)
        self.ip_address = ""

        # তোর পিসির সঠিক পাথ
        self.adb_path = r"C:\Users\nuLL\Desktop\Capcut Project\CapCut\Videos\platform-tools"
        self.scrcpy_path = r"C:\Users\nuLL\Desktop\Capcut Project\CapCut\Videos\scrcpy-win64-v3.3.4"
        os.environ["PATH"] = f"{self.adb_path};{self.scrcpy_path};" + os.environ.get("PATH", "")

        # --- CSS / QSS DART THEME ---
        dark_stylesheet = """
        QMainWindow {
            background-color: #1e1e1e;
        }
        QLabel {
            color: #ffffff;
            font-family: 'Segoe UI', Arial, sans-serif;
            font-size: 16px;
        }
        QPushButton {
            background-color: #2d2d30;
            color: #00ffcc;
            border: 2px solid #00ffcc;
            border-radius: 8px;
            padding: 12px;
            font-size: 14px;
            font-weight: bold;
            font-family: 'Segoe UI', Arial, sans-serif;
        }
        QPushButton:hover {
            background-color: #00ffcc;
            color: #121212;
        }
        QPushButton:disabled {
            background-color: #333333;
            color: #777777;
            border: 2px solid #555555;
        }
        QTextEdit {
            background-color: #0d0d0d;
            color: #00ff00;
            font-family: Consolas, 'Courier New', monospace;
            font-size: 13px;
            border: 1px solid #444444;
            border-radius: 5px;
            padding: 10px;
        }
        """
        self.setStyleSheet(dark_stylesheet)

        # UI Setup
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        # Branding Title
        self.title_label = QLabel("⚡ fabiTECH Wireless Manager ⚡")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("font-size: 22px; font-weight: bold; color: #00ffcc; margin-bottom: 5px;")
        layout.addWidget(self.title_label)

        # Status Label
        self.status_label = QLabel("Status: 🔴 Disconnected")
        self.status_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #ff4c4c;")
        self.status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status_label)

        # Connect Button
        self.btn_connect = QPushButton("🔗 Connect Device via Wi-Fi")
        self.btn_connect.setStyleSheet("background-color: #ffaa00; color: #121212; border: none;")
        self.btn_connect.clicked.connect(self.connect_device)
        layout.addWidget(self.btn_connect)

        # Menu Buttons
        self.btn_scrcpy = QPushButton("📱 [1] Start Scrcpy (Screen Mirror)")
        self.btn_scrcpy.clicked.connect(self.start_scrcpy)
        self.btn_scrcpy.setEnabled(False)
        layout.addWidget(self.btn_scrcpy)

        self.btn_pull = QPushButton("⬇️ [2] Download Alight Motion Videos")
        self.btn_pull.clicked.connect(self.pull_videos)
        self.btn_pull.setEnabled(False)
        layout.addWidget(self.btn_pull)

        self.btn_push = QPushButton("⬆️ [3] Send File to Mobile (Download Folder)")
        self.btn_push.clicked.connect(self.push_file)
        self.btn_push.setEnabled(False)
        layout.addWidget(self.btn_push)

        self.btn_disconnect = QPushButton("❌ [4] Disconnect & Exit")
        self.btn_disconnect.setStyleSheet("color: #ff4c4c; border-color: #ff4c4c;")
        self.btn_disconnect.clicked.connect(self.disconnect_device)
        self.btn_disconnect.setEnabled(False)
        layout.addWidget(self.btn_disconnect)

        # Terminal / Log Box
        self.log_box = QTextEdit()
        self.log_box.setReadOnly(True)
        layout.addWidget(self.log_box)

        self.worker = None # Worker thread placeholder

        self.log("fabiTECH System Initialized...")
        self.log("Awaiting USB connection...")

    def log(self, text):
        self.log_box.append(text)
        # অটোমেটিক স্ক্রল করে নিচে নামানোর জন্য
        scrollbar = self.log_box.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    def run_cmd_sync(self, cmd_list):
        creationflags = 0
        if sys.platform == "win32":
            creationflags = subprocess.CREATE_NO_WINDOW
        result = subprocess.run(cmd_list, capture_output=True, text=True, creationflags=creationflags)
        return result

    def connect_device(self):
        self.log("\n[*] Searching for phone's Wi-Fi IP address...")
        
        result = self.run_cmd_sync(["adb", "shell", "ip", "addr", "show", "wlan0"])
        match = re.search(r'inet (\d+\.\d+\.\d+\.\d+)', result.stdout)
        
        if match:
            self.ip_address = match.group(1)
            self.log(f"[+] Auto-detected IP: {self.ip_address}")
        else:
            self.log("[!] Could not find IP automatically.")
            ip, ok = QInputDialog.getText(self, "Manual IP", "Please enter your phone's Wi-Fi IP:")
            if ok and ip:
                self.ip_address = ip
            else:
                self.log("[-] Connection cancelled.")
                return

        self.log("[+] Enabling TCP/IP port 5555...")
        self.run_cmd_sync(["adb", "tcpip", "5555"])

        self.log(f"[+] Connecting to {self.ip_address}...")
        self.run_cmd_sync(["adb", "connect", f"{self.ip_address}:5555"])
        
        self.log("[!] Connected successfully! Unplug the USB cable now.")
        
        self.status_label.setText(f"Status: 🟢 Connected ({self.ip_address})")
        self.status_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #00ffcc;")
        
        self.set_buttons_enabled(True)
        self.btn_connect.setEnabled(False)
        self.btn_connect.setStyleSheet("background-color: #333333; color: #777; border: none;")

    def set_buttons_enabled(self, state):
        self.btn_scrcpy.setEnabled(state)
        self.btn_pull.setEnabled(state)
        self.btn_push.setEnabled(state)
        self.btn_disconnect.setEnabled(state)

    def start_scrcpy(self):
        if self.ip_address:
            self.log("\n[+] Starting Scrcpy...")
            subprocess.Popen(["scrcpy", "-s", f"{self.ip_address}:5555"])

    def pull_videos(self):
        self.log("\n[+] Starting Download from Alight Motion...")
        
        # তোর .bat ফাইলের ঠিকানাই দিলাম
        dest = r"C:\Users\nuLL\Desktop\Capcut Project\CapCut\Videos\Downloads"
        os.makedirs(dest, exist_ok=True)
        
        cmd = ["adb", "-s", f"{self.ip_address}:5555", "pull", "/sdcard/Movies/Alight Motion", dest]
        
        # বাটন ডিসেবল করা যেন ডাবল ক্লিক না পড়ে
        self.set_buttons_enabled(False)
        
        # থ্রেড চালু করা
        self.worker = BackgroundWorker(cmd)
        self.worker.log_signal.connect(self.log)
        self.worker.finished_signal.connect(self.on_pull_finished)
        self.worker.start()

    def on_pull_finished(self):
        self.log('[+] Done! Check the "Videos\\Alight Motion" folder on your PC.')
        QMessageBox.information(self, "Success", "Videos downloaded successfully!")
        self.set_buttons_enabled(True)

    def push_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select a File to Send")
        if file_path:
            self.log(f"\n[+] Sending '{os.path.basename(file_path)}' to phone...")
            
            cmd = ["adb", "-s", f"{self.ip_address}:5555", "push", file_path, "/sdcard/Download/"]
            
            self.set_buttons_enabled(False)
            self.worker = BackgroundWorker(cmd)
            self.worker.log_signal.connect(self.log)
            self.worker.finished_signal.connect(self.on_push_finished)
            self.worker.start()

    def on_push_finished(self):
        self.log('[+] Done! Check the "Download" folder on your mobile.')
        QMessageBox.information(self, "Success", "File sent to phone successfully!")
        self.set_buttons_enabled(True)

    def disconnect_device(self):
        if self.ip_address:
            self.log("\n[+] Disconnecting Device...")
            self.run_cmd_sync(["adb", "disconnect", f"{self.ip_address}:5555"])
            self.log("[+] Goodbye!")
            sys.exit()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = FabiTechManager()
    window.show()
    sys.exit(app.exec())