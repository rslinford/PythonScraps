import os
from googleapiclient.discovery import build
from matplotlib import pyplot as plt
from wordcloud import WordCloud, STOPWORDS

api_key = os.environ.get('api_key')

stop_words = ['this', 'your', 'that', 'video', 'videos', 'with',
              'like', 'from', 'when', 'they', 'just', 'have', 'much',
              'very', 'what', 'also', 'than', 'also', 'because', 'them',
              'even', 'there', 'then', 'will', 'into', 'their', 'would',
              'about', 'their', 'does', 'should', 'these', 'more']

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


def tally_and_filter(words):
    word_tally = {}
    for word in words:
        word = word.lower()
        if only_alpha_ascii_chars(word) and len(word) > 3 and word not in stop_words:
            try:
                if word in word_tally.keys():
                    word_tally[word] += 1
                else:
                    word_tally[word] = 1
            except TypeError as e:
                print(f"Skipping problem word {word} because {e}")
    return word_tally


def get_comment_words(video_id):
    resource = build('youtube', 'v3', developerKey=api_key)
    words = []
    pageToken = ''
    while pageToken != None:
        # create a request to get 20 comments on the video
        response = resource.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=20,
            order="orderUnspecified",
            pageToken=pageToken).execute()

        items = response["items"]

        print(f"-------  Items returned {len(items)} ---------")
        for item in items:
            item_info = item["snippet"]

            # the top level comment can have sub reply comments
            topLevelComment = item_info["topLevelComment"]
            comment_info = topLevelComment["snippet"]

            print("Comment By:", comment_info["authorDisplayName"])
            print("Comment Text:", comment_info["textDisplay"])
            print("Likes on Comment :", comment_info["likeCount"])
            print("Comment Date: ", comment_info['publishedAt'])
            print("================================\n")

            words.extend(comment_info["textDisplay"].split())
        if "nextPageToken" in response:
            pageToken = response['nextPageToken']
        else:
            pageToken = None
    return words

video_id = 'avAMY6Kt6Nc'
# video_id = 'Vi9Y9AL13Rc' # tech with Tim
# video_id = 'oMfOpfUPX_8' # asmrmagic

words = get_comment_words(video_id)
tally = tally_and_filter(words)
wc = generate_from_freq(tally) # wordcloud
display_wordcloud(wc)
print(tally)
