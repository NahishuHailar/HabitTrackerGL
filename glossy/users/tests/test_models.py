import pytest
from users.models import User, UserAvatar, AvatarGroup


@pytest.mark.django_db
def test_create_user():
    user = User.objects.create(
        username='testuser',
        email='testuser@example.com',
        phone=1234567890,
        firebase_key='firebase_key_value',
        fcm_key='fcm_key_value'
    )
    
    assert user.username == 'testuser'
    assert user.email == 'testuser@example.com'
    assert user.phone == 1234567890
    assert user.firebase_key == 'firebase_key_value'
    assert user.fcm_key == 'fcm_key_value'

@pytest.mark.django_db
def test_user_str_method():
    user = User.objects.create(username='testuser')
    assert str(user) == 'testuser'

    user_without_name = User.objects.create(username=None)
    assert str(user_without_name) == "Name isn't set"


@pytest.mark.django_db
def test_create_avatar_group():
    avatar_group = AvatarGroup.objects.create(
        name="Group A",
        product_id="product_123"
    )
    assert avatar_group.name == "Group A"
    assert avatar_group.product_id == "product_123"


@pytest.mark.django_db
def test_create_user_avatar():
    avatar_group = AvatarGroup.objects.create(
        name="Group B",
        product_id="product_456"
    )
    
    user_avatar = UserAvatar.objects.create(
        title="Avatar 1",
        product_id="avatar_001",
        avatar_group=avatar_group,
        image_url="http://example.com/avatar1.png",
        color="green",
        paid=True,
    )
    
    assert user_avatar.title == "Avatar 1"
    assert user_avatar.product_id == "avatar_001"
    assert user_avatar.avatar_group == avatar_group
    assert user_avatar.image_url == "http://example.com/avatar1.png"
    assert user_avatar.color == "green"
    assert user_avatar.paid is True