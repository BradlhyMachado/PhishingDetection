import unittest
from app import app
import json

class TestAnalizarUrl(unittest.TestCase):

    def setUp(self):
        # Configura el cliente de pruebas
        self.app = app.test_client()
        self.app.testing = True


    '''
    www.piclist.com/techref/piclist/jal/
    https://onedrive.live.com/download?cid=8FCB5E3154D8D2B8&resid=8FCB5E3154D8D2B8%214551&authkey=ABQZBwkdLd0fudo
    '''
    def test_url_sospechosa(self):
        # Prueba con una URL sospechosa
        url = "http://174.128.226.101/yakuza.i586"
        response = self.app.post('/analizar-url', 
                                 data=json.dumps({'url': url}),
                                 content_type='application/json')
        # Verifica la respuesta
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['sospechosa'], True)

    '''
    http://djsipke.nl/foto-album/5-druiprock-2010/detail/293-p8148754.html?tmpl=component
    english.turkcebilgi.com/Melodi+Grand+Prix
    '''
    def test_url_no_sospechosa(self):
        # Prueba con una URL no sospechosa
        url = "paypal.com.us.cgi.bin.webscr.cmd.login.member.verifed.crazynightsprod.com/54855458214/deb2e574f0b9cbc9b5cab5d9ca080039/"
        response = self.app.post('/analizar-url', 
                                 data=json.dumps({'url': url}),
                                 content_type='application/json')
        # Verifica la respuesta
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['sospechosa'], False)

if __name__ == '__main__':
    unittest.main()
