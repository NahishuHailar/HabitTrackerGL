def user_directory_path(instance, filename="profile"):
    """
    Upload user profile photo
    file will be uploaded to MEDIA_ROOT/users/user_<id>/<filename>
    """
    return f"users/{instance.id}/profile_photo/{filename}"
