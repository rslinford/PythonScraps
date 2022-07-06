import json
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import requests
from bs4 import BeautifulSoup

stop_words = ['three', 'after', 'which', 'about', 'might', 'would', 'could', 'every', 'really', 'years']


def filter_words(words):
    filtered_dict = dict()
    for w in words.keys():
        if len(w) < 5:
            continue
        if w.lower() in stop_words:
            continue
        w2 = w.strip('0123456789.,\'=_')
        if w2 != w:
            filtered_dict[w2] = words[w]
        else:
            filtered_dict[w] = words[w]
    return filtered_dict


def get_the_vanity_words(article_address):
    r = requests.get(article_address)
    soup = BeautifulSoup(r.text)
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


# Words from the times
def get_the_news_words():
    base_url = 'http://www.nytimes.com'
    r = requests.get(base_url)
    soup = BeautifulSoup(r.text)

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


# article_url = 'https://www.vanityfair.com/news/2022/07/donald-trump-2024-announcement-prosecution'
# article_url = 'https://www.vanityfair.com/style/2022/06/gabby-petito-death-brian-laundrie#intcid=_vanity-fair-verso-hp-trending_6304d215-7283-4465-8710-3807c98e6025_popular4-1'
# article_url = 'https://www.vanityfair.com/hollywood/2022/07/stranger-things-caleb-mclaughlin-interview-season-4-volume-2'
# article_url = 'https://www.vanityfair.com/style/2022/07/flamingo-estate-founder-richard-christiansens-summer-essentials'
# article_url = 'https://www.vanityfair.com/news/2021/07/rupert-murdoch-donald-trump-arizona-2020#intcid=_vanity-fair-bottom-recirc_0a7a3676-6b5b-443d-a430-5d4944c075b7_timespent-1yr-evergreen'
# article_url = 'https://www.vanityfair.com/news/2021/07/rupert-murdoch-donald-trump-arizona-2020#intcid=_vanity-fair-bottom-recirc_0a7a3676-6b5b-443d-a430-5d4944c075b7_timespent-1yr-evergreen'
article_url = 'https://www.vanityfair.com/news/2022/07/highland-park-shooting-limits-of-bipartisan-gun-compromise'
# article_url = 'https://www.vanityfair.com/style/2022/07/fka-twigs-viktor-rolf-good-fortune-interview'
# article_url = 'https://www.vanityfair.com/style/2022/07/how-patti-labelle-commanded-the-essence-festival-2022-stage-with-just-one-louboutin'
# article_url = 'https://www.vanityfair.com/style/society/2014/06/monica-lewinsky-humiliation-culture'

word_counts = filter_words(get_the_vanity_words(article_url))

print(word_counts)
wc = WordCloud(stopwords=STOPWORDS, collocations=True).generate_from_frequencies(word_counts)
plt.imshow(wc, interpolation='bilInear')
plt.axis('off')
plt.show()

word_counts = filter_words(get_the_news_words())
wc = WordCloud(stopwords=STOPWORDS, collocations=True).generate_from_frequencies(word_counts)
plt.imshow(wc, interpolation='bilInear')
plt.axis('off')
plt.show()
