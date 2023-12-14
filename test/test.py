import unittest
import requests

from shop_parser import Shop, Wildberries, MVideo, Item


class TestShops(unittest.TestCase):
    def test_wildberries(self):
        query = 'macbook air 13'
        items = Wildberries.parse_items(query)

        self.assertEqual(len(items), 5)

        for item in items:
            self.assertIsInstance(item.name, str)
            self.assertIsInstance(item.price, str)
            self.assertIsInstance(item.ref, str)
            self.assertIsInstance(item.pic, str)

            response = requests.get(item.ref)
            self.assertEqual(response.status_code, 200)

            response = requests.get(item.pic)
            self.assertEqual(response.status_code, 200)

    def test_mvideo(self):
        query = 'macbook air 13'
        items = MVideo.parse_items(query)

        self.assertEqual(len(items), 5)

        for item in items:
            self.assertIsInstance(item.name, str)
            self.assertIsInstance(item.price, str)
            self.assertIsInstance(item.ref, str)
            self.assertIsInstance(item.pic, str)

            response = requests.get(item.pic)
            self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
