from django.contrib.auth.hashers import make_password
from django.core.files.base import File
from django.test import TestCase

from art.models import Art, Like, Category, Tag, ArtTag, upload_to
from registration.models import User


class ArtModelsTests(TestCase):
    ##### model creation fixtures #####

    def create_user(self, username, password, email, first_name, last_name):
        hashed_password = make_password(password)

        return User.objects.create(username=username,
                                   password=hashed_password,
                                   email=email,
                                   first_name=first_name,
                                   last_name=last_name,
                                   is_active=True,
                                   is_superuser=False,
                                   is_staff=False,
                                   is_artist=True,
                                   )

    def create_category(self, name):
        return Category.objects.create(name=name)

    def create_art(self, user_id, category, photo, title, description):
        return Art.objects.create(user_id=user_id,
                                  category=category,
                                  photo=photo,
                                  title=title,
                                  description=description
                                  )

    def create_tag(self, name):
        return Tag.objects.create(name=name)

    def create_art_tag(self, art_id, tag_id):
        return ArtTag.objects.create(art_id=art_id, tag_id=tag_id)

    def create_art_like(self, user_id, art_id):
        return Like.objects.create(
            user_id=user_id, art_id=art_id
        )
    ####### end model fixtures ########

    ###### model tests ########

    def test_art_creation(self):
        """
            Test creation of an art record
        """

        user = self.create_user(
            username='test_user', password='password', email='user@test.com', first_name='test', last_name='user'
        )

        category = self.create_category(name='Test Category')
        art_photo = File('art/tests/resources/test_photo.jpg')
        art = self.create_art(
            user_id=user.id, category=category.id, photo=art_photo, title='Test Art', description='Some art'
        )

        self.assertTrue(isinstance(art, Art))

    def test_category_creation(self):
        """
            Test creation of a category record
        """

        category = self.create_category(name='Test Category')

        self.assertTrue(isinstance(category, Category))

    def test_like_creation(self):
        """
            test creation of an art like record
        """

        user = self.create_user(
            username='test_user', password='password', email='user@test.com', first_name='test', last_name='user'
        )

        category = self.create_category(name='Test Category')

        art = self.create_art(
            user_id=user.id, category=category.id, photo='test/photo', title='Test Art', description='Some art'
        )

        art_like = self.create_art_like(user_id=user.id, art_id=art.id)

        self.assertTrue(isinstance(art_like, Like))

    def test_tag_creation(self):
        """
            test creation of a tag
        """

        tag = self.create_tag(name='Test Tag')

        self.assertTrue(isinstance(tag, Tag))

    def test_art_tag_creation(self):
        """
            test creation of an art record with tags, and retrieving the tags with the art get_tags
            function
        """
        
        user = self.create_user(
            username='test_user', password='password', email='user@test.com', first_name='test', last_name='user'
        )

        category = self.create_category(name='Test Category')

        art = self.create_art(
            user_id=user.id, category=category.id, photo='test/photo', title='Test Art', description='Some art'
        )

        tag = self.create_tag(name='Test Tag')

        art_tag = self.create_art_tag(art_id=art.id, tag_id=tag.id)

        self.assertTrue(isinstance(art_tag, ArtTag))

        tags = art.get_tags()
        self.assertEqual(tags = 'Test Tag')