#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import feedparser
import re
import json
import os

YOUTUBE_CHANNEL = "UCmQwQ11GwCzs5qIv4klEX-Q"
FEED_URL = f"https://www.youtube.com/feeds/videos.xml?channel_id={YOUTUBE_CHANNEL}"

# Garante que a pasta js exista para o player funcionar
if not os.path.exists('js'):
    os.makedirs('js')

def update_all():
    print(f"🔍 Buscando vídeos do canal...")
    feed = feedparser.parse(FEED_URL)
    
    if not feed.entries:
        print("⚠️ Nenhum vídeo encontrado.")
        return

    # 1. Atualiza o arquivo de dados do Player (js/musicas_data.js)
    ids_lista = [e.yt_videoid for e in feed.entries]
    with open('js/musicas_data.js', 'w', encoding='utf-8') as f:
        f.write(f"const listaMusicasIds = {json.dumps(ids_lista)};")
    print(f"✅ Lista de IDs para o Player atualizada.")

    # 2. Atualiza os cards na página de músicas (musicas/index.html)
    try:
        with open('musicas/index.html', 'r', encoding='utf-8') as f:
            content = f.read()

        video_cards = ""
        for v in feed.entries:
            video_cards += f'''<div class="video-card">
<h3 class="video-title">{v.title}</h3>
<div class="video-wrapper">
<iframe src="https://www.youtube.com/embed/{v.yt_videoid}?rel=0&modestbranding=1" frameborder="0" allowfullscreen></iframe>
</div>
</div>\n'''

        pattern = r'(<div class="videos-grid">)(.*?)(</div>\s*</main>)'
        replacement = rf'\1\n{video_cards}\n\3'
        new_html = re.sub(pattern, replacement, content, flags=re.DOTALL)

        with open('musicas/index.html', 'w', encoding='utf-8') as f:
            f.write(new_html)
        print("✅ Cards da página de músicas atualizados.")
    except Exception as e:
        print(f"❌ Erro ao atualizar HTML de músicas: {e}")

if __name__ == "__main__":
    update_all()
