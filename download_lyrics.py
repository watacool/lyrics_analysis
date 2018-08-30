# coding: utf-8
# python 2.7
import os
import pandas as pd
import urllib2
from bs4 import BeautifulSoup


URL_LIST = ['https://www.uta-net.com/song/171764/', 'https://www.uta-net.com/song/180507/', 'https://www.uta-net.com/song/189921/',
            'https://www.uta-net.com/song/194130/', 'https://www.uta-net.com/song/207430/', 'https://www.uta-net.com/song/211946/',
            'https://www.uta-net.com/song/218121/', 'https://www.uta-net.com/song/230046/', 'https://www.uta-net.com/song/235924/',
            'https://www.uta-net.com/song/238932/', 'https://www.uta-net.com/song/245013/', 'https://www.uta-net.com/song/253268/',]
DATA_DIR = "./data"
IS_OUT_LYRICS = False

def load_html(url):
    html = urllib2.urlopen(url)
    return html

def parse_title_lyrics(html):
    soup = BeautifulSoup(html, "lxml")
    title = soup.find("h2", class_="prev_pad").text.encode('utf-8')
    lyrics = soup.find("div", id="kashi_area").text.encode('utf-8')
    return title, lyrics

def write_lyrics(title, lyrics):
    if not os.path.exists(DATA_DIR):
        os.mkdir(DATA_DIR)
    fn = os.path.join(DATA_DIR, title+'.txt')
    with open(fn, mode='w') as f:
        f.write(lyrics)
    return 0

def make_dataset():
    df = pd.DataFrame([])
    # download lyrics and make dataset
    for i, url in enumerate(URL_LIST):
        html = load_html(url)
        title, lyrics = parse_title_lyrics(html)
        print "# [{}] {} => {}".format(i+1, url, title)
        df = pd.concat([df, pd.Series([title, url, lyrics])], axis=1)
        if IS_OUT_LYRICS:
            write_lyrics(title, lyrics)

    # output dataset
    print "# output dataset..."
    df = df.T.reset_index(drop=True)
    df.columns = ['title', 'url', 'lyrics']
    df.to_csv(os.path.join(DATA_DIR, 'dataset.csv'), index=True, encoding='shift_jis')
    '''
    return df's encoding type
        title: utf-8
        html: utf-8
        lyrics: utf-8
    '''
    return df

def main():
    make_dataset()

if __name__ == '__main__':
    main()
