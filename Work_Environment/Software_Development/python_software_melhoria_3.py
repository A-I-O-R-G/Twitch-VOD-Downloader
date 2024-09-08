import os
import yt_dlp

def download_vod(vod_urls, quality='720p', extract_audio=False):
    """Faz o download de VODs da Twitch com opções de qualidade e extração de áudio."""
    
    # Melhoria: Validando a qualidade de vídeo e definindo um valor padrão
    valid_qualities = ['1080p', '720p', '480p']
    if quality not in valid_qualities:
        print('Qualidade inválida, utilizando 720p como padrão.')
        quality = '720p'

    ydl_opts = {
        'format': f'bestvideo[height<={quality[:-1]}]+bestaudio/best',
        'outtmpl': '%(title)s.%(ext)s',  # Renomeação dos arquivos baixados
        'noplaylist': True,  # Garante que apenas um VOD seja baixado
        'retries': 5  # Número de tentativas em caso de falha
    }

    if extract_audio:
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]

    for vod_url in vod_urls:
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                print(f'Iniciando download de: {vod_url}')
                ydl.download([vod_url])
            print(f'Download concluído para: {vod_url}')
        except yt_dlp.utils.DownloadError as de:
            print(f'Erro ao baixar {vod_url}: {de}')
        except Exception as e:
            print(f'Erro inesperado ao baixar {vod_url}: {e}')

def main():
    print('Bem-vindo ao downloader de VODs da Twitch!')
    vod_input = input('Insira a URL do VOD ou IDs separados por vírgula:\n')
    vod_urls = [url.strip() for url in vod_input.split(',')]  # Suporta múltiplos VODs

    quality = input('Selecione a qualidade do vídeo (1080p, 720p, 480p):\n').strip()
    extract_audio = input('Deseja extrair o áudio em formato MP3? (s/n):\n').strip().lower() == 's'

    download_vod(vod_urls, quality, extract_audio)

if __name__ == '__main__':
    # Verifica o sistema operacional
    print(f'Executando em: {os.name} (compatível com Windows, Mac e Linux)')
    main()