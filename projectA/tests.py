import unittest
from __init__ import app
from exts import db
from model import User
import config 
from flask import request

class BaseTestCase(unittest.TestCase):
    def create_app(self):
        app.config.from_object(config)
        return app
    def setup(self):
        db.create_all()
        db.session.add(User('牛牛','日蹦'))
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

class test_rigist(BaseTestCase):
    def test_index(self):
        tester = app.test_client()
        response = tester.get('/login/', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_rigist(self):
        tester = app.test_client()
        response = tester.post('/regist/',data=dict(username='mick',password='11'),follow_redirects=True)
        self.assertIn(byte(u'註冊'), response.data)

if __name__ == '__main__':
    unittest.main()