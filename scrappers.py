import json
import logging
import os
import xml.etree.ElementTree as ET

import requests
from bs4 import BeautifulSoup
try:
    import redis
except ModuleNotFoundError:
    # no redis caching
    pass

log = logging.getLogger('scrappers')


def _radio_i_ua(link):
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


def _radio_club_ua(station, stream):

    try:
        station_streams = None
        redis_client = None
        if 'redis' in globals():
            redis_client = redis.Redis(
                host=os.environ.get('SCRAPPER_CACHE_REDIS_HOST', '127.0.0.1'),
                port=int(os.environ.get('SCRAPPER_CACHE_REDIS_PORT', 6379)),
                db=0,
                socket_connect_timeout=1,
                socket_timeout=1,
            )
            try:
                playlist_cache = redis_client.get('radioclub.ua/json/playlist.json')
                if playlist_cache:
                    station_streams = json.loads(playlist_cache)
            except Exception as exc:
                log.exception('Failed to use redis cache when scrapping {}:{}. Continue without cache.'.format(station, stream))
                redis_client = None

        if station_streams is None:
            headers = {
                'Accept': "*/*",
                'Accept-Encoding': "gzip, deflate, br",
                'Accept-Language': "en-US,en;q=0.5",
                'Connection': "keep-alive",
                'Origin': "https://loungefm.com.ua",
                'TE': "Trailers",
                'Cache-Control': "no-cache",
            }

            resp = requests.get("https://radioclub.ua/json/playlist.json", headers=headers)
            resp.raise_for_status()
            if redis_client is not None:
                try:
                    redis_client.set('radioclub.ua/json/playlist.json', resp.content, 30)
                except:
                    log.exception('Redis cache set attempt exception:')
                    pass

            station_streams = resp.json()

        playlist = None
        for station_stream in station_streams['list']:
            if station_stream['station'] == station \
                    and station_stream['stream'] == stream:
                playlist = station_stream['playlist']
                break
        if not playlist:
            raise Exception("No playlist for station: '{}', stream: '{}'".format(station, stream))
        current_song = playlist[0]
        return "{artist} - {song}".format(
            artist=current_song['artists'][0]['title'],
            song=current_song['track']['title']
        )
    except:
        log.exception("Unexpected error in radio club ua scrapper:")


def _maximum_radio(station):
    # TODO: use onAirDate to bypass commercials
    try:
        resp = requests.get('https://maximum.fm/get-active-data/4/0')
        resp.raise_for_status()
        stations = resp.json()['stations']
        playlist = None
        for radio_station in stations:
            if radio_station['name'] == station:
                playlist = radio_station['songs']
                break
        if not playlist:
            raise Exception("No playlist for station: '{}'".format(station))
        current_song = playlist[0]
        artists = " & ".join(artist['name'] for artist in current_song['artists'])
        song = current_song['name']
        return "{} - {}".format(artists, song)

    except:
        log.exception("Unexpected error in maximum scrapper:")

def russkoe_radio_ukraina():
    return _radio_i_ua('russkoe.radio')

def nrj_ukraina():
    result = _radio_club_ua('nrj', 'online')
    if result:
        return result
    else:
        return _radio_i_ua('nrj')

def kiss_fm():
    return _radio_i_ua('kiss.fm')

def kexxx_fm():
    return _radio_i_ua('keksfm')

def fm_109():
    return _radio_i_ua('109fmnet')

def big_radio():
    return _radio_i_ua('bigradio.com.ua')

def metal_voice_radio():
    return _radio_i_ua('metalvoice')

def mix_fm():
    return _radio_i_ua('vtsu.dance')

def psy_radio():
    return _radio_i_ua('psyradio')

def radio_ex():
    return _radio_i_ua('radioex')

def rock_fm_ukraine():
    return _radio_i_ua('prorock.online')

def trance_is_star():
    return _radio_i_ua('tranceisstar')

def uafm():
    return _radio_i_ua('uafm.km.ua')

def melodia_fm():
    return _radio_i_ua('melodiya')

def nashe_radio():
    result = _radio_club_ua('nashe', 'nashe')
    if result:
        return result
    else:
        return _radio_i_ua('nashe.radio')

def radio_vtsu():
    return _radio_i_ua('vtsu.org.ua')

def radio_vecherniy_briz():
    return _radio_i_ua('rpr.dp.ua')

def radio_pyatnitsa():
    result = _radio_club_ua('radiopyatnica', 'radiopyatnica')
    if result:
        return result
    else:
        return _radio_i_ua('radiopyatnica')

def radio_z_kriyivki():
    return _radio_i_ua('kriyivki')

def rock_radio_ua():
    return _radio_i_ua('rockradio')

def hit_fm():
    return _radio_i_ua('hit.fm')

def shanson():
    try:
        resp = requests.get('https://www.shanson.ua/Poisk-pesen')
        assert resp.status_code == 200, resp.status_code
        soup = BeautifulSoup(resp.content, 'html.parser')
        song = soup.find(class_='play-online-song').text
        singer = soup.find(class_='play-online-singer').text
        return "{} - {}".format(singer, song)
    except:
        log.exception("Unexpected error while scapping www.shanson.ua:")

def loungefm():
    return _radio_club_ua('loungefm', 'online')

def jamfm():
    return _radio_club_ua('jamfm', 'jamfm')

def avtoradio():
    return _radio_club_ua('avtoradio', 'avtoradio')

def loungefm_chillout():
    return _radio_club_ua('loungefm', 'chillout')

def radiorelax():
    try:
        resp = requests.get('https://www.radiorelax.ua/playlist/')
        resp.raise_for_status()
        soup = BeautifulSoup(resp.content, 'html.parser')
        current_song = soup.find(id='ss0')
        artist = current_song.find(class_='artist').text.strip()
        song = current_song.find(class_='song').text.strip()
        return "{} - {}".format(artist, song)
    except:
        log.exception("Unexpected error in radiorelax scrapper:")

def maximum_onair():
    return _maximum_radio('ONAIR')

def maximum_ukrainian():
    return _maximum_radio('Максимум Українське')

def maximum_hitiv():
    return _maximum_radio('Максимум Хітів')

def maximum_rock():
    return _maximum_radio('Максимум Рок')

def super_diskoteka_90s():
    return _maximum_radio('Супер дискотека 90-х')

def _aristocrats(link):
    resp = requests.get(link)
    resp.raise_for_status()
    playlist = ET.fromstring(resp.content)
    artist = playlist.find('artist').attrib['title']
    song = playlist.find('song').attrib['title']
    return "{artist} - {song}".format(artist=artist, song=song)

def aristocrats():
    return _aristocrats('https://aristocrats.fm/service/nowplaying-aristocrats8.xml')

def amusic():
    return _aristocrats('https://aristocrats.fm/service/nowplaying-amusic8.xml')

def ajazz():
    return _aristocrats('https://aristocrats.fm/service/nowplaying-ajazz8.xml')
