from enum import Enum
from collections import Counter as counter
import numpy as np

class CONSTANTS(Enum):
    text_ommit = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '-', '+', '=', '[', ']', '{', '}', ';', ':', ',', '|', '/', '?', '<', '>', '.', '~', '`']


def most_common_word(words):
    words = filter_and_transform(words)
    comm = counter(words).most_common()
    return comm[0] if len(comm) > 1 else ('', 0)

def most_used(word):
    return most_common_word(word)[0]

def most_count(word):
    return most_common_word(word)[1]

def easy_read(b):
    return 'normal message' if int(b) == 0 else 'spam message'

def map_bool(label):
    return int(label) if len(label) ==1 else 1 if label == 'spam' else 0

def filter_and_transform(text):
    l = ''.join([c for c in text if c not in CONSTANTS.text_ommit.value])
    l = [w for w in l.split() if 4 < len(w) < 18]
    return l

def filter_to_text(text):
    return " ".join(filter_and_transform(text))

def filter_to_numerical_vals(df):
    cols = df.columns.values
    for col in cols:
        text_vals = {}
        def convert(val):
            return text_vals[val]

        if df[col].dtype != np.int64 and df[col].dtype != np.float64:
            cc = df[col].values.tolist()
            uvals = set(cc)
            i = 0
            for u in uvals:
                if u not in text_vals:
                    text_vals[u] = i
                    i+=1

            df[col] = list(map(convert, df[col]))
    return df