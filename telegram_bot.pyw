from telegram import KeyboardButton, ReplyKeyboardMarkup, Update 
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from mss import mss
import tempfile
import os
import psutil
import ctypes
import webbrowser
import pyperclip
import subprocess
import datetime

from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


class TelegramBot:
    def __init__(self):
        self.TOKEN = "HERE"
        self.CHAT_ID = "HERE"
        self.DESKTOP_PATH = r"HERE"

    async def comando_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        buttons = [
            [KeyboardButton("⚠ Screen status")],
            [KeyboardButton("🔒 Lock screen")],
            [KeyboardButton("📸 Take screenshot")],
            [KeyboardButton("✂ Paste clipboard")],
            [KeyboardButton("📄 Process list")],
            [KeyboardButton("🔊 Volume")],
            [KeyboardButton("💤 Shutdown")],
            [KeyboardButton("💡 Other commands")]
        ]
        await context.bot.send_message(
            chat_id=self.CHAT_ID,
            text="✅ Successfully authenticated. Welcome back !",
            reply_markup=ReplyKeyboardMarkup(buttons)
        )

    async def errore(self, update: object, context: ContextTypes.DEFAULT_TYPE):
        print(f"The update {update} caused error {context.error}")

    def fai_screenshot(self):
        TEMP_FOLDER = tempfile.gettempdir()
        os.chdir(TEMP_FOLDER)
        with mss() as sct:
            sct.shot(mon=-1)
        return os.path.join(TEMP_FOLDER, 'monitor-0.png')

    async def gestisci_messaggio(self, update: Update, context: ContextTypes.DEFAULT_TYPE, testo_input: str):
        user_message = testo_input.split()

        if testo_input == "other commands":
            return (
                "url <link>: open a link in browser\n"
                "kill <proc>: terminate process\n"
                "cmd <command>: execute shell command\n"
                "cd <dir>: change directory\n"
                "download <file>: download a file\n"
                "volume <0-100>: set volume"
            )

        if testo_input == 'screen status':
            for proc in psutil.process_iter():
                if proc.name() == "LogonUI.exe":
                    return 'Screen locked'
            return 'Screen unlocked'

        if testo_input == 'lock screen':
            try:
                ctypes.windll.user32.LockWorkStation()
                return "Screen locked successfully"
            except Exception:
                return "Error while locking screen"

        if testo_input == "take screenshot":
            photo_path = self.fai_screenshot()
            await context.bot.send_photo(chat_id=self.CHAT_ID, photo=open(photo_path, 'rb'))
            return None

        if testo_input == "paste clipboard":
            try:
                return pyperclip.paste()
            except Exception:
                return "Unable to read clipboard"

        if testo_input == "volume":
            try:
                devices = AudioUtilities.GetSpeakers()
                interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
                volume = cast(interface, POINTER(IAudioEndpointVolume))
                current_level = round(volume.GetMasterVolumeLevelScalar() * 100)
                return f"Current volume: {current_level}%\nUse 'volume <0-100>' to modify it"
            except Exception:
                return "Unable to get volume information"

        if user_message[0] == "volume" and len(user_message) > 1:
            try:
                new_volume = int(user_message[1])
                if 0 <= new_volume <= 100:
                    devices = AudioUtilities.GetSpeakers()
                    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
                    volume = cast(interface, POINTER(IAudioEndpointVolume))
                    volume.SetMasterVolumeLevelScalar(new_volume / 100, None)
                    return f"Volume set to {new_volume}%"
                else:
                    return "Volume must be between 0 and 100"
            except ValueError:
                return "Invalid format. Use 'volume <0-100>'"
            except Exception:
                return "Error while setting volume"

        if testo_input == "shutdown":
            try:
                os.system("shutdown /s /f /t 0")
                return "Windows will shut down"
            except Exception:
                return "Unable to shut down Windows"

        if testo_input == "process list":
            try:
                proc_list = []
                for proc in psutil.process_iter():
                    if proc.name() not in proc_list:
                        proc_list.append(proc.name())
                processes = "\n".join(proc_list)
                return processes
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                return "Error while listing processes"

        if user_message[0] == 'kill':
            proc_list = []
            for proc in psutil.process_iter():
                proc_list.append([proc.name(), str(proc.pid)])
            try:
                for p in proc_list:
                    if p[0].lower() == user_message[1].lower():
                        psutil.Process(int(p[1])).terminate()
                return 'Process terminated successfully'
            except Exception:
                return 'Error while terminating process'

        if user_message[0] == 'url':
            try:
                webbrowser.open(user_message[1])
                return 'Link opened successfully'
            except Exception:
                return 'Error while opening link'

        if user_message[0] == "cd":
            if len(user_message) > 1:
                try:
                    os.chdir(user_message[1])
                    return os.getcwd()
                except Exception:
                    return "Directory not found!"

        if user_message[0] == "download":
            if len(user_message) > 1:
                file_path = user_message[1]
                if os.path.exists(file_path):
                    try:
                        with open(file_path, 'rb') as document:
                            await context.bot.send_document(chat_id=self.CHAT_ID, document=document)
                        return None
                    except Exception:
                        return "Error while sending file!"
                else:
                    return "File does not exist!"

        if user_message[0] == "cmd":
            try:
                res = subprocess.Popen(
                    user_message[1:], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.DEVNULL
                )
                stdout = res.stdout.read().decode("utf-8", 'ignore').strip()
                stderr = res.stderr.read().decode("utf-8", 'ignore').strip()
                if stdout:
                    return stdout
                elif stderr:
                    return stderr
                else:
                    return ''
            except Exception as e:
                return f"Command execution failed: {str(e)}"

        return "Command not recognized."

    async def invia_risposta(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_message = update.message.text
        if update.message.chat.username != "YOUR_USERNAME":
            print("[!] " + str(update.message.chat.username) + " tried to use this bot")
            await context.bot.send_message(chat_id=self.CHAT_ID, text="Nothing to see here.")
            return

        user_message = user_message.encode('ascii', 'ignore').decode('ascii').strip(' ')
        if len(user_message) == 0:
            return
        user_message = user_message[0].lower() + user_message[1:]

        response = await self.gestisci_messaggio(update, context, user_message)
        if response:
            if len(response) > 4096:
                for i in range(0, len(response), 4096):
                    await context.bot.send_message(chat_id=self.CHAT_ID, text=response[i:i + 4096])
            else:
                await context.bot.send_message(chat_id=self.CHAT_ID, text=response)

    async def salva_foto(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.message.chat.username != "YOUR_USERNAME":
            return
        
        try:
            photo = update.message.photo[-1]
            file = await context.bot.get_file(photo.file_id)
            
            current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            file_name = f"photo_{current_time}.jpg"
            save_path = os.path.join(self.DESKTOP_PATH, file_name)
            
            print(f"[+] Saving photo to: {save_path}")
            
            await file.download_to_drive(save_path)
            
            await context.bot.send_message(
                chat_id=self.CHAT_ID, 
                text=f"✅ Photo saved to desktop: {file_name}"
            )
        except Exception as e:
            await context.bot.send_message(
                chat_id=self.CHAT_ID, 
                text=f"❌ Error while saving photo: {str(e)}"
            )
            
    async def salva_video(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.message.chat.username != "YOUR_USERNAME":
            return
        
        try:
            video = update.message.video
            file = await context.bot.get_file(video.file_id)
            
            current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            file_name = f"video_{current_time}.mp4"
            save_path = os.path.join(self.DESKTOP_PATH, file_name)
            
            print(f"[+] Saving video to: {save_path}")
            
            await file.download_to_drive(save_path)
            
            await context.bot.send_message(
                chat_id=self.CHAT_ID, 
                text=f"✅ Video saved to desktop: {file_name}"
            )
        except Exception as e:
            await context.bot.send_message(
                chat_id=self.CHAT_ID, 
                text=f"❌ Error while saving video: {str(e)}"
            )

    def avvia_bot(self):
        app = ApplicationBuilder().token(self.TOKEN).build()

        app.add_handler(CommandHandler("start", self.comando_start))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.invia_risposta))
        app.add_handler(MessageHandler(filters.PHOTO, self.salva_foto))
        app.add_handler(MessageHandler(filters.VIDEO, self.salva_video))
        app.add_error_handler(self.errore)

        print("[+] BOT started")
        app.run_polling()


if __name__ == "__main__":
    bot = TelegramBot()
    bot.avvia_bot()
