import os
import yt_dlp
import threading

def download_vod(vod_url, quality='720p', extract_audio=False, output_format='mp4'):
    """Faz o download de um VOD da Twitch com opções de qualidade, extração de áudio e formato de saída."""
    
    valid_qualities = ['1080p', '720p', '480p']
    if quality not in valid_qualities:
        print('Qualidade inválida, utilizando 720p como padrão.')
        quality = '720p'

    ydl_opts = {
        'format': f'bestvideo[height<={quality[:-1]}]+bestaudio/best',
        'outtmpl': f'%(title)s_%(id)s.{output_format}',  # Renomeação dos arquivos baixados
        'noplaylist': True,
        'retries': 5,
        'progress_hooks': [hook_progress],
        'postprocessors': [],
    }

    if extract_audio:
        ydl_opts['postprocessors'].append({
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        })

    filename = f"{vod_url.split('/')[-1]}.{output_format}"  # Nome do arquivo baseado na URL
    if os.path.exists(filename):
        print(f'Arquivo {filename} já existe, pulando download.')
        return

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f'Iniciando download de: {vod_url}')
            ydl.download([vod_url])
        print(f'Download concluído para: {vod_url}')
    except yt_dlp.utils.DownloadError as de:
        print(f'Erro ao baixar {vod_url}: {de}')
    except Exception as e:
        print(f'Erro inesperado ao baixar {vod_url}: {e}')


def hook_progress(d):
    """Função para exibir o progresso do download."""
    if d['status'] == 'downloading':
        print(f'Baixando: {d["filename"]}, Progresso: {d["_percent_str"]}, ETA: {d["_eta_str"]} restantes')


def main():
    print('Bem-vindo ao downloader de VODs da Twitch!')
    vod_input = input('Insira a URL do VOD ou IDs separados por vírgula:
')
    vod_urls = [url.strip() for url in vod_input.split(',')]

    quality = input('Selecione a qualidade do vídeo (1080p, 720p, 480p) [padrão: 720p]:
').strip() or '720p'

    extract_audio_input = input('Deseja extrair o áudio em formato MP3? (s/n):
').strip().lower()
    extract_audio = extract_audio_input in ('s', 'sim')

    output_format = input('Selecione o formato do vídeo (mp4, mkv) [padrão: mp4]:
').strip() or 'mp4'

    # Criação de threads para múltiplos downloads
    threads = []
    for vod_url in vod_urls:
        thread = threading.Thread(target=download_vod, args=(vod_url, quality, extract_audio, output_format))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()  # Aguarda a conclusão de todos os downloads

if __name__ == '__main__':
    print(f'Executando em: {os.name} (compatível com Windows, Mac e Linux)')
    main()