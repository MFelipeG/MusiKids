#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import isodate
import re
import json
import os

# CONFIGURAÇÕES CIRÚRGICAS
API_KEY = "AIzaSyBYM5TJkDtjp34HiRsXcRJ3ccJ8pBP7ff0"
CHANNEL_ID = "UCmQwQ11GwCzs5qIv4klEX-Q"

if not os.path.exists('js'):
    os.makedirs('js')

def get_valid_videos():
    print(f"🔍 Consultando YouTube API para filtrar os 50 vídeos mais recentes (> 60s)...")
    
    # 1. Busca os 50 vídeos mais recentes (Limite máximo da API por página)
    search_url = f"https://www.googleapis.com/youtube/v3/search?key={API_KEY}&channelId={CHANNEL_ID}&part=snippet,id&order=date&maxResults=50&type=video"
    r = requests.get(search_url).json()
    
    if 'items' not in r:
        print("❌ Erro na API ou nenhum vídeo encontrado.")
        return []

    video_ids = [item['id']['videoId'] for item in r['items']]
    
    # 2. Busca os detalhes de duração para filtrar os vídeos
    ids_str = ",".join(video_ids)
    details_url = f"https://www.googleapis.com/youtube/v3/videos?key={API_KEY}&id={ids_str}&part=contentDetails,snippet"
    details_r = requests.get(details_url).json()
    
    valid_videos = []
    for item in details_r['items']:
        duration_iso = item['contentDetails']['duration']
        # Converte o formato do YouTube para segundos
        seconds = isodate.parse_duration(duration_iso).total_seconds()
        
        # FILTRO: Apenas vídeos com 60 segundos ou mais
        if seconds >= 60:
            valid_videos.append({
                'id': item['id'],
                'title': item['snippet']['title']
            })
    
    return valid_videos

def update_all():
    videos = get_valid_videos()
    if not videos:
        print("⚠️ Nenhum vídeo válido encontrado com mais de 60s.")
        return

    # 1. Atualiza o arquivo de dados do Player (js/musicas_data.js)
    ids_lista = [v['id'] for v in videos]
    with open('js/musicas_data.js', 'w', encoding='utf-8') as f:
        f.write(f"const listaMusicasIds = {json.dumps(ids_lista)};")
    print(f"✅ Player atualizado com {len(ids_lista)} vídeos (excluindo shorts).")

    # 2. Atualiza os cards na página de músicas (musicas/index.html)
    try:
        if os.path.exists('musicas/index.html'):
            with open('musicas/index.html', 'r', encoding='utf-8') as f:
                content = f.read()

            video_cards = ""
            for v in videos:
                video_cards += f'''<div class="video-card">
<h3 class="video-title">{v['title']}</h3>
<div class="video-wrapper">
<iframe src="https://www.youtube.com/embed/{v['id']}?rel=0&modestbranding=1" frameborder="0" allowfullscreen></iframe>
</div>
</div>\n'''

            pattern = r'(<div class="videos-grid">)(.*?)(</div>\s*</main>)'
            replacement = rf'\1\n{video_cards}\n\3'
            new_html = re.sub(pattern, replacement, content, flags=re.DOTALL)

            with open('musicas/index.html', 'w', encoding='utf-8') as f:
                f.write(new_html)
            print("✅ Página de músicas atualizada com os novos cards.")
    except Exception as e:
        print(f"❌ Erro ao atualizar HTML: {e}")

if __name__ == "__main__":
    update_all()
    
