import random
import sys
import pandas as pd
import HTMLParser
#from bs4 import BeautifulSoup
# Suppress warnings for reading URL in a tweet
#import warnings
#warnings.filterwarnings("ignore", category=UserWarning, module='bs4')
eols = [u'.', u'?', u';']
digit = [u'0',u'1',u'2',u'3',u'4',u'5',u'6',u'7',u'8',u'9',u'0']

triples = {}
if len(sys.argv) != 2:
    print("usage: tweeter.py <training_corpus>. \
        This should be a csv with at least the column 'text'")
    sys.exit(2)
fn = sys.argv[1]

df = None
try:
    df = pd.read_csv(fn)
except pd.errors.ParserError:
    df = pd.read_csv(fn, sep="|")
finally:
    if df is None:
        print("Unable to read " + fn)
        sys.exit(1)

if 'is_retweet' in df.columns:
    tweets = df['text'][df['is_retweet'] == False]
else:
    tweets = df['text']
h = HTMLParser.HTMLParser()
tweets = tweets.apply(lambda s: h.unescape(s.decode('utf-8')))

words = u'\n'.join(tweets).split()

# Generate a 4-gram model
for i in range(len(words)-3):
    try:
        triples[(words[i], words[i+1], words[i+2])].append(words[i+3])
    except KeyError: 
        triples[(words[i], words[i+1], words[i+2])] = [words[i+3]]
NG = len(triples)

# Make some tweets!
for _ in range(15):
    l = random.choice(triples.keys())
    w = random.choice(triples[l])
    twt = u"{} {} {}".format(*l) + (u'\n' if w[-1] in eols else '')
    while len(twt) < 140:
        w = random.choice(triples[l])
        twt = twt + u" {0}".format(w) + (u'\n' if w[-1] in eols else '')
        if len(twt) >= 40 and w[-1] in eols:
            break # That's a long enough tweet
        l = (l[1], l[2], w)
        if not l in triples:
            l = random.choice(triples.keys())
    print(twt)
    print

