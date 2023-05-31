from django.shortcuts import render
from rest_framework.views import APIView
from .models import Feed


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
