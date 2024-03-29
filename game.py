import streamlit as st
import string
from ast import literal_eval
from random import randint,random
import time
import requests
import shutil
import os
from translations import translations

def button_click(button_key:str):
    if button_key in st.session_state:
        st.session_state[button_key] = True
    
    if 'end_game' in st.session_state:
        if time.time()>st.session_state['end_game']:
            GameOver()
            
def GameOver():
    gameover_message=translation.get_title('gameover')
    st.markdown(f'# {gameover_message}')


def initialize_buttons(button_key):
    if button_key not in st.session_state:
        st.session_state[button_key] = False



def game_off_only(func):
    def wrapper(*args,**kwargs):
        if not ('game_on' in st.session_state and st.session_state['game_on']):
            return func(*args,**kwargs)
        else:
            return None
    return wrapper

def game_on_only(func):
    def wrapper(*args,**kwargs):
        if 'game_on' in st.session_state and st.session_state['game_on']:
            return func(*args,**kwargs)
        else:
            return None
    return wrapper

def centralize(n=3):
    cols=st.columns(n)
    return cols[n//2]

def load_themes():
    with open('themes.txt','r') as f:
        themes=f.readlines()
    return themes

def load_random_theme():
    key=os.getenv('ninja_api_key')
    type='noun'
    api_url = 'https://api.api-ninjas.com/v1/randomword?type={}'.format(type)
    response = requests.get(api_url, headers={'X-Api-Key': key})
    if response.status_code == requests.codes.ok:
        theme=response.json()['word']
    else:
        print("Error:", response.status_code, response.text)
        theme='Not Found'
    return theme

def get_random_theme(themes=None):
    theme=load_random_theme()
    st.session_state['theme']=theme

    return theme

def display_random_theme(theme=None):
    theme_word=translation.get_title('theme_word')
    if not theme:
        if 'theme' in st.session_state:
            
            theme=st.session_state['theme']
            
            if theme=='img':
                display_image_theme()
            else:
                st.markdown(f'<h1> <center>{theme_word}: {theme}</center></h1>',unsafe_allow_html=True)
                
    elif theme:
            if theme=='img':
                display_image_theme()
            else:

                st.markdown(f'<h1> <center> {theme_word}: {theme}</center></h1>',unsafe_allow_html=True)

 
async def stopwatch():
    if  'start' in st.session_state and st.session_state['start']:
        if 'timer' not in st.session_state:
            get_random_time()

        timer=st.session_state['timer']           
        if 'timer_temp' not in st.session_state:
            st.session_state['timer_temp']=timer

        timer_temp=st.session_state['timer_temp']
        percentage=int(timer_temp/timer*100)
        step=100/timer
        if True:
            # bar=st.progress(percentage,'Timer')
            while (timer_temp>0):
                timer_temp-=1
                st.session_state['timer_temp']=timer_temp
                await asyncio.sleep(0.1)
                percentage-=step
                # bar.progress(int(percentage),text='Timer')

def start_game():
    if 'theme' in st.session_state:
        button_click(button_key='start')
        # asyncio.run(stopwatch())
        if 'timer' not in st.session_state:
                get_random_time()
        st.session_state['end_game']=time.time()+st.session_state['timer']
        st.session_state['game_on']=True
    else:
        theme_warning=translation.get_title('themeWarning')
        st.markdown(f'# {theme_warning}')


def game_on_display():
    if 'end_game' in st.session_state:
        with st.sidebar:
            gameon_message=translation.get_title('gameon')
            st.markdown(f'# {gameon_message}')
            st.markdown('## TikTak, TikTak, Tiktak...')



def get_random_time():
    button_click(button_key='start')
    min=to_seconds(st.session_state['min_time'])
    max=to_seconds(st.session_state['max_time'])
    time=randint(min,max)
    st.session_state['timer']=time
    return time

def to_seconds(time):
    seconds=0
    seconds+=int(time)*60
    seconds+=int((time-int(time))*60)
    return seconds

def side_bar():
    with st.sidebar:
        game_on_display()
        start_game_button()
        reset_game_button()
     
        

def start_game_button(pos=st,**kwargs):
    initialize_buttons('start')
    button_name=translation.get_button_name('start')
    pos.button(button_name,on_click=start_game,disabled=st.session_state['start'],**kwargs)

def reset_game_button(pos=st,**kwargs):
    button_name=translation.get_button_name('reset')
    pos.button(button_name,on_click=reset_actions,**kwargs)
    

def reset_actions():
    language=st.session_state['language_code']
    clear_cache()
    st.session_state['game_on']=False
    st.session_state['language_code']=language

def clear_cache():
    for key in st.session_state:
        del st.session_state[key]


def set_timer_range():
    if 'time_limits' in st.session_state:
        min,max=st.session_state['time_limits']
        st.session_state['min_time']=min
        st.session_state['max_time']=max    

    else:
        st.session_state['min_time']=0.1
        st.session_state['max_time']=0.2


def get_random_key():
    # return {'key':str(time.time_ns())+str(random())}
    return {'key':None}


def create_button(col,label,session_key,tracked=True,translate=False,**kwargs):
    initialize_buttons(session_key)
    disabled=st.session_state[session_key]
    if translate:
        label=translation.button_names(session_key)
    return  col.button(label,on_click=button_click,args=session_key,disabled=disabled,**get_random_key(),**kwargs)

@game_on_only
def alphabet_buttons():
    columns=5
    for row in range(len(letters)//columns+len(letters)%columns):
        cols=st.columns(columns)
        for index,col in enumerate(cols):
            letter_index=row*columns+index
            if letter_index>=len(letters):
                break
                
            letter=letters[letter_index]
            create_button(col,letter,letter)

def theme_seted_only(func):
    def wrapper(*args,**kwargs):
        if 'theme' in st.session_state:
            return func(*args,**kwargs)
        else:
            return None
    return wrapper

@game_off_only
@theme_seted_only
def start_game_display():
    start_game_button(pos=centralize(5),key='startgameMain')
    
@game_off_only
def timer_components():
    with st.sidebar:
        timer_message=translation.get_title('timer')
        st.markdown(f'{timer_message}')
        timer_button_name=translation.get_button_name('timer')
        timer=st.slider(timer_button_name,min_value=0.5,max_value=4.0,value=(1.5,3.0),step=0.1,on_change=set_timer_range)
        st.session_state['time_limits']=timer
        cols=st.columns(5)
        timer_button_visibility='visible'
        initialize_buttons(timer_button_visibility)




@game_off_only
def theme_components():
    cols=st.columns(5)
    word_button_name=translation.get_button_name('themeWord')
    image_button_name=translation.get_button_name('themeImage')
    cols[1].button(word_button_name,on_click=get_random_theme)
    cols[3].button(image_button_name,on_click=load_img_theme)


def load_img_theme():

    key=os.getenv('ninja_api_key')
    category = ''
    api_url = 'https://api.api-ninjas.com/v1/randomimage?category={}'.format(category)
    response = requests.get(api_url, headers={'X-Api-Key': key, 'Accept': 'image/jpg'}, stream=True)
    if response.status_code == requests.codes.ok:
        with open('img.jpg', 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
    else:
        print("Error:", response.status_code, response.text)
    time.sleep(0.1)
    st.session_state['theme']='img'

def display_image_theme():
    st.image('img.jpg')


def header():
    lasting_letters()
    pass
  
@game_on_only
def lasting_letters():
    letters_avaible=0
    for letter in letters:
        if not letter in st.session_state :        
            letters_avaible=len(letters)
            break
        elif not st.session_state[letter]:            
            letters_avaible+=1

    if letters_avaible==0:
        game_draw()
        reset_game_button(pos=centralize(5),key='anotherReset')
    else:    
        letters_avaible_message=translation.get_title('letters')
        st.markdown(f'<h1><center>{letters_avaible} {letters_avaible_message}!</center></h1>',True)

def hint():
    pass


def game_draw():
    draw_message=translation.get_title('draw')
    st.markdown(f"<h1><center>{draw_message}</center></h1>",True)

@game_off_only
def help_button(**kwargs):
    help_button_name=translation.get_button_name('help')
    st.sidebar.button(f'{help_button_name}',on_click=game_rules)


def game_rules():
    rules=translation.get_text('rules')
    st.sidebar.write(f'{rules}')

def load_language_options():
    with open('settings/language_options.txt','r') as f:
        options=literal_eval(f.read())
    return options

@game_off_only
def language_options():
    options=load_language_options()
    

    language_title()

    cols=st.columns(len(options))
    for col,(country,path) in zip(cols,options.items()):
        col.image(path,width=100)
        col.button(country,on_click=set_language,args=(country,))


def language_title():
    language_message=translation.get_title('language')
    st.write(language_message)


def set_language(code):
    st.session_state['language_code']=code

def lower_side_bar():
    with st.sidebar:
        help_button()   
        language_options()


def main():
    global translation
    print(st.session_state['language_code'],'---')
    translation=translations(st.session_state['language_code'])
    side_bar()
    theme_components()
    display_random_theme()
    start_game_display()
    set_timer_range()
    timer_components() 
    alphabet_buttons()
    lasting_letters()
    lower_side_bar()

def default():
    
    if not 'language_code' in st.session_state: 
        st.session_state['language_code']='US'
    print(st.session_state['language_code'],'---')
    global letters
    letters=list(string.ascii_uppercase.replace('Y','').replace('W','').replace('K',''))
    

default()
main()
