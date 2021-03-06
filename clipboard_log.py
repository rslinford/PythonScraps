import multiprocessing
from datetime import datetime
from logging import info, warning, error
from multiprocessing import freeze_support

import pyperclip as pyc
from matplotlib import pyplot as plt
from wordcloud import WordCloud, STOPWORDS


def replace_non_alpha_chars_with_spaces(text):
    text_list = []
    for c in text:
        if str(c).isalpha():
            text_list.append(c)
        else:
            text_list.append(' ')
    return "".join(text_list)


class ClipboardLog:
    def __init__(self):
        self.log_file_name = "clipboard.log"
        self.stop_words = ['this', 'your', 'that', 'video', 'videos', 'with',
                           'like', 'from', 'when', 'they', 'just', 'have', 'much',
                           'very', 'what', 'also', 'than', 'also', 'because', 'them',
                           'even', 'there', 'then', 'will', 'into', 'their', 'would',
                           'about', 'their', 'does', 'should', 'these', 'more',
                           'wordcloud', 'subscriber', 'which']
        self.display_process = None

    @staticmethod
    def generate_from_freq(word_tally):
        return WordCloud(stopwords=STOPWORDS, collocations=True, background_color='dimgray',
                         width=900, height=500, colormap='YlGnBu', max_words=400
                         ).generate_from_frequencies(word_tally)

    @staticmethod
    def display_wordcloud(wc):
        info('***  display_wordcloud Start')
        plt.imshow(wc, interpolation='bilInear')
        plt.axis('off')
        plt.show()
        info('***  display_wordcloud End')

    def display_wordcloud_in_parallel(self, wc):
        if self.display_process:
            warning("***  Joining old display process. Close the matplotlib window to continue.")
            self.display_process.join()
            info("***  Joined")
        self.display_process = multiprocessing.Process(target=self.display_wordcloud, args=(wc,))
        info("***  Starting display process")
        self.display_process.start()
        info("***  Started")

    def tally_words_in_log(self):
        word_tally = {}
        with open(self.log_file_name, "r", encoding="utf-8") as log_file:
            text = log_file.read()
            text = replace_non_alpha_chars_with_spaces(text)
            words = text.split()
            for word in words:
                if len(word) > 4 and word not in self.stop_words:
                    if word in word_tally.keys():
                        word_tally[word] += 1
                    else:
                        word_tally[word] = 1
        return word_tally

    def make_word_cloud(self):
        word_tally = self.tally_words_in_log()
        if word_tally:
            wc = self.generate_from_freq(word_tally)
            self.display_wordcloud_in_parallel(wc)
        else:
            print('*** No words yet. Copy some stuff.')

    def clipboard_listener(self):
        file_mode = "a"
        while file_mode:
            with open(self.log_file_name, file_mode, encoding="utf-8") as log_file:
                i = 0
                while True:
                    pyc.waitForNewPaste()
                    text = pyc.paste()
                    text = text.lower()
                    text = replace_non_alpha_chars_with_spaces(text)
                    entry = f'{i:8}) {datetime.now().isoformat()}  {text}\n'
                    print(entry, end="")
                    try:
                        log_file.write(entry)
                    except UnicodeEncodeError as e:
                        error(f"***  Entry not saved:  {e}")
                    log_file.flush()
                    i += 1
                    if text == "stop it please":
                        file_mode = None
                        break
                    elif text == "wordcloud":
                        self.make_word_cloud()
                    elif text == "reset it please":
                        print("***  Truncating log file")
                        file_mode = "w"
                        break
                    elif text.find('help') != -1:
                        print('help')
                        print('stop it please')
                        print('wordcloud')
                        print('reset it please')


if __name__ == '__main__':
    # Calling freeze_support prevents the hangup during
    # bootstrap phase of subprocess. It took hours and hours
    # to find this solution.
    freeze_support()
    a = ClipboardLog()
    a.clipboard_listener()
