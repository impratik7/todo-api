import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app, get_db
from app.database import Base
from app.schemas import UserCreate, TaskCreate

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="module")
def client():
    return TestClient(app)

@pytest.fixture(scope="module", autouse=True)
def setup_database():
    # Drop and recreate the database schema before running tests
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    # Optionally drop the schema after tests are done
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="module")
def token(client: TestClient):
    # Register the user
    response = client.post(
        "/register",
        json={"username": "user_test_2", "password": "pass_test_2"}
    )
    print(f"Register response status code: {response.status_code}")
    print(f"Register response content: {response.json()}")
    assert response.status_code == 200, f"Register failed: {response.json()}"
    
    # Log in to get the token
    response = client.post(
        "/token",
        data={"username": "user_test_2", "password": "pass_test_2"}
    )
    print(f"Login response status code: {response.status_code}")
    print(f"Login response content: {response.json()}")
    assert response.status_code == 200, f"Login failed: {response.json()}"
    
    token = response.json()["access_token"]
    print(f"Generated token: {token}")  # Debug output
    return token
