from uuid import uuid4
from django.shortcuts import render
from rest_framework.views import Response
from rest_framework.views import APIView
from .models import Feed, Reply, Like, Bookmark
from instagram.settings import MEDIA_ROOT
from user.models import User
import os


# Create your views here.
class Main(APIView):
    def get(self, request):
        # select * from content_feed; 쿼리문과 같음, 데이터 양이 많을 경우 이건 위험한 코드. where 조건문을 같이 써야함
        # 최신순으로 데이터를 가져오기 위해 order_by() 사용, 아이디를 기준으로 역순.
        feed_object_list = Feed.objects.all().order_by("-id")
        feed_list = []

        # 이메일 데이터가 없을 경우, None 처리
        email = request.session.get("email", None)

        # 세션에 담겨있는 이메일을 읽어옴
        # print(f"로그인 이메일 : {email}")

        # 이메일 정보가 없으면 로그인창으로
        if email is None:
            return render(request, "user/login.html")

        user = User.objects.filter(email=email).first()

        # 유저정보가 없으면 로그인 창으로
        if user is None:
            return render(request, "user/login.html")

        for feed in feed_object_list:
            user = User.objects.filter(email=email).first()
            reply_object_list = Reply.objects.filter(feed_id=feed.id)
            reply_list = []

            for reply in reply_object_list:
                reply_user = User.objects.filter(email=reply.email).first()
                reply_list.append(
                    dict(
                        reply_content=reply.reply_content,
                        nickname=reply_user.nickname,
                    )
                )

            like_count = Like.objects.filter(feed_id=feed.id, is_like=True).count()

            is_liked = Like.objects.filter(
                feed_id=feed.id,
                email=email,
                is_like=True,
            ).exists()

            is_marked = Bookmark.objects.filter(
                feed_id=feed.id,
                email=email,
                is_marked=True,
            ).exists()

            feed_list.append(
                dict(
                    id=feed.id,
                    image=feed.image,
                    content=feed.content,
                    like_count=like_count,
                    reply_list=reply_list,
                    is_liked=is_liked,
                    is_marked=is_marked,
                    nickname=feed.nickname,
                    profile_image=feed.profile_image,
                )
            )

        return render(
            request,
            "instagram/main.html",
            context=dict(
                feeds=feed_list,
                user=user,
            ),
        )


class UploadView(APIView):
    def post(self, request):
        # 파일 불러오기
        file = request.FILES["file"]
        # 파일명에 한글이나 특수문자 등을 랜덤한 문자로 처리함
        uuid_name = uuid4().hex
        # 저장 경로 설정 - MEDIA_ROOT는 설정 파일에서 BASE_DIR(프로젝트 경로)에 'media'를 붙인 변수이며, 여기에 uuid_name을 붙여서
        # 최종적으로 프로젝트 경로/media/uuid_name의 경로로 파일이 저장될 것이다.
        save_path = os.path.join(MEDIA_ROOT, uuid_name)
        # 실제 파일이 저장되는 코드, 파일을 열어서 파일 청크를 for문을 통해 하나하나 저장해나간다.
        with open(save_path, "wb+") as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        image = uuid_name
        content = request.data.getlist("file")[1]
        email = request.session.get("email", None)

        user = User.objects.filter(email=email).first()

        profile_image = user.profile_image
        nickname = user.nickname

        Feed.objects.create(
            email=email,
            image=image,
            content=content,
            profile_image=profile_image,
            nickname=nickname,
        )

        return Response(status=200)


class Profile(APIView):
    def get(self, request):
        email = request.session.get("email", None)

        # 세션에 이메일 정보 없으면 로그인 페이지로 리다이렉트
        if email is None:
            return render(request, "user/login.html")

        user = User.objects.filter(email=email).first()

        # 유저정보가 존재하지 않아도 로그인 페이지로 리다이렉트
        if user is None:
            return render(request, "user/login.html")

        feed_list = Feed.objects.filter(email=email).all().order_by("-id")

        # values_list는 특정 데이터를 쿼리셋으로 추출할 수 있다.
        like_list = list(
            Like.objects.filter(email=email, is_like=True).values_list(
                "feed_id", flat=True
            )
        )

        # 쿼리셋 __in은 해당 데이터를 포함한 레코드만 추출할 수 있도록 한다.
        like_feed_list = Feed.objects.filter(id__in=like_list).order_by("-id")

        bookmark_list = list(
            Bookmark.objects.filter(email=email, is_marked=True).values_list(
                "feed_id", flat=True
            )
        )

        bookmark_feed_list = Feed.objects.filter(id__in=bookmark_list).order_by("-id")

        return render(
            request,
            "content/profile.html",
            context=dict(
                user=user,
                feed_list=feed_list,
                like_feed_list=like_feed_list,
                bookmark_feed_list=bookmark_feed_list,
            ),
        )


class UploadReply(APIView):
    def post(self, request):
        feed_id = request.data.get("feed_id", None)
        reply_content = request.data.get("reply_content", None)
        email = request.session.get("email", None)

        # 댓글 테이블 생성
        Reply.objects.create(
            feed_id=feed_id,
            reply_content=reply_content,
            email=email,
        )

        return Response(status=200)


class ToggelLike(APIView):
    def post(self, request):
        feed_id = request.data.get("feed_id", None)
        is_like = request.data.get("is_like", True)

        if is_like == "True" or is_like == "true":
            is_like = True
        else:
            is_like = False

        print(is_like)

        email = request.session.get("email", None)

        like = Like.objects.filter(feed_id=feed_id, email=email).first()

        if like:
            like.is_like = is_like
            like.save()
        else:
            # 댓글 테이블 생성
            Like.objects.create(
                feed_id=feed_id,
                is_like=is_like,
                email=email,
            )

        return Response(status=200)


class ToggelBookmark(APIView):
    def post(self, request):
        feed_id = request.data.get("feed_id", None)
        is_marked = request.data.get("is_marked", True)

        if is_marked == "True" or is_marked == "true":
            is_marked = True
        else:
            is_marked = False

        print(is_marked)

        email = request.session.get("email", None)

        bookmark = Bookmark.objects.filter(feed_id=feed_id, email=email).first()

        if bookmark:
            bookmark.is_marked = is_marked
            bookmark.save()
        else:
            # 댓글 테이블 생성
            Bookmark.objects.create(
                feed_id=feed_id,
                is_marked=is_marked,
                email=email,
            )

        return Response(status=200)
