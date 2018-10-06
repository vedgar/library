# Adapted from http://inventwithpython.com/hacking (BSD Licensed)
import string, collections, pathlib

alphabet = string.ascii_letters

def readfile(name):
    path = pathlib.Path(__file__).parent / name
    return frozenset(path.read_text().casefold().splitlines())

common_words = readfile('English_common_words.txt')
words = readfile('English_words.txt') | common_words

def clean(message, hold=frozenset(alphabet + string.whitespace[:3])):
    return ''.join(symbol for symbol in message if symbol in hold)

def words_share(message):
    possible_words = clean(message.casefold()).split() or '_'
    return sum(word in words for word in possible_words) / len(possible_words)

def is_English(message, words=.2, letters=.85):
    message_letters_share = len(clean(message)) / len(message or '_')
    return words_share(message) >= words and message_letter_share >= letters

def sorted_freq(frequency):
    return ''.join(sorted(sorted(frequency), key=frequency.get, reverse=True))

frequency = collections.Counter(e=1270, t=906, a=817, o=751, i=697, n=675,
    s=633, h=609, r=599, d=425, l=403, c=278, u=276, m=241, w=236, f=223,
    g=202, y=197, p=193, b=129, v=98, k=77, j=15, x=15, q=10, z=7)

etaoin = sorted_freq(frequency)

def only_letters(message):
    return clean(message.casefold(), alphabet)

def letter_frequency(message):
    counter = collections.Counter(dict.fromkeys(alphabet, 0))
    counter.update(only_letters(message))
    return counter

def frequency_match(message, threshold=6):
    diagram = sorted_freq(letter_frequency(message))
    match_common = len(set(diagram[:threshold]) & set(etaoin[:threshold]))
    match_uncommon = len(set(diagram[-threshold:]) & set(etaoin[-threshold:]))
    return match_common + match_uncommon
