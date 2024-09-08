import os
import yt_dlp

def download_vod(vod_urls, quality='720p', extract_audio=False):
    """Faz o download de VODs da Twitch com opções de qualidade e extração de áudio."""

    # Validando a qualidade de vídeo e definindo um valor padrão
    valid_qualities = ['1080p', '720p', '480p']
    if quality not in valid_qualities:
        print('Qualidade inválida, utilizando 720p como padrão.')
        quality = '720p'

    # Configurações do yt-dlp
    ydl_opts = {
        'format': f'bestvideo[height<={quality[:-1]}]+bestaudio/best',
        'outtmpl': '%(title)s_%(id)s.%(ext)s',  # Renomeação dos arquivos baixados
        'noplaylist': True,  # Garante que apenas um VOD seja baixado
        'retries': 5,  # Número de tentativas em caso de falha
        'progress_hooks': [hook_progress],  # Adiciona um hook para progresso
        'postprocessors': [],  # Inicia como uma lista vazia
    }

    # Adiciona o pós-processador se for necessário extrair áudio
    if extract_audio:
        ydl_opts['postprocessors'].append({
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        })

    # Processa cada URL de VOD
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


def hook_progress(d):
    """Função para exibir o progresso do download."""
    if d['status'] == 'downloading':
        print(f'Baixando: {d["filename"]}, Progresso: {d["_percent_str"]}, ETA: {d["_eta_str"]} restantes')


def main():
    print('Bem-vindo ao downloader de VODs da Twitch!')
    vod_input = input('Insira a URL do VOD ou IDs separados por vírgula:\n')
    vod_urls = [url.strip() for url in vod_input.split(',')]  # Suporta múltiplos VODs

    # Escolha de qualidade com opção padrão
    quality = input('Selecione a qualidade do vídeo (1080p, 720p, 480p) [padrão: 720p]:\n').strip() or '720p'
    extract_audio_input = input('Deseja extrair o áudio em formato MP3? (s/n):\n').strip().lower()
    extract_audio = extract_audio_input in ('s', 'sim')

    # Chama a função principal para download
    download_vod(vod_urls, quality, extract_audio)


if __name__ == '__main__':
    # Verifica o sistema operacional
    print(f'Executando em: {os.name} (compatível com Windows, Mac e Linux)')
    main()