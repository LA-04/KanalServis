from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from .models import kanalservis
from .serializer import kanalservis_serializer
from rest_framework.response import Response

# Create your views here.
# class kanalservis_view(APIView):
#     def get(self, request):
#         output = [
#             {
#                 "number": output.number,
#                 "order": output.order,
#                 "price_usd": output.price_usd,
#                 "price_rub": output.price_rub,
#                 "ord_date": output.ord_date
#             } for output in kanalservis.objects.all()
#         ]
#         return Response(output)
#
#     def post(self, request):
#         serializer = kanalservis_serializer(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             serializer.save()
#             return Response(serializer.data)

class kanalservis_view(generics.ListAPIView):
    queryset = kanalservis.objects.all()
    serializer_class = kanalservis_serializer



# class kanalservis_view(APIView):
#     def get(self, request):
#         queryset = kanalservis.objects.all()
#         serializer = kanalservis_serializer(queryset, many=True)
#         return Response(serializer.data)