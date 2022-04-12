import re

def clean_text(text):
    cleaned_text = re.sub('[a-zA-Z]', '', text)
    cleaned_text = re.sub('[\{\}\[\]\/;:""|\·)\n\t\r\r\n\r\n\r\n\r\n\r\n*~`^\-_+<>@…©\#$%&\\\=\(\'\"]',
                          '', cleaned_text)
    final_cleaned_text = ' '.join(cleaned_text.split())
    return final_cleaned_text