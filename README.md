
# Downloader de VODs da Twitch

## Introdução
Este software permite que os usuários façam o download de VODs da Twitch de forma fácil e eficiente. O aplicativo suporta o download de múltiplos VODs, permitindo ao usuário selecionar a qualidade do vídeo e a opção de extrair o áudio em formato MP3, se desejado.

## Instalação
Para utilizar o downloader de VODs da Twitch, você precisa ter o Python e a biblioteca `yt-dlp` instalados. Os passos são os seguintes:

### Passo 1: Instalar o Python
Certifique-se de que o Python está instalado em seu sistema. Você pode baixá-lo [aqui](https://www.python.org/downloads/).

### Passo 2: Instalar `yt-dlp`
Abra um terminal e execute o seguinte comando para instalar a biblioteca `yt-dlp`:
```bash
pip install yt-dlp
```

## Uso
Para usar o software, siga os passos abaixo:

1. Execute o script no terminal:
   ```bash
   python downloader.py
   ```

2. Quando solicitado, insira a URL do VOD ou IDs separados por vírgula.

3. Selecione a qualidade do vídeo desejada (opções disponíveis: 1080p, 720p, 480p). Caso uma qualidade inválida seja inserida, a qualidade padrão será definida como `720p`.

4. Responda se deseja extrair o áudio em formato MP3 com 's' (sim) ou 'n' (não).

O aplicativo começará o download e informará quando cada operação for concluída.

## Referência de API
A função `download_vod` é responsável pelo download dos VODs. Abaixo estão as informações necessárias:

### Função: `download_vod(vod_urls, quality='720p', extract_audio=False)`
- **vod_urls**: Lista de URLs ou IDs dos VODs a serem baixados.
- **quality**: (opcional) Qualidade do vídeo que deve ser baixada. Aceita os valores '1080p', '720p', e '480p'. O padrão é '720p'.
- **extract_audio**: (opcional) Se `True`, o áudio será extraído em formato MP3 com qualidade de 192kbps.

### Tratamento de Erros
Caso ocorra um erro durante o download, uma mensagem de erro será exibida, indicando qual VOD falhou e o motivo.

## Contribuição
Se você deseja contribuir para o projeto, siga as seguintes etapas:

1. Faça um **fork** do repositório.
2. Crie uma nova branch para suas alterações (`git checkout -b feature/nome-da-sua-feature`).
3. Realize suas alterações e submeta um **pull request**.

## Licença
Este projeto está licenciado sob a Licença MIT. Consulte o arquivo `LICENSE` para mais detalhes.

#### docs/
1. **installation.md**  
   - Detalhes sobre o processo de instalação do Python e das dependências necessárias.  
2. **usage.md**  
   - Exemplos práticos sobre como usar o software.  
3. **api_reference.md**  
   - Descrições detalhadas das funções e seus parâmetros.  
4. **contribution_guide.md**  
   - Diretrizes para contribuir com o projeto.  
5. **license.md**  
   - Informações sobre a licença que se aplica ao projeto.