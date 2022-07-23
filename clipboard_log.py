from datetime import datetime
from threading import Thread
from matplotlib import pyplot as plt
from wordcloud import WordCloud, STOPWORDS
import pyperclip as pyc

class ClipboardLog:

    def __init__(self):
        self.log_file_name = "clipboard.log"
        self.stop_words = ['this', 'your', 'that', 'video', 'videos', 'with',
                      'like', 'from', 'when', 'they', 'just', 'have', 'much',
                      'very', 'what', 'also', 'than', 'also', 'because', 'them',
                      'even', 'there', 'then', 'will', 'into', 'their', 'would',
                      'about', 'their', 'does', 'should', 'these', 'more',
                      'wordcloud', 'subscriber']
        self.display_thread = None
        self.wordcloud = None

    def generate_from_freq(self, word_tally):
        return WordCloud(stopwords=STOPWORDS, collocations=True, background_color='dimgray',
                         width=900, height=500, colormap='YlGnBu', max_words=400
                         ).generate_from_frequencies(word_tally)


    def display_wordcloud(self):
        plt.imshow(self.wordcloud, interpolation='bilInear')
        plt.axis('off')
        plt.show()


    def display_wordcloud_in_parallel(self):
        if self.display_thread:
            print("*** Joining old display thread")
            self.display_thread.join()
            print("*** Joined")
        self.display_thread = Thread(target=self.display_wordcloud)
        print("*** Starting display thread")
        self.display_thread.start()
        print("*** Started")


    def only_alpha_ascii_chars(self, word):
        for c in word:
            if c < 'A' or c > 'z' or ('Z' < c < 'a'):
                return False
        return True

    def tally_words_in_log(self):
        word_tally = {}
        with open(self.log_file_name, "r") as log_file:
            text = log_file.read()
            words = text.split()
            for word in words:
                word = word.lower()
                if self.only_alpha_ascii_chars(word) and len(word) > 4 and word not in self.stop_words:
                    if word in word_tally.keys():
                        word_tally[word] += 1
                    else:
                        word_tally[word] = 1
        return word_tally

    def make_word_cloud(self):
        word_tally = self.tally_words_in_log()
        if word_tally:
            self.wordcloud = self.generate_from_freq(word_tally)
            self.display_wordcloud()
        else:
            print('*** No words yet. Copy some stuff')

    def clipboard_listener(self):
        file_mode = "a"
        while file_mode:
            with open(self.log_file_name, file_mode) as log_file:
                i = 0
                while True:
                    pyc.waitForNewPaste()
                    text = pyc.paste()
                    entry = f'{i:8}) {datetime.now().isoformat()}  {text}\n'
                    print(entry, end="")
                    try:
                        log_file.write(entry)
                    except UnicodeEncodeError as e:
                        print(f"***  Entry not saved:  {e}")
                    log_file.flush()
                    i += 1
                    if text.lower() == "stop it please":
                        file_mode = None
                        break
                    elif text.lower() == "wordcloud":
                        self.make_word_cloud()
                    elif text.lower() == "reset it please":
                        file_mode = "w"
                        break

a = ClipboardLog()
a.clipboard_listener()
