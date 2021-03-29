from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.utils import timezone
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import (
    ListAPIView, RetrieveAPIView, CreateAPIView,
    UpdateAPIView, DestroyAPIView
)
from datetime import datetime
from rest_framework.permissions import IsAuthenticated
import json
import re
import time
from time import time,ctime
from django.utils import timezone
from Medicine.models import Medicines

class MedicineView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self,request,*args, **kwargs):
        name = request.data.get("Name",None)
        phone = request.data.get("Phone",None)
        Prescription_File = request.FILES['Prescription_File']
        address = request.data.get("Address",None)
        Other_Detail = request.data.get("Other_Detail",None)

        Medicines.objects.create(Name=name,Phone=phone,Prescription_File=Prescription_File,Address=address,Other_Detail=Other_Detail)
        return Response({"Message" : "You response is recorded"},status=status.HTTP_200_OK)
