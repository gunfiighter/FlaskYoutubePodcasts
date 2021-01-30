import ast
import os
import youtube_dl

PATH = "static/podcasts/"
ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': PATH + '/%(id)s.%(ext)s',

}
dl = youtube_dl.YoutubeDL(ydl_opts)


def download(link):
    try:
        r = dl.extract_info(link)
    except youtube_dl.utils.DownloadError:
        return False
    with open(f"{PATH}{r['id']}", 'w', encoding='UTF-8', errors='replace') as f:
        f.write(str(r))
    return True


def get():
    audios = {}
    for i in os.walk(PATH):
        for filename in i[2]:
            if '.' in filename and not filename.endswith('.part'):
                try:
                    audios[f'{PATH}{filename}'] = ast.literal_eval(open(f'{PATH}{filename.split(".")[0]}', 'r', encoding='UTF-8').read())
                except FileNotFoundError:
                    pass
    return audios
