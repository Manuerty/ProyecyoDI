# style.py

def load_stylesheet():
    with open('style.qss', 'r') as style_file:
        return style_file.read()