import json
import os
import time
import uuid

import imageio as imageio
import matplotlib.pyplot as plt
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from wordcloud import WordCloud, STOPWORDS

# The Wayback Machine base address
wayback_base_url = 'https://web.archive.org/web/'

# Characters to be stripped before word is checked against stop list
strip_chars = '0123456789.,\'=_:[]{}-?!/<>"'

stop_words = ['about', 'after', 'associated', 'content', 'continue', 'could', 'esquire', 'every',
              'first', 'friday', 'greatest', 'guardian', 'hours', 'iconic', 'issue', 'might', 'minutes',
              'model', 'monday', 'movie', 'movies', 'news', 'newsmax', 'people', 'photographs', 'picture',
              'reading', 'really', 'saturday', 'scenes', 'story', 'sunday', 'their', 'three',
              'thursday', 'times', 'tuesday', 'vanity', 'wednesday', 'which', 'would',
              "year's", 'years', 'google', 'months', 'seconds', 'internet', 'wayback']


# Wordcloud includes words that are 5 characters or longer. Stopwords are checked. And 'weird'
# characters are stripped.
def filter_words(words):
    filtered_dict = dict()
    for w in words.keys():
        if len(w) < 5:
            continue
        if w.lower() in stop_words:
            continue
        w2 = w.strip(strip_chars)
        if len(w2) < 5:
            continue
        if w2 != w:
            filtered_dict[w2] = words[w]
        else:
            filtered_dict[w] = words[w]
    return filtered_dict


def only_alpha_ascii_chars(word):
    for c in word:
        if c < 'A' or c > 'z' or ('Z' < c < 'a'):
            return False
    return True


def is_cammel_case(word):
    has_lower_case = False
    for c in word:
        if 'a' <= c <= 'z':
            has_lower_case = True
        if 'A' <= c <= 'Z' and has_lower_case:
            return True
    return False


# Parsing not customized to any web-site. Attempts to get
# all text from web page.
def get_words_general_parsing(article_address):
    print(f'Requesting: {article_address}')
    r = requests.get(article_address)
    soup = BeautifulSoup(r.text, features="lxml")
    word_dict = dict()
    words = soup.text.split(" ")
    for w in words:
        # Strip 'garbage' characters from candidate word
        w = w.strip(strip_chars)
        # Candidate word must be 5 or longer
        if len(w) < 5:
            continue
        # Candidate must not be cammel case
        if is_cammel_case(w):
            continue
        # Candidate must not be stop words
        if w.lower() in stop_words:
            continue
        # Candidate must contain Alpha chars only
        if not only_alpha_ascii_chars(w):
            continue
        # Tally the word that finally passes
        if w in word_dict.keys():
            word_dict[w] += 1
        else:
            word_dict[w] = 1
    return word_dict


# Custom parsing for the NY Times. Not used.
# Included here as an example of targeted content
# extraction.
def get_the_news_words():
    base_url = 'http://www.nytimes.com'
    r = requests.get(base_url)
    soup = BeautifulSoup(r.text, features="lxml")

    summary_list = []
    # Target the article summaries. This is specific to the NY Time website.
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


# Custom parsing for YouTube. Generic parsing gets 0 words.
def get_the_youtube_words(web_address='https://www.youtube.com'):
    browser = webdriver.Chrome()
    browser.get(web_address)
    browser.execute_script("window.scrollTo(0,500)")
    time.sleep(2)
    browser.execute_script("window.scrollTo(0,3000)")
    time.sleep(7)
    content = browser.page_source
    browser.close()

    # Target the article summaries. This is specific to the NY Time website.
    words = dict()
    for w in content.split(' '):
        if not only_alpha_ascii_chars(w):
            continue
        if w in words.keys():
            words[w] += 1
        else:
            words[w] = 1
    return filter_words(words)


# Parsing customized for Vanity Fair which packs the entire article in JSON wrapper.
# This function isn't being used at the moment. It's here as another example of
# custom parsing.
def get_the_vanity_words_custom_parsing(article_address):
    r = requests.get(article_address)
    soup = BeautifulSoup(r.text, features="lxml")
    word_dict = dict()
    # Extract JSON via the type attribute specific to Vanity Fair
    for x in soup.find_all(type="application/ld+json"):
        # Convert JSON to a Python dict
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


def generate_from_freq(word_counts):
    return WordCloud(stopwords=STOPWORDS, collocations=True, background_color='dimgray',
                     width=900, height=500, colormap='YlGnBu', max_words=400
                     ).generate_from_frequencies(word_counts)


# Shows the plot in a pop-up window
def display_wordcloud(web_page):
    word_counts = get_words_general_parsing(web_page)
    print(word_counts)
    wc = generate_from_freq(word_counts)
    plt.imshow(wc, interpolation='bilInear')
    plt.axis('off')
    plt.show()


