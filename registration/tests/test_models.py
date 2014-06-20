from django.test import TestCase

from liwi import fixtures
from registration.models import User, SecurityAnswer, SecurityQuestion

class RegistrationModelsTest(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_create_user(self):
        """
            Test creation of a user record
        """
        user = fixtures.create_user(
            username='test_user', password='password', email='user@test.com', first_name='test', last_name='user'
        )

        self.assertTrue(isinstance(user, User))

    def test_create_security_question(self):
        """
            test creation of a security question record
        """

        security_question = fixtures.create_security_question(question='Test question?')

        self.assertTrue(isinstance(security_question, SecurityQuestion))

    def test_create_security_answer(self):
        """
            Test creation of a security answer record

        """

        user = fixtures.create_user(
            username='test_user', password='password', email='user@test.com', first_name='test', last_name='user'
        )

        security_question = fixtures.create_security_question(question='Test question?')

        security_answer = fixtures.create_secret_answer(
            user_id=user.id, question_id=security_question.id, answer='Test Answer'
        )

        self.assertTrue(isinstance(security_answer, SecurityAnswer))