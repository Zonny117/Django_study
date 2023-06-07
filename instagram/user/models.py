from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser

# Create your models here.


# 커스텀 사용자 모델
# 장고에는 기본적으로 사용자 모델이 포함되어 있다. 따라서 AbstractBaseUser를 상속받아 사용자 모델을 커스텀화하여 사용하면,
# 기존 사용자 모델에 있던 관련 메소드 등도 사용할 수 있다.
class User(AbstractBaseUser):
    profile_image = models.TextField()  # 프로필 사진
    nickname = models.CharField(max_length=24, unique=True)  # 닉네임
    name = models.CharField(max_length=24)  # 이름
    email = models.EmailField(unique=True)

    USERNAME_FIELD = "nickname"

    class Meta:
        db_table = "User"
