from unittest import TestCase
from app import app
from models import User


class Blog(TestCase):

    def setUp(self):
        """Stuff to do before every test?"""

        self.client = app.test_client()
        app.config["TESTING"] = True

    def test_home(self):
        with app.test_client() as client:
            response = client.get("/")
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 302)
            self.assertEqual(response.location, "http://localhost/users")

    # def test_show_users(self):
    #     with app.test_client() as client:
    #         response = client.post(
    #             "/users", follow_redirects=True, data={'first_name': 'Martha', 'last_name': "Jenkins", "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTXRej6zzcY4qe5XWwSyrFpemK1dUaiXuoe3wBbJ8qff4lvPdoGCg"})
    #         html = response.get_data(as_text=True)

    #         self.assertEqual(response.status_code, 200)
    #         self.assertIn('>Martha Jenkins</a>', html)
