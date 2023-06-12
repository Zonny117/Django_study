from django.db import models

# python manage.py makemigrations 명령어를 통해 models.py에 작성된 클래스를 데이터베이스를 위한 모델로 생성한다.
# python manage.py migrate 명령어로 생성된 모델을 실제 데이터베이스의 테이블로 작성한다. 이때 테이블명을 지정하지 않으면 폴더명_클래스명이 된다.


# 피드 게시물 모델
class Feed(models.Model):
    content = models.TextField()  # 글내용
    image = models.TextField()  # 피드 이미지
    email = models.EmailField(default="")  # 이메일
    like_count = models.IntegerField()  # 좋아요 수


# 좋아요 모델
class Like(models.Model):
    feed_id = models.IntegerField(default=0)
    email = models.EmailField(default="")
    is_like = models.BooleanField(default=True)


# 댓글 모델
class Reply(models.Model):
    feed_id = models.IntegerField(default=0)
    email = models.EmailField(default="")
    reply_content = models.TextField()


# 북마크
class Bookmark(models.Model):
    feed_id = models.IntegerField(default=0)
    email = models.EmailField(default="")
    is_marked = models.BooleanField(default=True)
