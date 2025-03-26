from django.shortcuts import render
from rest_framework.decorators import api_view,authentication_classes,permission_classes
from rest_framework.permissions import IsAuthenticated,AllowAny,IsAdminUser
from rest_framework import permissions
from .models import *
from rest_framework.response import Response
from oauth2_provider.contrib.rest_framework.authentication import OAuth2Authentication
from .serializers import *
from rest_framework import status
# Create your views here.
# @api_view(['POST'])
# @authentication_classes([OAuth2Authentication])
# @permission_classes([IsAuthenticated])
# def Createcompany(request):
#     comp = Rdb()
#     comp.names = request.data['names']
#     comp.tin_number = request.data['tin_number']
#     comp.save()
#     return Response(comp) 
@api_view(['POST'])
@authentication_classes([OAuth2Authentication])
@permission_classes([IsAuthenticated])
def Createcompany(request):
    serializer = RdbSerializer(data=request.data)

    if serializer.is_valid():
       serializer.save()
       return Response(serializer.data,status=status.HTTP_201_CREATED)
    else:
        return Response({'msg':serializer.errors},status=status.HTTP_400_BAD_REQUEST )
# @api_view(['POST'])
# @authentication_classes([OAuth2Authentication])
# @permission_classes([IsAuthenticated])
# def Industry_check(request):
#     industry = Industry()
#     c = Rdb.objects.all()
#     b=RdbSerializer(c , many=True)
#     print(b)
#     industry.owner_name = request.data['owner_name']
#     industry.Brand_name = request.data['Brand_name']
#     industry.physical_address = request.data['physical_address']
#     industry.Phone = request.data['Phone']
#     industry.email = request.data['email']
#     if b.data.company_name !=industry.Brand_name:
#        return Response({"msg":"not in databse"})
#     # return Response(b.data)