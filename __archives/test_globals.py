from globals import *

class TestClass:
    def test_grabDiscography(self):
        x = computeRelatedRawHTMLFileName('toto')
        assert x == 'data/allmusic/discography/toto.raw.html'
