import os
import json
import requests
import tkinter as tk
from tkinter import filedialog, messagebox
from urllib.parse import urlparse

class VODDownloader:
    def __init__(self):
        self.downloaded_files = self.load_downloaded_files()
        
    def load_downloaded_files(self):
        """Carrega os URLs já baixados de um arquivo."""
        if os.path.exists('downloaded_vods.json'):
            with open('downloaded_vods.json', 'r') as f:
                return json.load(f)
        return []

    def save_downloaded_file(self, url):
        """Salva um URL baixado em um arquivo para cache."""
        self.downloaded_files.append(url)
        with open('downloaded_vods.json', 'w') as f:
            json.dump(self.downloaded_files, f)

    def download_vod(self, url):
        """Baixa o VOD a partir da URL dada."""
        if url in self.downloaded_files:
            print(f"O VOD {url} já foi baixado.")
            return

        try:
            response = requests.get(url)
            response.raise_for_status()  # Levanta um erro HTTP se a resposta for um código de erro
            file_name = os.path.basename(urlparse(url).path)
            with open(file_name, 'wb') as f:
                f.write(response.content)
            self.save_downloaded_file(url)
            print(f"Download completo: {file_name}")
            self.notify_user(f"Download completo: {file_name}")
        except requests.exceptions.RequestException as e:
            print(f"Erro ao baixar {url}: {e}")
            messagebox.showerror("Erro", f"Erro ao baixar {url}: {e}")

    def download_multiple_vods(self, file_path):
        """Baixa múltiplos VODs a partir de um arquivo .txt."""
        with open(file_path, 'r') as f:
            urls = f.read().strip().split('\n')
            for url in urls:
                self.download_vod(url)

    def notify_user(self, message):
        """Notifica o usuário quando um download é concluído."""
        messagebox.showinfo("Notificação", message)

    def run_gui(self):
        """Inicializa a interface gráfica do usuário para interação."""
        root = tk.Tk()
        root.withdraw()  # Ocultar a janela principal

        url_or_file = filedialog.askopenfilename(title="Selecione um arquivo com URLs ou insira um URL")
        
        if url_or_file.endswith('.txt'):
            self.download_multiple_vods(url_or_file)
        else:
            self.download_vod(url_or_file)

if __name__ == "__main__":
    downloader = VODDownloader()
    downloader.run_gui()