# 標準モジュールをimportする
import cgi
import os
import time
_weekdayname = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
_monthname = [None,
              "Jan", "Feb", "Mar", "Apr", "May", "Jun",
              "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


class Request(object):
    """
    HTTPのリクエストをハンドリングするクラス
    CGI側でインスタンを生成することによって利用する
    クエリデータや環境変数へのアクセス、主要ヘッダへの
    アクセス用メソッドを提供
    """
    def __init__(self, environ=os.environ):
        """
        インタンス初期化メソッド
        クエリ、環境変数をアトリビュートとして保持する
        """
        self.form=cgi.FieldStorage()
        self.environ=environ

class Response(object):
    """
    HTTPのレスポンスをハンドリングするクラス
    レスポンスを送る前にインスタンスを生成して利用する
    レスポンスやヘッダの内容の保持、ヘッダを含めたレスポンスの送信を行う
    """
    def __init__(self, charset='utf-8'):
        """
        インスタンス用の初期化メソッド
        ヘッダ用の辞書、本文用の文字列などを初期化する

        """
        self.headers={'Content-type':'text/html;charset={char}'.format(char=charset)}
        self.body=""
        self.status=200
        self.status_message='OK'
        self.http_ver = 'HTTP/1.1'

    def set_header(self, name, value):
        """
         レスポンスのヘッダを設定する
        :param name:
        :param value:
        :return:
        """
        self.headers[name]=value

    def get_header(self, name):
        """
        設定済みのレスポンス用ヘッダを返す
        :param name:
        :return:
        """
        return self.headers.get(name, None)

    def set_body(self, bodystr):
        """
        レスポンスとして出力する本文の文字列を返す
        :param bodystr:
        :return:
        """
        self.body=bodystr

    def make_output(self, timestamp=None):
        """
        ヘッダと本文を含めたレスポンス文字列を作る
        :param timestamp:
        :return:
        """
        if timestamp is None:
            timestamp = time.time()
            year, month, day, hh, mm, ss, wd, y, z = time.gmtime( timestamp)
            dtstr="%s, %02d %3s %4d %02d:%02d:%02d GMT" % (
                _weekdayname[wd], day,
                _monthname[month], year,
                hh, mm, ss
            )

            status_line = "{http} {status} {chk}".format(http=self.http_ver,
                                                         status=self.status,
                                                         chk=self.status_message)

            self.set_header("Last-Modified", dtstr)
            #headers='\n'.join(["%s: %s" % (k, v)
            #                   for k, v in self.headers.items()])

            headers = 'Content-type: text/html; charset=utf-8'

        return headers + '\n\n' + self.body

    def __str__(self):
        """
        リクエストを文字列に変換する
        """
        return self.make_output()

def get_htmltemplate():
    """
    レスポンスとして返すHTMLのうち、提携部分を返す
    :return:
    """
    html_body = """
<html>
        <head>
            <meta http-equiv="content-type"
                content="text/html;charset=utf-8" />
        </head>
        <body>
        {}
        </body>
</html>"""
    return html_body

def get_script():
    script = """
<script>alert("わーい");</script>
"""
    return script