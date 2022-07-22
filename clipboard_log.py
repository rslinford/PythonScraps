from datetime import datetime

import pyperclip as pyc


def make_word_cloud():
    pass


with open("Clipboard.log", "a") as log_file:
    i = 0
    while True:
        pyc.waitForNewPaste()
        text = pyc.paste()
        entry = f'{i:8}) {datetime.now().isoformat()}  {text}\n'
        print(entry, end="")
        log_file.write(entry)
        log_file.flush()
        i += 1
        if text.lower() == "stop it please":
            break
        elif text.lower() == "wordcloud":
            make_word_cloud()