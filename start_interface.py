import time
import cherrypy
import webbrowser
import random
import string
import compare_texts
try:
    webbrowser.open('http://127.0.0.1:8080')
except:
    pass
import time



def remove_html(text):
    import re
    text = re.sub("<.*?>", " ", text)
    text = text.replace('&nbsp', '')
    # remove html esc chars
    text = " ".join(filter(lambda x:x[0]!='&', text.split()))
    return text

def score_to_color(score):
    color = 'green'
    if score > 15:
        color = 'Gold'
    if score > 25:
        color = 'DarkOrange'
    if score > 50:
        color = 'red'
    return color

class StringGenerator(object):

    @cherrypy.expose
    def index(self, textinput=None, textinput2=None):
        if textinput is None:
            textinput = open('examples/text1.txt').read()
        if textinput2 is None:
            textinput2 = open('examples/text2.txt').read()
        textinput = remove_html(textinput)
        textinput2 = remove_html(textinput2)
        assert('span' not in textinput)
        textinput, textinput2, score = compare_texts.main(textinput, textinput2)
        #score = score[-1]
        frame_color = score_to_color(score)
        score_str = str(score)
        try:
            score_str = score_str[:5]
        except:
            pass
        print('frame_color ',frame_color)
        template = open('template.html').read()

        return template.replace('{textinput}',textinput).replace('{textinput2}',textinput2).replace('{framecolor}', frame_color).replace('{score}', score_str)




if __name__ == '__main__':
    cherrypy.quickstart(StringGenerator())