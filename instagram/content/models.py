from django.db import models


# Create your models here.
class Feed(models.Model):
    content = models.TextField()  # 글내용
    image = models.TextField()  # 피드 이미지
    profile_image = models.TextField()  # 프로필 이미지
    user_id = models.TextField()  # 글쓴이
    like_count = models.IntegerField()  # 좋아요 수


# python manage.py makemigrations 명령어를 통해 models.py에 작성된 클래스를 데이터베이스를 위한 모델로 생성한다.
# python manage.py migrate 명령어로 생성된 모델을 실제 데이터베이스의 테이블로 작성한다. 이때 테이블명은 폴더명_클래스명이 된다.
