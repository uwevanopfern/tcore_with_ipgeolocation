import pytest
from django.contrib.auth.models import User


@pytest.mark.django_db
def test_signup(client):
    data = {
        "username": "Van",
        "email": "uweaime@gmail.com",
        "first_name": "Uwe",
        "last_name": "Van",
        "password": "kigali",
    }

    headers = {"content-type": "application/json"}
    res = client.post(f"/api/v1/signup/", data=data, headers=headers)
    assert res.status_code == 201
    assert res.data["username"] == "Van"


@pytest.mark.django_db
def test_login(client, signup):

    user = signup()

    credentials = {
        "username": user.username,
        "password": "kigali",
    }

    headers = {"content-type": "application/json"}

    res = client.post(f"/login/v1/", data=credentials, headers=headers)
    assert res.status_code == 200


@pytest.mark.django_db
def test_add_post(client, authenticate_user, signup):
    user = signup()
    data = {
        "user": user,
        "title": "Task for Python Engineer role @TradeCore",
        "content": "Objective of this task is to create a simple REST API based social network in Django",
    }
    res = authenticate_user.post(f"/api/v1/posts/", data=data)
    assert res.status_code == 201


@pytest.mark.django_db
def test_get_posts(client, authenticate_user):
    res = authenticate_user.get(f"/api/v1/posts/")
    assert res.status_code == 200


@pytest.mark.django_db
def test_get_post(client, authenticate_user, signup):

    user = signup()
    data = {
        "user": user,
        "title": "Task for Python Engineer role @TradeCore",
        "content": "Objective of this task is to create a simple REST API based social network in Django",
    }
    res = authenticate_user.post(f"/api/v1/posts/", data=data)
    id = res.data["id"]

    res = authenticate_user.get(f"/api/v1/posts/{id}")
    assert res.status_code == 200


@pytest.mark.django_db
def test_update_post(client, authenticate_user, signup):
    user = signup()
    data = {
        "user": user,
        "title": "Task for Python Engineer role @TradeCore",
        "content": "Objective of this task is to create a simple REST API based social network in Django",
    }
    res = authenticate_user.post(f"/api/v1/posts/", data=data)
    id = res.data["id"]

    updated_params = {
        "user": user,
        "title": "Task for Python Engineer role @TradeCore, UPDATED",
        "content": "Objective of this task is to create a simple REST API based social network in Django, UPDATED",
    }

    res = authenticate_user.put(f"/api/v1/posts/{id}", data=updated_params)
    assert res.status_code == 200


@pytest.mark.django_db
def test_delete_post(client, authenticate_user, signup):
    user = signup()
    data = {
        "user": user,
        "title": "Task for Python Engineer role @TradeCore",
        "content": "Objective of this task is to create a simple REST API based social network in Django",
    }
    res = authenticate_user.post(f"/api/v1/posts/", data=data)
    id = res.data["id"]

    res = authenticate_user.delete(f"/api/v1/posts/{id}")
    assert res.status_code == 204


@pytest.mark.django_db
def test_add_like(client, authenticate_user, signup):
    user = signup()
    data = {
        "user": user,
        "title": "Task for Python Engineer role @TradeCore",
        "content": "Objective of this task is to create a simple REST API based social network in Django",
    }
    res = authenticate_user.post(f"/api/v1/posts/", data=data)
    id = res.data["id"]

    like_params = {"post": id, "user": user}

    res = authenticate_user.post(f"/api/v1/likes/", data=like_params)
    assert res.status_code == 201


@pytest.mark.django_db
def test_unlike_post(client, authenticate_user, signup):
    user = signup()
    data = {
        "user": user,
        "title": "Task for Python Engineer role @TradeCore",
        "content": "Objective of this task is to create a simple REST API based social network in Django",
    }
    res = authenticate_user.post(f"/api/v1/posts/", data=data)
    id = res.data["id"]

    like_params = {"post": id, "user": user}

    like_res = authenticate_user.post(f"/api/v1/likes/", data=like_params)
    like_id = like_res.data["id"]
    unlike_res = authenticate_user.delete(f"/api/v1/unlike/{like_id}")
    assert unlike_res.status_code == 204


@pytest.mark.django_db
def test_get_user_data(client, authenticate_user):
    res = authenticate_user.get(f"/api/v1/user/data/")
    assert res.status_code == 200
