from django.shortcuts import render
from rest_framework.views import APIView, Response
import openpyxl


class Main(APIView):
    def get(self, request):
        return render(request, "upload/index.html")


class Upload(APIView):
    def post(self, request):
        file = request.FILES["file"]

        excel = openpyxl.load_workbook(file, data_only=True)
        work_sheet = excel.worksheets[0]

        all_values = []
        for row in work_sheet.rows:
            row_value = []
            for cell in row:
                row_value.append(cell.value)
            print(row_value)
            all_values.append(row_value)

        return Response(status=200)
