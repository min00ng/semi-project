
import re
def clean_text(title):
    text_rmv = re.sub('[-=+,#/\?:^.@*\"※%~∼ㆍ!【】』㈜©囹圄秋 ■◆◇▷▶◁◀ △▲▽▼<>‘|\(\)\[\]`\'…》→←↑↓↔〓♤♠♡♥♧♣⊙◈▣◐◑☆★\”\“\’·※~ ! @ # $ % ^ & * \ " ]', ' ', title)
    text_rmv = ' '.join(text_rmv.split())
    return text_rmv