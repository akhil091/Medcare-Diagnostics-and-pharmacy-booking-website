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
from contact.models import Messages

class ContactView(APIView):

    def post(self,request,*args, **kwargs):
        name = request.data.get("Name",None)
        email = request.data.get("Email",None)
        contact = request.data.get("Contact",None)
        subject = request.data.get("Subject",None)
        message = request.data.get("Message",None)

        Messages.objects.create(Name=name,Email=email,Contact=contact,Subject=subject,Message=message)
        return Response({"Message" : "Thank You!! Your response is recorded"},status=status.HTTP_200_OK)
