import re

def delete_punc(text):
    cleaned_text = re.sub('[a-zA-Z]', '', text)
    cleaned_text = re.sub('[\{\}\[\]\/;:""|\·..“”‘’!?,■◇◆※)\n\t\r\r\n\r\n\r\n\r\n\r\n*~`^\-_+<>@…©\#$%&\\\=\(\'\"]',
                          '', cleaned_text)
    punc_deleted_text = ' '.join(cleaned_text.split())
    return punc_deleted_text