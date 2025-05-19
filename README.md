# Windows Remote Control Telegram Bot

A powerful and feature-rich Telegram bot designed to remotely control and monitor Windows systems.

> **Note:** This code was derived from an old repository which I cannot recall the name of. I've updated it and added several new features to meet my specific needs.

---

## 🚀 Features

### 🖥️ System Control
- 📸 Screenshot capture and delivery  
- 🔒 Screen lock functionality  
- 💻 System shutdown command  
- 🧠 Process monitoring and management  

### 📁 File Operations
- 📥 File download capability  
- 📂 Directory navigation  
- 🖼️ Save photos and videos received through Telegram to desktop  

### 🧾 System Information
- 📄 Process listing  
- ⚠️ Screen lock status check  
- 📋 Clipboard content retrieval  

### 🔊 Audio Control
- 🔈 View current volume level  
- 🎚️ Adjust system volume remotely  

### 💻 Command Execution
- 🖥️ Execute shell commands remotely  
- 🌐 Open URLs in the default browser  

---

## 🧰 Requirements

- Python 3.6+
- `python-telegram-bot`
- `mss` (for screenshots)
- `psutil` (for process management)
- `pyperclip` (for clipboard operations)
- `pycaw` (for audio control)
- `comtypes` (dependency for pycaw)

---

## 📦 Installation

```
pip install python-telegram-bot mss psutil pyperclip pycaw comtypes 
```
## ⚙️ Setup

1. Replace `TOKEN` with your Telegram bot token (get it from [@BotFather](https://t.me/BotFather))  
2. Replace `CHAT_ID` with your Telegram chat ID  
3. Update `DESKTOP_PATH` to your system's desktop directory  
4. Replace `YOUR_USERNAME` with your Telegram username for authentication  
5. (Optional) To run the script automatically at startup:
    - Press `Win + R`, type `shell:startup`, and press Enter
    - Copy your Python script or a shortcut to it into the opened folder
    - The bot will now run every time your PC starts

---

## ▶️ Usage

1. Run the script:

```bash
python telegram_remote_control.py
```

2. Start a chat with your bot on Telegram  
3. Send `/start` to initialize the keyboard interface  
4. Use buttons or text commands to control your PC  

---

## 🔐 Security Notice

This bot grants powerful control over your PC. To ensure security:

- Use a unique, secure bot token  
- Share access only with trusted users  
- Monitor usage regularly  
- Consider extra authentication measures  

---

## 🧾 Available Commands

| Command              | Description                              |
|----------------------|------------------------------------------|
| ⚠ `Screen status`    | Check if the screen is locked or not     |
| 🔒 `Lock screen`     | Lock the PC screen                        |
| 📸 `Take screenshot` | Capture and send a screenshot             |
| ✂ `Clipboard`        | Get contents of the clipboard             |
| 📄 `Process list`    | List active processes                     |
| 🔊 `Volume`          | Show current volume level                 |
| 💤 `Shutdown`        | Shut down the PC                          |
| 💡 `More commands`   | Display additional commands               |

---

### 🔧 Additional Commands

- `url <link>` – Open a URL in the default browser  
- `kill <process>` – Kill a specific process  
- `cmd <command>` – Run a shell command  
- `cd <directory>` – Change working directory  
- `download <file>` – Download a file from the PC  
- `volume <0-100>` – Set system volume  

---

## 🖼️ Media Handling

The bot automatically saves any photo or video sent to it into the desktop folder.


---

## ⚠️ Disclaimer

This tool is intended for personal use only. Use it responsibly. The author is not responsible for any misuse.


