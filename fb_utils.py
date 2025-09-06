import pickle
import pyperclip

def save_to_file(data, file_name):
    with open(file_name, 'wb') as f:
        pickle.dump(data, f)

def get_link(post):
    first = post.find_element('xpath' , './/div/div/div/div/div/div/div/div/div/div/div/div/div[13]/div/div/div[2]/div/div[3]').click()
    copy_link = first.find_element('tag name', './div/div/div[1]/div[1]/div/div/div/div/div/div/div[1]/div/div[4]')
    copy_link.click()
    link = pyperclip.paste()
    return link
