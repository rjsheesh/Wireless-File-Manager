# ⚡ fabiTECH Wireless Manager ⚡

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python)
![PySide6](https://img.shields.io/badge/PySide6-GUI-green?style=for-the-badge&logo=qt)
![License](https://img.shields.io/badge/License-Free-orange?style=for-the-badge)

A sleek, modern, and powerful desktop application built with Python (PySide6) to wirelessly manage your Android device. Connect your phone via Wi-Fi, mirror your screen, and transfer files seamlessly without the hassle of cables!

## ✨ Key Features

* **🔗 Wireless ADB Connection:** Automatically detects your phone's Wi-Fi IP and connects wirelessly. Manual IP entry is also supported.
* **📱 One-Click Screen Mirroring:** Instantly start `scrcpy` to mirror and control your Android screen on your PC.
* **⬇️ Smart Video Downloader:** One-click download for your edited videos (e.g., Alight Motion) directly to your PC.
* **⬆️ Drag & Drop File Transfer:** Select or drag-and-drop any file from your PC to instantly send it to your phone's `Download` folder.
* **🚀 Background Processing:** Uses `QThread` for heavy tasks (like file transfer) so the UI never freezes or shows "Not Responding".
* **💻 Live Terminal Log:** A built-in dark-themed terminal viewer to see real-time progress and ADB logs.
* **🎨 Premium Dark Mode UI:** Beautiful custom QSS styling with hover effects, rounded corners, and a hacker-style aesthetic.

---

## 🛠️ Prerequisites

Before running the application, make sure you have the following installed:

1.  **Python 3.x** installed on your PC.
2.  **PySide6** library. Install it via pip:
    ```bash
    pip install PySide6
    ```
3.  **ADB (Android Debug Bridge)** & **Scrcpy**: Must be downloaded and extracted on your PC.
4.  **Developer Options & USB Debugging** must be ENABLED on your Android phone.

---

## 🚀 How to Use

### Step 1: Configuration
Open the `main.py` file in a text editor and update the folder paths for ADB and Scrcpy according to your PC:
```python
self.adb_path = r"C:\Your\Path\To\platform-tools"
self.scrcpy_path = r"C:\Your\Path\To\scrcpy-win64"

### 🔌 Step 2: Initial Connection

1. Connect your Android phone to your PC using a **USB Cable** *(Required only for the first setup to enable TCP/IP)*.
2. Run the application by opening your terminal/CMD and typing:
   ```bash
   python main.py

## Step 3: Go Wireless!

**Click on the "🔗 Connect Device via Wi-Fi" button**

**Accept any ADB authorization prompts** on your phone screen

**Once the status turns 🟢 Connected**, you can safely unplug the USB cable

**Use the menu buttons to:**
- Mirror Screen
- Pull Videos
- Push Files

## 👨‍💻 Developed By

**fabiTECH**  
*Crafted for seamless productivity and wireless freedom.*
