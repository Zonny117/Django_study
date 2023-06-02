from uuid import uuid4
from django.shortcuts import render
from rest_framework.views import Response
from rest_framework.views import APIView
from .models import Feed
from instagram.settings import MEDIA_ROOT
import os


# Create your views here.
class Main(APIView):
    def get(self, request):
        # select * from content_feed; 쿼리문과 같음, 데이터 양이 많을 경우 이건 위험한 코드. where 조건문을 같이 써야함
        # 최신순으로 데이터를 가져오기 위해 order_by() 사용, 아이디를 기준으로 역순.
        feed_list = Feed.objects.all().order_by("-id")

        return render(
            request,
            "instagram/main.html",
            context=dict(feeds=feed_list),
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
        user_id = request.data.getlist("file")[2]
        profile_image = request.data.getlist("file")[3]

        Feed.objects.create(
            profile_image=profile_image,
            user_id=user_id,
            image=image,
            content=content,
            like_count=0,
        )

        return Response(status=200)
