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


def nrj():
    return {'station': '"Русское Радио" Украина', 'onair': i_ua('russkoe.radio')}


I_UA = [
    lambda: {'station': '"Русское Радио" Украина', 'onair': i_ua('russkoe.radio')},
    lambda: {'station': 'NRJ', 'onair': i_ua('nrj')},
    lambda: {'station': 'Kiss FM', 'onair': i_ua('kiss.fm')},
    lambda: {'station': 'KEXXX FM', 'onair': i_ua('keksfm')},
    lambda: {'station': '109FM', 'onair': i_ua('109fmnet')},
    lambda: {'station': 'BiG Radio', 'onair': i_ua('bigradio.com.ua')},
    lambda: {'station': 'Metal Voice Радио', 'onair': i_ua('metalvoice')},
    lambda: {'station': 'MiX FM', 'onair': i_ua('vtsu.dance')},
    lambda: {'station': 'PsyRadio', 'onair': i_ua('psyradio')},
    lambda: {'station': 'RadioEx', 'onair': i_ua('radioex')},
    lambda: {'station': 'Rock FM Ukraine', 'onair': i_ua('prorock.online')},
    lambda: {'station': 'TRANCE IS STAR', 'onair': i_ua('tranceisstar')},
    lambda: {'station': 'UAFM', 'onair': i_ua('uafm.km.ua')},
    lambda: {'station': 'Мелодия FM', 'onair': i_ua('melodiya')},
    lambda: {'station': 'Наше Радио', 'onair': i_ua('nashe.radio')},
    lambda: {'station': 'Радио VTSU', 'onair': i_ua('vtsu.org.ua')},
    lambda: {'station': 'Радио Вечерний Бриз', 'onair': i_ua('rpr.dp.ua')},
    lambda: {'station': 'Радио ПЯТНИЦА', 'onair': i_ua('radiopyatnica')},
    lambda: {'station': 'Радіо з криївки', 'onair': i_ua('kriyivki')},
    lambda: {'station': 'РокРадио UA', 'onair': i_ua('rockradio')},
    lambda: {'station': 'Хiт FM', 'onair': i_ua('hit.fm')},
]