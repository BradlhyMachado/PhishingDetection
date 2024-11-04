import unittest
from app import app
import json

class TestAnalizarUrl(unittest.TestCase):

    def setUp(self):
        # Configura el cliente de pruebas
        self.app = app.test_client()
        self.app.testing = True

    def test_url_sospechosa(self):
        # Prueba con una URL sospechosa
        url = "http://malicious.com"
        response = self.app.post('/analizar-url', 
                                 data=json.dumps({'url': url}),
                                 content_type='application/json')
        # Verifica la respuesta
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['sospechosa'], True)

    def test_url_no_sospechosa(self):
        # Prueba con una URL no sospechosa
        url = "http://safe.com"
        response = self.app.post('/analizar-url', 
                                 data=json.dumps({'url': url}),
                                 content_type='application/json')
        # Verifica la respuesta
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['sospechosa'], False)

if __name__ == '__main__':
    unittest.main()
