#!/usr/bin/env python
# coding: utf-8

import cgi
from datetime import datetime

html_body = """
<html><head>
    <meta http-equiv="content-type"
        content="text/html; charset=utf-8">
    </head>
    <body>
    {}
    </body>
</html>"""

content=''

form=cgi.FieldStorage()
year_str=form.getvalue('year', '')
if not year_str.isdigit():
    content=u"西暦を入力してください"
else:
    year=int(year_str)
    friday13=0
    for month in range(1, 13):
        date=datetime(year, month, 13)
        if date.weekday()==4:
            friday13 += 1
            content += u"{0}年{1}月13日は金曜日です".format(year, date.month)
            content += u"<br />"
    
    if friday13:
        content += u"{0}年には合計{1}個の13日の金曜日があります".format(year, friday13)
    else:
        content += u"{}年には13日の金曜日がありません".format(year)

print("Content-type: text/html; charset=utf-8\n")
print((html_body.format(content)))