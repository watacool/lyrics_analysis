# coding: utf-8
# python 2.7
import os
import argparse
import pandas as pd
from morphological_analysis import morphological
from gensim.models import word2vec

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--init_load", default=False, action='store_true')
    parser.add_argument("--dataset", default="./data/dataset.csv", type=str)
    parser.add_argument("--wordlist", default="./data/word_list.txt", type=str)
    args = parser.parse_args()
    return args

def my_word2vec(args):
    '''
    # reference: https://qiita.com/makaishi2/items/63b7986f6da93dc55edd
    size: 圧縮次元数
    min_count: 出現頻度の低いものをカットする
    window: 前後の単語を拾う際の窓の広さを決める
    iter: 機械学習の繰り返し回数(デフォルト:5)十分学習できていないときにこの値を調整する
    '''

    # learning model
    print "# learning word2vec"
    read_word_list = word2vec.LineSentence(args.wordlist)
    model = word2vec.Word2Vec(read_word_list, size=200, min_count=5, window=5, iter=20)

    # output model
    model_dir = "./model"
    model_name = "my_model.model"
    print "# output {}...".format(os.path.join(model_dir, model_name))
    if not os.path.exists(model_dir):
        os.mkdir(model_dir)
    model.save(os.path.join(model_dir, model_name))

    testword = [u"君"]
    print "# testing {}".format(testword[0].encode('utf-8'))
    rets = model.wv.most_similar(positive=testword)
    for ret in rets:
        print "{}: {}".format(ret[0].encode('utf-8'), ret[1])
    return 0

def main():
    args = get_args()
    word_list = morphological(args)
    my_word2vec(args)

if __name__ == '__main__':
    main()
