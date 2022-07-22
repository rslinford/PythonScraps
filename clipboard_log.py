from datetime import datetime

from matplotlib import pyplot as plt
from wordcloud import WordCloud, STOPWORDS
import pyperclip as pyc


log_file_name = "clipboard.log"

def generate_from_freq(word_tally):
    return WordCloud(stopwords=STOPWORDS, collocations=True, background_color='dimgray',
                     width=900, height=500, colormap='YlGnBu', max_words=400
                     ).generate_from_frequencies(word_tally)


def display_wordcloud(wc):
    plt.imshow(wc, interpolation='bilInear')
    plt.axis('off')
    plt.show()


def only_alpha_ascii_chars(word):
    for c in word:
        if c < 'A' or c > 'z' or ('Z' < c < 'a'):
            return False
    return True

def tally_words_in_log():
    word_tally = {}
    with open(log_file_name, "r") as log_file:
        text = log_file.read()
        words = text.split()
        for word in words:
            if only_alpha_ascii_chars(word) and len(word) > 3:
                if word in word_tally.keys():
                    word_tally[word] += 1
                else:
                    word_tally[word] = 1
    return word_tally

def make_word_cloud():
    word_tally = tally_words_in_log()
    wc = generate_from_freq(word_tally)
    display_wordcloud(wc)


with open(log_file_name, "a") as log_file:
    i = 0
    while True:
        pyc.waitForNewPaste()
        text = pyc.paste()
        entry = f'{i:8}) {datetime.now().isoformat()}  {text}\n'
        print(entry, end="")
        try:
            log_file.write(entry)
        except UnicodeEncodeError as e:
            print(f"   Entry not saved:  {e}")
        log_file.flush()
        i += 1
        if text.lower() == "stop it please":
            break
        elif text.lower() == "wordcloud":
            make_word_cloud()