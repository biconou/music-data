from allmusic_parse_discography import *

class TestClass:
    def test_parse(self):
        artistId = 'celtic-frost-mn0000191063'
        artistDiscography = parseDicography(artistId)
        assert artistDiscography[0]['albumYear'] == '1984'
        assert artistDiscography[0]['albumTitle'] == 'Morbid Tales'
        assert artistDiscography[1]['albumYear'] == '1985'
        assert artistDiscography[1]['albumTitle'] == 'To Mega Therion'
        assert artistDiscography[2]['albumYear'] == '1987'
        assert artistDiscography[2]['albumTitle'] == 'Into the Pandemonium'
        assert artistDiscography[3]['albumYear'] == '1988'
        assert artistDiscography[3]['albumTitle'] == 'Cold Lake'
        assert artistDiscography[4]['albumYear'] == '1989'
        assert artistDiscography[4]['albumTitle'] == 'Vanity/Nemesis'
        assert artistDiscography[5]['albumYear'] == '2006'
        assert artistDiscography[5]['albumTitle'] == 'Monotheist'
        assert artistDiscography[6]['albumYear'] == ''
        assert artistDiscography[6]['albumTitle'] == 'Live at the Hammersmith Odeon'
