# coding: utf-8
# python 2.7
import os
import argparse
import pandas as pd
from download_lyrics import make_dataset
from janome.tokenizer import Tokenizer # $ pip install janome

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--init_load", default=False, action='store_true')
    parser.add_argument("--dataset", default="./data/dataset.csv", type=str)
    parser.add_argument("--wordlist", default="./data/word_list.txt", type=str)
    args = parser.parse_args()
    return args

def morphological_analysis_janome(text):
    t = Tokenizer()
    token = t.tokenize(text) # input unicode
    return token

def morphological(args=None):
    # make and load dataset
    print args.init_load
    if args.init_load:
        print "# make dataset..."
        make_dataset()
    print "# load dataset {}...".format(args.dataset)
    df = pd.read_csv(args.dataset, encoding='shift-jis')

    word_list = ""
    for index, row in df.iterrows():
        print "# [{}] {}".format(index+1, row.title.encode('utf-8'))
        mor_list = morphological_analysis_janome(row.lyrics)
        for mor in mor_list:
            '''
            reference
            http://ailaby.com/janome/
            '''
            type = mor.part_of_speech.split(',')[0].encode('utf-8')
            if type==u'名詞'.encode('utf-8') or type==u'動詞'.encode('utf-8'):
                word = mor.base_form.encode('utf-8')
                if word != u','.encode('utf-8'):
                    print "[{}]: {}".format(word, type)
                    word_list = word_list + " " + word
        word_list = word_list + "\n"
    with open(args.wordlist, mode="w") as f:
        f.write(word_list)
    return word_list


def main():
    args = get_args()
    word_list = morphological(args)
    print word_list

if __name__ == '__main__':
    main()
