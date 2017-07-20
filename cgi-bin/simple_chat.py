#!/usr/bin/env python
# coding: utf-8

from httphandler import Response, Request, get_htmltemplate, get_script
import pickle
import os
import sqlite3
import re

prog = re.compile("[0-9a-zA-Z]+")

form_body= """
<form method="POST" action="/cgi-bin/simple_chat.py">
<br />
{text_parts}:
<input type="submit" name="submit" />
<input type="submit" name="reset" value="" />
</form>
<p>{current_chat}</p>
<p>{text_list}</p>
<br />
"""

text_parts= """
<input type="text" size="30" maxlength="30" name="chat" value="" />
"""

text_list= """
{chat}<br />
"""



conn = sqlite3.connect("./chat.db", isolation_level=None)
curs = conn.cursor()

try:
    s = 'CREATE TABLE chat_log(id integer primary key, chat text)'
    curs.execute(s)

except sqlite3.OperationalError:
    pass

chat_list = []
content = ""
try:
    s = 'SELECT chat FROM chat_log ORDER BY id ASC'
    for line in list(curs.execute(s)):
        chat_list.append(line[0])
    
    for line in reversed(chat_list):
        content += text_list.format(chat=line)
except:
    pass

req = Request()
#chat = ""

try:
    reset = req.form.getvalue('reset', False)
    chat = req.form.getvalue('chat', "")
    if reset:
        d = 'DELETE FROM chat_log'
        curs.execute(d)
        content = ""
    elif chat:
        tmp_list = re.split('\W+', chat)
        chat = "".join(tmp_list)
        if len(chat) > 30:
            chat = chat[:30]
        id_number = len(chat_list)
        i = 'INSERT INTO chat_log(id, chat) VALUES (?, ?)'
        curs.execute(i, (id_number, chat))
        curs.execute("vacuum")
        
except:
    pass

res = Response()

body = form_body.format(text_parts=text_parts,text_list=content, current_chat=chat)
res.set_body(get_htmltemplate().format(body))

print(res.make_output())

try:
    curs.close()
    conn.close()
except:
    pass