#! python3
# FacebookEditor.py - Removes extra lines of text from a Facebook page document, copied from FacebookCollector2.py .

import re
import pyperclip


def main():
    text = str(pyperclip.paste())
    text = deEmojify(text)
    text_lines = text.split('\n')
    write_file = open('C:/Users/kerry/Documents/NatalieClineDocuments/FormattedMcKinleyFacebookPosts.txt', 'a', encoding='utf-8')
    delete_comments = False
    post_num = 1
    write_file.write("Post #" + str(post_num))
    for i in text_lines:
        if 'Comment' in i or 'Comments' in i:
            delete_comments = True
        if delete_comments is True and i == '\r':
            delete_comments = False
            post_num += 1
            write_file.write("\nPost #" + str(post_num) + "\n")
        if delete_comments is False:
            write_file.write(i)
    write_file.close()
    print("Done")


def deEmojify(text):
    regrex_pattern = re.compile(pattern = "["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags = re.UNICODE)
    return regrex_pattern.sub(r'',text)


main()
