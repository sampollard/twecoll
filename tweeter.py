import random
import sys
import pandas as pd
eols = ['.', '?', ';']
digit = ['0','1','2','3','4','5','6','7','8','9','0']

triples = {}
if len(sys.argv) != 2:
    print("usage: tweeter.py <training_corpus>. \
    This should be a csv with least the column 'text'")
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
words = '\n'.join(tweets).split()

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
    twt = "{} {} {}".format(*l) + ('\n' if w[-1] in eols else '')
    while len(twt) < 140:
        w = random.choice(triples[l])
        twt = twt + " {0}".format(w) + ('\n' if w[-1] in eols else '')
        if len(twt) >= 40 and w[-1] in eols:
            break # That's a long enough tweet
        l = (l[1], l[2], w)
        if not l in triples:
            l = random.choice(triples.keys())
    print(twt)
    print

