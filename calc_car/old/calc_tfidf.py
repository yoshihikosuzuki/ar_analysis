#!/usr/bin/env python3
#coding: utf-8

from collections import defaultdict, Counter
from multiprocessing import Pool
from scipy import stats
import numpy as np
from math import log

car_th = 0.
max_count = 100000   # very sensitive for input data
min_count = 100   # very sensitive for input data


def sub_df_s(w):   # number of emergence of word w in the set of all PR, s
    count = 0
    for mor in s:
        if w in mor:
            count += 1
    return (w, count)


def sub_df_s1(w):   # w in the partial set of all PR, s1
    count = 0
    for mor in s1:
        if w in mor:
            count += 1
    return (w, count)


if __name__ == "__main__":
    
    pr_mor_fname = "pr_mor"
    car_fname = "car.new.rsquare"

    car_all = defaultdict(list)   # {article_id : [car] (for all companies)} for all PR
    with open(car_fname, 'r') as f:
        for line in f:
            articleid, prtype, code, val, rs = line.strip().split('\t')
            if prtype == "01: Product":
                car_all[articleid].append(float(val) * 100.)

    car = {}   # {article_id : average car among companies}
    for articleid, val_list in car_all.items():
        car[articleid] = sum(val_list) / len(val_list)

    car_th = stats.scoreatpercentile(np.array([x[1] for x in car.items()]), 75)
    #print(car_th)
    #exit()
    
    pr_mor = {}   # {article_id : bodysub_mor list}
    with open(pr_mor_fname, 'r') as f:
        for line in f:
            articleid, mor = line.strip().split('\t')
            if articleid in car:
                pr_mor[articleid] = mor.split(' ')

    s = [set(m) for a, m in pr_mor.items()]   # set of words in all PR
    n_s = len(s)   # number of all words
    s1 = [set(m) for a, m in pr_mor.items() if car[a] >= car_th]   # set of words in significant PR
    n_s1 = len(s1)   # number of all words in significant PR

    word_count = Counter()   # frequency of each word
    for articleid, mor in pr_mor.items():
        for m in mor:
            word_count[m] += 1

    #print(word_count)    

    word_set = set()   # filtered set of all words
    for w, c in word_count.items():
        if min_count <= c and c <= max_count:
            word_set.add(w)

    #print(word_set)

    exe_pool = Pool(24)

    df_s = Counter()
    for ret in exe_pool.imap(sub_df_s, word_set):   # for each word, calculate the number of emergence of the word in s, the set of all PR mor lists
        df_s[ret[0]] = ret[1]
    #with open("df_s", 'w') as f:
    #    for w, c in df_s.items():
    #        f.write(str(w) + '\t' + str(c) + '\n')

    df_s1 = Counter()
    for ret in exe_pool.imap(sub_df_s1, word_set):
        df_s1[ret[0]] = ret[1]
    #with open("df_s1", 'w') as f:
    #    for w, c in df_s1.items():
    #        f.write(str(w) + '\t' + str(c) + '\n')
    
    tfidf = {}
    for w in word_set:
        tfidf[w] = float(df_s1[w]) / n_s1 * log(float(n_s) / df_s[w], 2)   # calc tf-idf

    print(str(n_s) + "\t" + str(n_s1))
    for data in sorted(tfidf.items(), key=lambda x: x[1], reverse = True):
        print('\t'.join([data[0], str(data[1]), str(df_s[data[0]]), str(df_s1[data[0]])]))   # TODO: statistical test
        #print(str(data[0]), data[1])
