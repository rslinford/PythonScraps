import nltk
from nltk import sent_tokenize, word_tokenize, WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.stem.snowball import PorterStemmer

def tokenize_example():
    example_string = ("Muad'Dib learned rapidly because his first training was in how to learn.\n"
                      "And the first lesson of all was the basic trust that he could learn.\n"
                      "It's shocking to find how many people do not believe they can learn,\n"
                      "and how many more believe learning to be difficult.")
    for i, sentence in enumerate(sent_tokenize(example_string)):
        print(i, sentence)
    for word in word_tokenize(example_string):
        print(word)

def filtering_stop_words():
    worf_quote = "Sir, I protest. I am not a merry man!"
    words_in_quote = word_tokenize(worf_quote)
    print(words_in_quote)
    stop_words = set(stopwords.words("english"))

    filtered_list = [
        word for word in words_in_quote if word.casefold() not in stop_words
    ]
    for word in filtered_list:
        print(word)

def stemming():
    stemmer = PorterStemmer()
    string_for_stemming = ("The crew of the USS Discovery discovered many discoveries.\n"
                           " Discovering is what explorers do")
    words = word_tokenize(string_for_stemming)
    for word in words:
        print(word)
    stemmed_words = [stemmer.stem(word) for word in words]
    print()
    for word in stemmed_words:
        print(word)

def parts_of_speach():
    sagan_quote = ("If you wish to make an apple pie from scratch,\n"
                   "you must first invent the universe.")

    words_in_sagan_quote = word_tokenize(sagan_quote)
    tagged_words = nltk.pos_tag(words_in_sagan_quote)
    for word in tagged_words:
        print(word)

    jabberwocky_excerpt = ("'Twas brillig, and the slithy toves did gyre and gimble in the wabe:\n"
                           "all mimsy were the borogoves, and the mome raths outgrabe.")
    words_in_jaberwocky_excerpt = word_tokenize(jabberwocky_excerpt)
    tagged_words = nltk.pos_tag(words_in_jaberwocky_excerpt)
    for word in tagged_words:
        print(word)

def lemmatizing():
    lemmatizer = WordNetLemmatizer()
    print('scarves', lemmatizer.lemmatize('scarves'))
    print('geese', lemmatizer.lemmatize('geese'))
    print('worst', lemmatizer.lemmatize('worst', pos='a')) # Specify adjective as part of speech. The default POS is noun.
    string_for_lemmatizing = "The friends of DeSoto love scarves."
    words_for_lemmatizing = word_tokenize(string_for_lemmatizing)
    lemmatized_words = [lemmatizer.lemmatize(word) for word in words_for_lemmatizing]
    [print(word) for word in lemmatized_words]

def chunking_and_chinking():
    lotr_quote = "It's a dangerous business, Frodo, going out your door."
    words_in_lotr_quote = word_tokenize(lotr_quote)
    lotr_pos_tags = nltk.pos_tag(words_in_lotr_quote)
    grammar = "NP: {<DT>?<JJ>*<NN>}"
    chunk_parser = nltk.RegexpParser(grammar)
    tree = chunk_parser.parse(lotr_pos_tags)
    tree.draw()
    grammar = """
        Chunk: {<.*>+}
               }<JJ>{"""
    chunk_parser = nltk.RegexpParser(grammar)
    tree = chunk_parser.parse(lotr_pos_tags)
    tree.draw()

def named_entity_recognition():
    lotr_quote = "It's a dangerous business, Frodo, going out your door."
    words_in_lotr_quote = word_tokenize(lotr_quote)
    lotr_pos_tags = nltk.pos_tag(words_in_lotr_quote)
    tree = nltk.ne_chunk(lotr_pos_tags)
    tree.draw()
    tree = nltk.ne_chunk(lotr_pos_tags, binary=True)
    tree.draw()
    wotw_quote = ("Men like Schiaparelli watched the red planet—it is odd, by-the-bye, that\n"
             "for countless centuries Mars has been the star of war—but failed to\n"
             "interpret the fluctuating appearances of the markings they mapped so well.\n"
             "All that time the Martians must have been getting ready.\n"
             "\n"
             "During the opposition of 1894 a great light was seen on the illuminated\n"
             "part of the disk, first at the Lick Observatory, then by Perrotin of Nice,\n"
             "and then by other observers. English readers heard of it first in the\n"
             "issue of Nature dated August 2.")

    def extract_ne(quote):
        words = word_tokenize(wotw_quote, language='english')
        tags = nltk.pos_tag(words)
        tree = nltk.ne_chunk(tags, binary=True)
        tree.draw()
        return set(
            ' '.join(i[0] for i in t) for t in tree
        )

    print(extract_ne(wotw_quote))

named_entity_recognition()