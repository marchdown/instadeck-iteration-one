import re
from hashlib import sha1

def slugify(content):
    return sha1(content).hexdigest()[:6]

def emb(line):
    ''' return an html element with video or image or None '''
    youtube_url = youtube_url_validation(line) 
    vimeo_url = vimeo_url_validation(line)
    img_url = extract_img_url(line) #FIXME: return None
    if (youtube_url):
        return wrap_youtube_link(youtube_url)
    if (vimeo_url):
        return wrap_vimeo_link(vimeo_url)
    if (img_url):
        return wrap_img_link(img_url)
    return None



def youtube_url_validation(url):
    youtube_regex = (
        r'(https?://)?(www\.)?'
        '(youtube|youtu|youtube-nocookie)\.(com|be)/'
        '(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')

    youtube_regex_match = re.match(youtube_regex, url)
    if youtube_regex_match:
        return youtube_regex_match.group(6)

    return youtube_regex_match

def extract_img_url(url):
    img_regex = (
        r'([a-z\-_0-9\/\:\.]*\.(jpg|jpeg|png|gif)$)')
    
    img_regex_match = re.match(img_regex, url)
    if img_regex_match:
        return img_regex_match.group(1)
    
    return img_regex_match

def vimeo_url_validation(url):
    vimeo_regex = (
        r'(?:https?\:\/\/)?(?:www\.)?(?:vimeo\.com\/)([0-9]+)')

    vimeo_regex_match = re.match(vimeo_regex, url)
    if vimeo_regex_match:
        return vimeo_regex_match.group(1) 

    return vimeo_regex_match



def wrap_img_link(img_url):
    return '<img src="' + img_url + '"/>'

def wrap_youtube_link(youtube_url):
    return '<iframe width="420" height="315" src="https://www.youtube.com/embed/'+ youtube_url  +'" frameborder="0" allowfullscreen></iframe>'
    
def wrap_vimeo_link(vimeo_id):
    return '<iframe src="https://player.vimeo.com/video/'+ vimeo_id + '" width="500" height="281" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen></iframe>'
