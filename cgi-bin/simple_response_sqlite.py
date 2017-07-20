#!/usr/bin/env python
# coding: utf-8

from httphandler import Response, Request, get_htmltemplate
import pickle
import os
import sqlite3

form_body= """
<form method="POST" action="/cgi-bin/simple_response_sqlite.py">
好きな軽量言語は？<br />
{lang}
<input type="submit" />
</form>"""

radio_parts= """
<input type="radio" name="language" value="{lang}" />{lang}
<div style="border-left: solid {num}em red; ">{num}</div>
"""

conn = sqlite3.connect("./favorite_language.db")
curs = conn.cursor()

try:
    s = 'CREATE TABLE favorite_language(id integer primary key, language text, number int)'
    curs.execute(s)

except sqlite3.OperationalError:
    #print("テーブルがすでに存在しているため、作成はパスしました")
    pass

try:
    li = ["Python", "Ruby", "Perl", "PHP"]
    for i, row in enumerate(li):
        s = 'INSERT INTO favorite_language(id, language, number) VALUES (?, ?, ?)'
        curs.execute(s, (i, row, 0))
except sqlite3.IntegrityError:
    #print("すでに初期値は設定されていました")
    pass

lang_dic = {}
try:
    s = 'SELECT language, number FROM favorite_language'
    lang_dic.update(curs.execute(s))
except:
    #print("dic update error")
    pass

content = ""
req = Request()
try:
    if 'language' in req.form:
        lang = req.form['language'].value
        lang_dic[lang] = lang_dic.get(lang, 0) + 1
    
    u = 'UPDATE favorite_language SET number = ? WHERE language LIKE ?'
    curs.execute(u, (lang_dic.get(lang, 0), lang))
except:
    #print("update failue")
    pass

for lang in li:
    num = lang_dic.get(lang, 0)
    content += radio_parts.format(lang=lang, num=num)

res = Response()
body = form_body.format(lang=content)
res.set_body(get_htmltemplate().format(body))


print(res.make_output())
conn.commit()
curs.close()
conn.close()