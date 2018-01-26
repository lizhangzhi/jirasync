import requests
from html.parser import HTMLParser


class MyHTMLParser(HTMLParser):
    indicators = [('class', 'issue-link'), ('id', 'summary-val'), ('id', 'versions-val'), ('title', 'UX UX related changes')]

    def __init__(self):
        HTMLParser.__init__(self)
        self.flag = False
        self.com = False
        self.data_list = []

    def handle_starttag(self, tag, attrs):

        for i in self.indicators:
            if i in attrs:
                self.flag = True

    def handle_data(self, data):
        if self.flag:
            print(data.strip())
            self.data_list.append(data.strip())
            self.flag = False

if __name__ == "__main__":
    r = requests.get('https://116.12.252.147/dcifjira/browse/IDEAAA-40', verify=False, auth=('huina', 'ideal3@pwd33'))
    parser = MyHTMLParser()
    parser.feed(r.text)
