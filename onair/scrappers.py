import logging
import requests
from bs4 import BeautifulSoup

log = logging.getLogger('scrappers')


def i_ua(link):
    try:
        link = link.strip('/')
        resp = requests.get('https://radio.i.ua/{}/'.format(link))
        assert resp.status_code == 200, resp.status_code
        soup = BeautifulSoup(resp.content, 'html.parser')
        links = soup.find_all(href='/{}/archive/'.format(link), class_=None)
        assert len(links) == 1, links
        return links[0].text
    except:
        log.exception("Unexpected error while scapping i.ua {}:".format(link))


def hit_fm():
    return {'station': 'Хiт FM', 'onair': i_ua('hit.fm')}


def russkoe_radio_ukraina():
    return {'station': '"Русское Радио" Украина', 'onair': i_ua('russkoe.radio')}

def nrj():
    return {'station': 'NRJ', 'onair': i_ua('nrj')}

def kiss_fm():
    return {'station': 'Kiss FM', 'onair': i_ua('kiss.fm')}

def melodiya():
    return {'station': 'Мелодия FM', 'onair': i_ua('melodiya')}

def nashe_radio():
    return {'station': 'Наше Радио', 'onair': i_ua('nashe.radio')}

def uafm():
    return {'station': 'UAFM', 'onair': i_ua('uafm.km.ua')}

def keksfm():
    return {'station': 'KEXXX FM', 'onair': i_ua('keksfm')}

def radiopyatnica():
    return {'station': 'Радио ПЯТНИЦА', 'onair': i_ua('radiopyatnica')}
