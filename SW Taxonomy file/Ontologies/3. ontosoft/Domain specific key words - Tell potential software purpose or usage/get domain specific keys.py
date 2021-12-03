from html.parser import HTMLParser
import codecs


# class
class MyHTMLParser(HTMLParser):
    
    def handle_data(self, data):
        
        print(data)

  

 # create parser object
parser = MyHTMLParser()

# create parser object
parser = MyHTMLParser()

parser.feed(codecs.open("domain.html", "r", "utf-8").read())