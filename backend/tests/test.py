from fastapi.testclient import TestClient

from backend.main import app

client = TestClient(app)


# Make sure server is running
def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "Hello World"


# This should return an error since this account already exists
# Tests AuthHandler workflow
def test_sign_up():
    response = client.post(
        "/auth/signUp",
        json={
            "email": "saimm.ahmadd@gmail.com",
            "password": "",
            "firstName": "",
            "lastName": "",
        },
    )

    assert response.status_code == 409
    assert (
        response.json()["detail"] == "Account already exists for saimm.ahmadd@gmail.com"
    )


# Test logging into a fake account
# Tests AuthHandler workflow
def test_login():
    response = client.post(
        "/auth/login",
        data={
            "username": "test@gmail.com",
            "password": "test",
        },
        headers={"content-type": "application/x-www-form-urlencoded"},
    )

    assert response.status_code == 200
    assert response.json()["token_type"] == "bearer"
    assert "access_token" in response.json()


# Test getting user repositories
def test_get_repos():
    get_user_header = client.post(
        "/auth/login",
        data={
            "username": "test@gmail.com",
            "password": "test",
        },
        headers={"content-type": "application/x-www-form-urlencoded"},
    )

    assert get_user_header.json()["token_type"] == "bearer"
    print(get_user_header.json())
    token = get_user_header.json()["access_token"]

    repos = client.get(
        "/user/getAllRepos", headers={"Authorization": f"Bearer {token}"}
    )

    assert repos.status_code == 200
    assert len(repos.json()) == 0


# Ensures we can query a repository
def test_get_repo_info():
    repo = client.get("/user/getRepoInfo?repo_url=https://github.com/facebook/react")

    assert repo.status_code == 200
    assert repo.json()["name"] == "react"
