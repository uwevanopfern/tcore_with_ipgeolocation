import pytest

from django.contrib.auth.models import User
from social_app.models import Post, Like
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken


@pytest.fixture(scope="function")
def signup():
    def _signup():
        user = User(
            username="uwe",
            email="uweaime@yahoo.com",
            is_active=True,
            is_staff=True,
            is_superuser=True,
        )
        user.set_password("kigali")
        user.save()
        return user

    return _signup

@pytest.fixture
def authenticate_user():
    user = User(
        username="van",
        email="van@yahoo.com",
        is_active=True,
        is_staff=True,
        is_superuser=True,
    )
    user.set_password("kigali")
    user.save()
    client = APIClient()
    refresh = RefreshToken.for_user(user)
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")

    return client
