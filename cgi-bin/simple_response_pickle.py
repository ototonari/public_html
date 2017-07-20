#!/usr/bin/env python
# coding: utf-8

from httphandler import Response, Request, get_htmltemplate
import pickle
import os

form_body= """
<form method="POST" action="/cgi-bin/simple_response.py">
好きな軽量言語は？<br />
{lang}
<input type="submit" />
</form>"""

radio_parts= """
<input type="radio" name="language" value="{lang}" />{lang}
<div style="border-left: solid {num}em red; ">{num}</div>
"""

lang_dic = {}
try:
    if os.path.exists('./favorite_language.dat'):
        with open('./favorite_language.dat', 'rb') as f:
            lang_dic = pickle.load(f)
        
except IOError:
    pass


content = ""
req = Request()
if 'language' in req.form:
    lang = req.form['language'].value
    lang_dic[lang] = lang_dic.get(lang, 0) + 1

with open('favorite_language.dat', 'wb') as f:
    pickle.dump(lang_dic, f)

for lang in ['Perl', 'PHP', 'Python', 'Ruby']:
    num = lang_dic.get(lang, 0)
    content += radio_parts.format(lang=lang, num=num)

res = Response()
body = form_body.format(lang=content)
res.set_body(get_htmltemplate().format(body))


print(res.make_output())
