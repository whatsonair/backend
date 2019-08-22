import logging
import requests
from bs4 import BeautifulSoup

log = logging.getLogger('scrappers')


def radio_i_ua(link):
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


def russkoe_radio_ukraina():
    return radio_i_ua('russkoe.radio')

def nrj_ukraina():
    return radio_i_ua('nrj')

def kiss_fm():
    return radio_i_ua('kiss.fm')

def kexxx_fm():
    return radio_i_ua('keksfm')

def fm_109():
    return radio_i_ua('109fmnet')

def big_radio():
    return radio_i_ua('bigradio.com.ua')

def metal_voice_radio():
    return radio_i_ua('metalvoice')

def mix_fm():
    return radio_i_ua('vtsu.dance')

def psy_radio():
    return radio_i_ua('psyradio')

def radio_ex():
    return radio_i_ua('radioex')

def rock_fm_ukraine():
    return radio_i_ua('prorock.online')

def trance_is_star():
    return radio_i_ua('tranceisstar')

def uafm():
    return radio_i_ua('uafm.km.ua')

def melodia_fm():
    return radio_i_ua('melodiya')

def nashe_radio():
    return radio_i_ua('nashe.radio')

def radio_vtsu():
    return radio_i_ua('vtsu.org.ua')

def radio_vecherniy_briz():
    return radio_i_ua('rpr.dp.ua')

def radio_pyatnitsa():
    return radio_i_ua('radiopyatnica')

def radio_z_kriyivki():
    return radio_i_ua('kriyivki')

def rock_radio_ua():
    return radio_i_ua('rockradio')

def hit_fm():
    return radio_i_ua('hit.fm')