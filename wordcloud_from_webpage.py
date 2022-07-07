import json
import os
import uuid

import imageio as imageio
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
import requests
from bs4 import BeautifulSoup

stop_words = ['about', 'after', 'associated', 'content', 'continue', 'could', 'esquire', 'every',
              'first', 'friday', 'greatest', 'guardian', 'hours', 'iconic', 'issue', 'might', 'minutes',
              'model', 'monday', 'movie', 'movies', 'news', 'newsmax', 'people', 'photographs', 'picture',
              'reading', 'really', 'saturday', 'scenes', 'story', 'sunday', 'their', 'three',
              'thursday', 'times', 'tuesday', 'vanity', 'wednesday', 'which', 'would',
              "year's", 'years']

def filter_words(words):
    filtered_dict = dict()
    for w in words.keys():
        if len(w) < 5:
            continue
        if w.lower() in stop_words:
            continue
        # Skip words with &lrm; entity which shows up as a box character in wordcloud
        if '\u200E' in w:
            continue
        w2 = w.strip('0123456789.,\'=_:[]{}-?!/')
        if w2 != w:
            filtered_dict[w2] = words[w]
        else:
            filtered_dict[w] = words[w]
    return filtered_dict


# Parsing customized, article extracted from its JSON wrapper
def get_the_vanity_words_custom_parsing(article_address):
    r = requests.get(article_address)
    soup = BeautifulSoup(r.text, features="lxml")
    word_dict = dict()
    for x in soup.find_all(type="application/ld+json"):
        j = json.loads(x.text)
        key = 'articleBody'
        if key in j.keys():
            value = j[key]
            words = value.split(" ")
            for w in words:
                if len(w) < 5:
                    continue
                if w.lower() in stop_words:
                    continue
                w = w.strip('0123456789.,\'*+\n')
                if '\n' in w or '_' in w or '=' in w or '’' in w:
                    continue
                if w in word_dict.keys():
                    word_dict[w] += 1
                else:
                    word_dict[w] = 1
    return word_dict


def only_alpha_ascii_chars(word):
    for c in word:
        if c < 'A' or c > 'z' or ('Z' < c < 'a'):
            return False
    return True


# Parsing not customized, reads entire page
def get_words_general_parsing(article_address):
    print(f'Requesting: {article_address}')
    r = requests.get(article_address)
    soup = BeautifulSoup(r.text, features="lxml")
    word_dict = dict()
    words = soup.text.split(" ")
    for w in words:
        w = w.strip('0123456789.,\'*+\n')
        if len(w) < 5:
            continue
        if w.lower() in stop_words:
            continue
        if not only_alpha_ascii_chars(w):
            continue
        if w in word_dict.keys():
            word_dict[w] += 1
        else:
            word_dict[w] = 1
    return word_dict


# Words from the times
def get_the_news_words():
    base_url = 'http://www.nytimes.com'
    r = requests.get(base_url)
    soup = BeautifulSoup(r.text, features="lxml")

    summary_list = []
    for summary in soup.find_all(class_="summary-class"):
        summary_list.append(summary.text)
    words = dict()
    print("All summaries:")
    for summary in summary_list:
        summary = summary.split(' ')
        for w in summary:
            if w in words.keys():
                words[w] += 1
            else:
                words[w] = 1
    return filter_words(words)


def display_wordcloud(web_page):
    word_counts = filter_words(get_words_general_parsing(web_page))
    print(word_counts)
    wc = WordCloud(stopwords=STOPWORDS, collocations=True).generate_from_frequencies(word_counts)
    plt.imshow(wc, interpolation='bilInear')
    plt.axis('off')
    plt.show()


def save_wordcloud(web_page, file_name, title):
    word_counts = filter_words(get_words_general_parsing(web_page))
    wc = WordCloud(stopwords=STOPWORDS, collocations=True).generate_from_frequencies(word_counts)
    plt.imshow(wc, interpolation='bilInear')
    plt.axis("off")
    plt.title(title)
    print(f'Saving wordcloud from {web_page} to file: {file_name}')
    plt.savefig(file_name)


def generate_unique_filename(prefix):
    uid = uuid.uuid4().hex
    return f'{prefix}_{uid}.png'


def make_gif(dir_name, gif_file_name):
    # dir of dir_nam
    dir_list = [os.path.join(dir_name, x) for x in sorted(os.listdir(dir_name)) if
                '.png' in x and os.path.isfile(os.path.join(dir_name, x))]
    with imageio.get_writer(gif_file_name, mode='I', duration=0.4) as writer:
        for filename in dir_list:
            writer.append_data(imageio.imread_v2(filename))


def month_in_summary(web_page, year_str, month_str, dir_name_prefix):
    dir_name = f'{dir_name_prefix}_{year_str}{month_str}'
    all_file_names = []
    if not os.path.isdir(dir_name):
        os.mkdir(dir_name)
    for day_of_month in range(1, 28):
        day_of_month_str = str(day_of_month)
        if len(day_of_month_str) == 1:
            day_of_month_str = '0' + day_of_month_str
        wayback_base_url = 'https://web.archive.org/web/'
        target_web_page = web_page
        for hour in ['00', '06', '12', '18']:
            wayback_timestamp = f'{year_str}{month_str}{day_of_month_str}{hour}3000'
            wayback_web_page = f'{wayback_base_url}{wayback_timestamp}/{target_web_page}'
            file_name = os.path.join(dir_name, generate_unique_filename(wayback_timestamp))
            all_file_names.append(file_name)
            save_wordcloud(wayback_web_page, file_name,
                           f'{web_page} on {year_str}-{month_str}-{day_of_month_str}')
    gif_file_name = os.path.join(dir_name, f'{dir_name_prefix}_{year_str}{month_str}.gif')
    make_gif(dir_name, gif_file_name)


def year_in_summary(web_page, year_str, dir_name_prefix):
    # Target days: the first of each month
    first_of_month = '01'
    dir_name = f'{dir_name_prefix}_{year_str}{first_of_month}'
    all_file_names = []
    if not os.path.isdir(dir_name):
        os.mkdir(dir_name)
    for month in range(1, 12):
        month_str = str(month)
        if len(month_str) == 1:
            month_str = '0' + month_str
        wayback_base_url = 'https://web.archive.org/web/'
        target_web_page = web_page
        for hour in ['00', '06', '12', '18']:
            wayback_timestamp = f'{year_str}{month_str}{first_of_month}{hour}3000'
            wayback_web_page = f'{wayback_base_url}{wayback_timestamp}/{target_web_page}'
            file_name = os.path.join(dir_name, generate_unique_filename(wayback_timestamp))
            all_file_names.append(file_name)
            save_wordcloud(wayback_web_page, file_name,
                           f'{web_page} on {year_str}-{month_str}-{first_of_month}')
    gif_file_name = os.path.join(dir_name, f'{dir_name_prefix}_{year_str}{month_str}.gif')
    make_gif(dir_name, gif_file_name)


if __name__ == '__main__':
    # month_in_summary('https://www.newsmax.com/', "2022", "02", "newsmax")
    # month_in_summary('https://www.nytimes.com/', "2022", "02", "nytimes")
    # month_in_summary('https://news.google.com/', "2022", "02", "googlenews")
    # month_in_summary('https://news.google.com/', "2021", "01", "googlenews")
    # month_in_summary('https://www.life.com/', "2021", "06", "life_magazine")
    year_in_summary('https://www.life.com/', "2020", "life_magazine")

