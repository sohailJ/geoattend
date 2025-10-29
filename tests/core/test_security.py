from geoattend.core.security import get_password_hash, verify_password


def test_password_hashing():
    # Arrange
    password = "MySuperSecretPassword123"

    # Act
    hashed_password = get_password_hash(password)

    # Assert
    assert hashed_password != password
    assert verify_password(password, hashed_password)
    assert not verify_password("WrongPassword", hashed_password)
