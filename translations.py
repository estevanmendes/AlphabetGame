from ast import literal_eval

class translations:
    
    def __init__(self,language_code) -> None:
        self.titles=self.load_titles()[language_code]
        self.button_names=self.load_button_names()[language_code]
        self.texts=self.load_texts()[language_code]
        self.language_code=language_code


    def load_titles(self):
        with open('settings/titles.txt','r') as f:
            titles_dict=literal_eval(f.read())
        return titles_dict

    def load_button_names(self):
        with open('settings/buttons.txt','r') as f:
            button_names_dict=literal_eval(f.read())
        return button_names_dict

    def load_texts(self):
        with open('settings/texts.txt','r') as f:
            texts_dict=literal_eval(f.read())
        return texts_dict


    def get_button_name(self,button_name):
        return self.button_names[button_name]
        

    def get_title(self,title_name):
        return self.titles[title_name]

    def get_text(self,text_name):
        return self.texts[text_name]