# Create the plot and save it. Optionally a test_run=True means nothing gets saved, only shown on screen.
def save_wordcloud(web_page, file_name, title, test_run=False, get_words=get_words_general_parsing):
    word_counts = get_words(web_page)
    wc = generate_from_freq(word_counts)
    plt.imshow(wc, interpolation='bilInear')
    plt.axis("off")
    plt.title(title)
    if test_run:
        print(f'Showing wordcloud from {web_page} to file: {file_name}')
        plt.show()
    else:
        print(f'Saving wordcloud from {web_page} to file: {file_name}')
        plt.savefig(file_name)


# Used in file names to prevent name conflicts
def generate_unique_filename(prefix):
    uid = uuid.uuid4().hex
    return f'{prefix}_{uid}.png'


# Makes an animated GIF from all the PNG files in dir_name
def make_gif(dir_name, gif_file_name):
    print(f'Creating {gif_file_name} from PNG files in {dir_name}')
    # Get directory listing with each file name prepended with dir_name
    dir_list = [os.path.join(dir_name, x) for x in sorted(os.listdir(dir_name)) if
                '.png' in x and os.path.isfile(os.path.join(dir_name, x))]
    with imageio.get_writer(gif_file_name, mode='I', duration=0.5) as writer:
        for filename in dir_list:
            writer.append_data(imageio.imread_v2(filename))


# Does the live version of the web-site instead of from the Wayback Machine
def live_page_summary(web_page):
    display_wordcloud(web_page)


def month_in_summary(web_page, year_str, month_str, dir_name_prefix, test_run=False,
                     get_words=get_words_general_parsing):
    dir_name = f'{dir_name_prefix}_{year_str}{month_str}'
    if not os.path.isdir(dir_name) and not test_run:
        os.mkdir(dir_name)
    for day_of_month in range(1, 29):
        day_of_month_str = f'{day_of_month:02}'
        if test_run:
            hours = ['06']
        else:
            hours = ['00', '06', '12', '18']
        for hour in hours:
            wayback_timestamp = f'{year_str}{month_str}{day_of_month_str}{hour}3000'
            wayback_web_page = f'{wayback_base_url}{wayback_timestamp}/{web_page}'
            file_name = os.path.join(dir_name, generate_unique_filename(wayback_timestamp))
            save_wordcloud(wayback_web_page, file_name, f'{web_page} on {year_str}-{month_str}-{day_of_month_str}',
                           test_run, get_words)
    if not test_run:
        gif_file_name = os.path.join(dir_name, f'{dir_name_prefix}_{year_str}{month_str}.gif')
        make_gif(dir_name, gif_file_name)


def year_in_summary(web_page, year_str, dir_name_prefix, test_run=False):
    # Target days: the first of each month
    first_of_month = '01'
    dir_name = f'{dir_name_prefix}_{year_str}{first_of_month}'
    if not os.path.isdir(dir_name) and not test_run:
        os.mkdir(dir_name)
    for month in range(1, 13):
        month_str = f'{month:02}'
        for hour in ['00', '06', '12', '18']:
            wayback_timestamp = f'{year_str}{month_str}{first_of_month}{hour}3000'
            wayback_web_page = f'{wayback_base_url}{wayback_timestamp}/{web_page}'
            file_name = os.path.join(dir_name, generate_unique_filename(wayback_timestamp))
            save_wordcloud(wayback_web_page, file_name, f'{web_page} on {year_str}-{month_str}-{first_of_month}',
                           test_run)
    if not test_run:
        gif_file_name = os.path.join(dir_name, f'{dir_name_prefix}_{year_str}{month_str}.gif')
        make_gif(dir_name, gif_file_name)


if __name__ == '__main__':
    # month_in_summary('https://www.newsmax.com/', "2022", "02", "newsmax_month", test_run=False)
    # month_in_summary('https://www.nytimes.com/', "2022", "02", "nytimes")
    # month_in_summary('https://news.google.com/', "2022", "02", "googlenews")
    # month_in_summary('https://news.google.com/', "2022", "07", "googlenews", test_run=True)
    # month_in_summary('https://www.life.com/', "2021", "06", "life_magazine")
    # year_in_summary('https://www.life.com/', "2021", "life_magazine_year", test_run=True)
    # year_in_summary('https://news.google.com/', "2021", "google_news_year")
    # live_page_summary('https://news.google.com/')
    # live_page_summary('https://www.nytimes.com/')
    month_in_summary('https://www.youtube.com/', "2022", "06", "youtube", test_run=False, get_words=get_the_youtube_words)
