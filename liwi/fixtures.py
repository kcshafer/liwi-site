from django.contrib.auth.hashers import make_password

from art.models import Art, Like, Category, Tag, ArtTag
from registration.models import User, SecurityQuestion, SecurityAnswer
from user_profile.models import Profile

def create_user(username, password, email, first_name, last_name, is_artist=True, is_active=True):
    hashed_password = make_password(password)

    return User.objects.create(username=username,
                               password=hashed_password,
                               email=email,
                               first_name=first_name,
                               last_name=last_name,
                               is_active=is_active,
                               is_superuser=False,
                               is_staff=False,
                               is_artist=is_artist,
                               )

def create_category(name):
    return Category.objects.create(name=name)

def create_art(user_id, category, photo, title, description):
    return Art.objects.create(user_id=user_id,
                              category=category,
                              photo=photo,
                              title=title,
                              description=description
                              )

def create_tag(name):
    return Tag.objects.create(name=name)

def create_art_tag(art_id, tag_id):
    return ArtTag.objects.create(art_id=art_id, tag_id=tag_id)

def create_art_like(user_id, art_id):
    return Like.objects.create(
        user_id=user_id, art_id=art_id
    )

def create_user_profile(user_id, bio, twitter, photo):
    return Profile.objects.create(
        user_id=user_id, bio=bio, twitter=twitter, photo=photo
    )

def create_security_question(question):
    return SecurityQuestion(question=question)

def create_secret_answer(user_id, question_id, answer):
    return SecurityAnswer(
        user_id=user_id, security_questions_id=question_id, answer=answer
    )