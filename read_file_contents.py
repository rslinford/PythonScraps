
# Read file. Count words.
word_counter = {}
with open("textfile.txt", "r") as f:
    line = f.readline()
    while line:
        line = line.strip()
        words = line.split('/')
        for w in words:
            if len(w) == 0:
                continue
            if w not in word_counter:
                word_counter[w] = 1
            else:
                word_counter[w] += 1
        line = f.readline()
print(word_counter)
