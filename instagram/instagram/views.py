from rest_framework.views import APIView
from django.shortcuts import render

class Sub(APIView):
    def get(self, request):
        print("get 호출")
        return render(request, "instagram/main.html")
    
    def post(self, request):
        print("post 호출")
        return render(request, "instagram/main.html")