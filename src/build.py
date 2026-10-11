import json, pathlib
from PIL import Image, ImageDraw
root = pathlib.Path(__file__).resolve().parent.parent
src = (root/'src/app.html').read_text()
dist = root/'dist' if (root/'dist').exists() else root; dist.mkdir(exist_ok=True)
head = '''<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" content="#eef1f6">
<meta name="description" content="Temporizador de ayuno intermitente con estadísticas.">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="Ayuno">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<link rel="manifest" href="manifest.webmanifest">
<link rel="icon" href="icon-192.png" type="image/png">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<style>:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}body{margin:0}[hidden]{display:none!important}img{max-width:100%}</style>
'''
title_end = src.index('</title>') + len('</title>')
style_end = src.index('</style>') + len('</style>')
html = head + src[:style_end] + '\n</head>\n<body>\n' + src[style_end:] + '\n</body>\n</html>\n'
(dist/'index.html').write_text(html)
manifest = {"name":"Reloj de Ayuno","short_name":"Ayuno","description":"Temporizador de ayuno intermitente con estadísticas","lang":"es","start_url":"./","scope":"./","display":"standalone","orientation":"portrait","background_color":"#eef1f6","theme_color":"#3346c9",
 "icons":[{"src":"icon-192.png","sizes":"192x192","type":"image/png"},{"src":"icon-512.png","sizes":"512x512","type":"image/png"},{"src":"icon-maskable-512.png","sizes":"512x512","type":"image/png","purpose":"maskable"}]}
(dist/'manifest.webmanifest').write_text(json.dumps(manifest, ensure_ascii=False, indent=1))
def icon(size, maskable=False, bg=(20,27,45)):
    S=size*4; im=Image.new('RGBA',(S,S),(0,0,0,0)); d=ImageDraw.Draw(im)
    if maskable: d.rectangle([0,0,S,S],fill=bg)
    else: d.rounded_rectangle([0,0,S,S],radius=int(S*.22),fill=bg)
    sc = .62 if maskable else .74
    r=S*sc/2; c=S/2; w=int(S*(.085 if maskable else .1))
    box=[c-r,c-r,c+r,c+r]
    d.ellipse(box,outline=(52,62,100),width=w)
    d.arc(box,start=-90,end=150,fill=(141,155,255),width=w)
    rr=S*.07; d.ellipse([c-rr,c-rr,c+rr,c+rr],fill=(242,166,80))
    return im.resize((size,size),Image.LANCZOS)
icon(192).save(dist/'icon-192.png'); icon(512).save(dist/'icon-512.png')
icon(512,True).save(dist/'icon-maskable-512.png')
icon(180,True).convert('RGB').save(dist/'apple-touch-icon.png')
print('built', len(html))
