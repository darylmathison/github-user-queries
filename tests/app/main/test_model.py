import unittest
import app.main.model


class TestUserFactory(unittest.TestCase):
    def setUp(self):
        self.factory = app.main.model.User.keeper
        self.user = self.factory.create("test", "potato")

    def test_create(self):
        created_user = self.factory.create("test", "potato")
        self.assertEqual("test", created_user.get_id())

    def test_get_valid_user(self):
        self.assertEqual(self.factory.get("test").get_id(), self.user.get_id())

    def test_get_non_existant_user(self):
        self.assertIsNone(self.factory.get("fake"))


class TestUser(unittest.TestCase):
    def setUp(self):
        self.user = app.main.model.User("test", "potato")

    def test_get_id(self):
        self.assertEqual(self.user.get_id(), "test")

if __name__ == '__main__':
    unittest.main()
