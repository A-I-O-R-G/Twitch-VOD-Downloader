import os
import json
import requests
import tkinter as tk
from tkinter import filedialog, messagebox, StringVar, ttk
from urllib.parse import urlparse
from threading import Thread
import logging
import sys

# Configuração de logging
logging.basicConfig(filename='vod_downloader.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class VODDownloader:
    def __init__(self):
        self.downloaded_files = self.load_downloaded_files()
        self.is_downloading = False
        self.progress_bar_value = 0

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

    def download_vod(self, url, output_format):
        """Baixa o VOD a partir da URL dada."""
        if url in self.downloaded_files:
            logging.info(f"O VOD {url} já foi baixado.")
            return

        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            file_name = os.path.join(self.output_directory, f"{os.path.basename(urlparse(url).path)}.{output_format}")
            total_size = int(response.headers.get('content-length', 0))
            with open(file_name, 'wb') as f:
                for data in response.iter_content(chunk_size=1024):
                    f.write(data)
                    self.progress_bar_value += len(data)
                    self.update_progress_bar(total_size)
            self.save_downloaded_file(url)
            logging.info(f"Download completo: {file_name}")
            self.notify_user(f"Download completo: {file_name}")
        except requests.exceptions.RequestException as e:
            logging.error(f"Erro ao baixar {url}: {e}")
            messagebox.showerror("Erro", f"Erro ao baixar {url}: {e}")

    def update_progress_bar(self, total_size):
        """Atualiza a barra de progresso."""
        if self.progress_bar_value >= total_size:
            self.progress_bar['value'] = 100
            self.progress_bar_value = 0
            self.is_downloading = False
        else:
            percentage = (self.progress_bar_value / total_size) * 100
            self.progress_bar['value'] = percentage

    def download_multiple_vods(self, file_path, output_format):
        """Baixa múltiplos VODs a partir de um arquivo .txt."""
        with open(file_path, 'r') as f:
            urls = f.read().strip().split('\n')
            self.is_downloading = True
            for url in urls:
                if not self.is_downloading:  # Verifica se o usuário cancelou
                    logging.info("Download cancelado pelo usuário.")
                    break
                self.download_vod(url, output_format)

    def notify_user(self, message):
        """Notifica o usuário quando um download é concluído."""
        messagebox.showinfo("Notificação", message)

    def cancel_download(self):
        """Cancela o download em andamento."""
        self.is_downloading = False

    def select_output_directory(self):
        """Permite ao usuário escolher o diretório de saída."""
        self.output_directory = filedialog.askdirectory()
        if self.output_directory:
            messagebox.showinfo("Diretório de Saída", f"Diretório selecionado: {self.output_directory}")

    def run_gui(self):
        """Inicializa a interface gráfica do usuário para interação."""
        root = tk.Tk()
        root.title("VOD Downloader")

        # Seção do diretório de saída
        output_button = tk.Button(root, text="Selecionar Diretório de Saída", command=self.select_output_directory)
        output_button.pack(pady=5)

        # Seção de URL e formato
        self.url_var = StringVar()
        tk.Entry(root, textvariable=self.url_var, width=50).pack(pady=5)
        self.output_format_var = StringVar(value='mp4')
        tk.OptionMenu(root, self.output_format_var, 'mp4', 'mkv').pack(pady=5)

        # Botões de download e cancelamento
        download_button = tk.Button(root, text="Baixar VOD", command=lambda: Thread(target=self.start_download).start())
        download_button.pack(pady=5)

        cancel_button = tk.Button(root, text="Cancelar Download", command=self.cancel_download)
        cancel_button.pack(pady=5)

        # Barra de progresso
        self.progress_bar = ttk.Progressbar(root, length=200, mode='determinate')
        self.progress_bar.pack(pady=5)

        root.mainloop()

    def start_download(self):
        """Inicia o download em uma nova thread para evitar travamento da interface."""
        url = self.url_var.get()
        output_format = self.output_format_var.get()
        self.download_vod(url, output_format)

if __name__ == "__main__":
    downloader = VODDownloader()
    downloader.run_gui()