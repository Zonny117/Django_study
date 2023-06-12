import os
from uuid import uuid4
from django.shortcuts import render
from rest_framework.views import APIView, Response
from content.models import Feed
from instagram.settings import MEDIA_ROOT
from .models import User
from django.contrib.auth.hashers import make_password


# Create your views here.
class Join(APIView):
    def get(self, request):
        return render(request, "user/join.html")

    # 회원가입
    def post(self, request):
        email = request.data.get("email", None)
        nickname = request.data.get("nickname", None)
        name = request.data.get("name", None)
        password = request.data.get("password", None)

        # 유저 테이블 레코드 생성
        # 비밀번호의 경우, 암호화 처리를 하여 db에 저장해야한다.
        # 복호화가 불가능한 단뱡향으로 암호화한다.
        User.objects.create(
            email=email,
            nickname=nickname,
            name=name,
            password=make_password(password),
            profile_image="default_profile.jpg",
        )

        return Response(status=200)


class Login(APIView):
    def get(self, request):
        return render(request, "user/login.html")

    # 로그인
    def post(self, request):
        email = request.data.get("email", None)
        password = request.data.get("password", None)

        # filter는 SQL문의 WHERE의 역할을 한다.
        # first 메소드를 사용한 이유는 db에서 데이터를 읽어올 경우 쿼리셋으로 받게 되는데,
        # 일종의 list 자료와 같다. 따라서 추출한 데이터의 첫번째 것만 받아서
        # 변수에 지정할 경우, 해당 변수는 객체로 활용할 수 있다.
        user = User.objects.filter(email=email).first()

        if user is None:
            return Response(
                status=400,
                # 실제론 db상 존재하지 않는 계정이지만, 계정이 없다고 알려줄 경우,
                # 해커가 계정 정보가 없다는 사실을 알 수 있고, 이를 악용할 여지가 있으므로,
                # 계정 정보가 오타가 나든, 존재하지 않던간에 똑같은 메세지로 처리하는 것이 바람직하다.
                data=dict(message="이메일 혹은 비밀번호를 확인해주세요."),
            )

        if user.check_password(password):
            # 로그인 성공, 세션 혹은 쿠키에 저장
            request.session["email"] = email

            return Response(status=200)
        else:
            return Response(status=400, data=dict(message="이메일 혹은 비밀번호를 확인해주세요."))


class Logout(APIView):
    def get(self, request):
        request.session.flush()
        return render(request, "user/login.html")


class UploadProfileImage(APIView):
    def post(self, request):
        file = request.FILES["file"]
        uuid_name = uuid4().hex
        save_path = os.path.join(MEDIA_ROOT, uuid_name)
        with open(save_path, "wb+") as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        profile_image = uuid_name
        email = request.data.get("email")

        user = User.objects.filter(email=email).first()

        # 테이블 업데이트시 세이브 메소드를 실행시켜줘야 데이터베이스에 최종 반영된다.
        user.profile_image = profile_image
        user.save()

        return Response(status=200)
