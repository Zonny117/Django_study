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

            feed_list.append(
                dict(
                    id=feed.id,
                    image=feed.image,
                    content=feed.content,
                    like_count=feed.like_count,
                    reply_list=reply_list,
                    nickname=user.nickname,  # user에서 받아와서 새로고침하면 피드 프로필이 변경됨 에러의심
                    profile_image=user.profile_image,  # user에서 받아와서 새로고침하면 피드 프로필이 변경됨 에러의심
                    # 피드 업로드할때 세션 이메일과 매칭되는 유저의 닉네임과 프로필사진도 레코드로 추가해서 db에 저장해야할듯 싶다.
                )
            )

        # 세션에 담겨있는 이메일을 읽어옴
        # print(f"로그인 이메일 : {email}")

        # 이메일 정보가 없으면 로그인창으로
        if email is None:
            return render(request, "user/login.html")

        user = User.objects.filter(email=email).first()

        # 유저정보가 없으면 로그인 창으로
        if user is None:
            return render(request, "user/login.html")

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

        Feed.objects.create(
            email=email,
            image=image,
            content=content,
            like_count=0,
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

        return render(
            request,
            "content/profile.html",
            context=dict(
                user=user,
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
