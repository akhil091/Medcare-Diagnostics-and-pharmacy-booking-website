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
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
import json
import re
from .models import Specialization,Condition, Doctor, AllBooking
from .serializers import DoctorSerializer,SpecializationSerializer,ConditionSerializer
from rest_framework.renderers import TemplateHTMLRenderer


def doctorpage(request):
    speciality = Specialization.objects.all()
    condition = Condition.objects.all()
    doc = Doctor.objects.all()
    Doctor.objects.all()
    context={'speciality':speciality, 'condition':condition, 'doc':doc}
    return render(request,'doctors.html',context)

class SpecializationView(APIView):

    def get(self,request):
        serializer = SpecializationSerializer(Specialization.objects.all(),many=True)
        return Response(serializer.data)

    def post(self,request,*args, **kwargs):
        pk = request.data.get('pk',None)
        if pk is None:
            return Response({'message': "Invalid Request"},status=status.HTTP_400_BAD_REQUEST)

        return Response(DoctorSerializer(Doctor.objects.filter(Specialization=pk),many=True).data)

class ConditionView(APIView):

    def get(self,request):
        serializer = ConditionSerializer(Condition.objects.all(),many=True)
        return Response(serializer.data)

    def post(self,request,*args, **kwargs):
        pk = request.data.get('pk',None)
        if pk is None:
            return Response({'message': "Invalid Request"},status=status.HTTP_400_BAD_REQUEST)
        serializer =  DoctorSerializer(Doctor.objects.filter(Condition=pk), many=True)
        return Response(serializer.data)

def doctorprofile(request,id):
    product = Doctor.objects.filter(id=id)
    return render(request, 'doctordetails.html', {'product':product[0]})

def conditiondoctors(request,id):
    cond = Condition.objects.filter(id=id)
    return render(request, 'conditiondoctors.html', {'cond':cond[0]})

def specialitydoctors(request,id):
    specialz = Specialization.objects.filter(id=id)
    return render(request, 'specialitydoctors.html', {'specialz':specialz[0]})

class GetDoctorView(generics.RetrieveAPIView):



    # def post(self, request, *args, **kwargs):
    #     pk = request.data.get('id',None)
    #     if pk is None:
    #         return Response({"Message" : "Enter ID"},status=status.HTTP_400_BAD_REQUEST)
    #     if Doctor.objects.filter(id=pk).exists == False:
    #         return Response({"Message" : "Doctor with this ID Doesn't exists"},status=status.HTTP_400_BAD_REQUEST)
    #     return Response(DoctorSerializer(Doctor.objects.filter(id=pk),many=True).data)
    def get(self, request, *args, **kwargs):
        pk = kwargs.get("id")
        obj = get_object_or_404(Doctor, id=pk)
        return Response(DoctorSerializer(obj).data)


class DoctorDetialView(APIView):

    def check(self, reg, value):
        if re.fullmatch(reg,value):
            return False
        else:
            return True

    def get(self,request):
        serializer = DoctorSerializer(Doctor.objects.all(),many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        date = request.data.get('date',None)
        id  = request.data.get('id',None)

        First_Name = request.data.get('First_Name',None)
        Last_Name = request.data.get('Last_Name',None)
        Age = request.data.get('Age',None)
        Phone = request.data.get('Phone',None)
        Email = request.data.get('Email',None)

        phone_re = re.compile(r"[0-9]{10}")
        email_re = re.compile(r"[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}")
        age_re = re.compile(r"[0-9]{1,2}")
        print("------------------",date)
        if First_Name is None:
            return Response({"Message" : "Enter First Name"})
        if Last_Name is None:
            return Response({"Message" : "Enter Last Name"})
        if Age is None:
            return Response({"Message" : "Enter Age"})
        if self.check(age_re,Age):
            return Response({"Message" : "Enter Valid Age"})
        if Phone is None:
            return Response({"Message" : "Enter Phone"})
        elif self.check(phone_re,Phone):
            return Response({"Message" : "Enter Valid Phone"})
        if Email is None:
            return Response({"Message" : "Enter Email"})
        elif self.check(email_re,Email):
            return Response({"Message" : "Enter Valid Email"})

        if date is None and id is None:
            return Response({"Message" : "Field is not given"})

        doc_obj = Doctor.objects.get(id=id)

        AllBooking.objects.create(Doctor=doc_obj,First_Name=First_Name, Last_Name=Last_Name, Age=Age, Phone=Phone,Email=Email, Fee=doc_obj.Fee,User=self.request.user,Date=date)
        return Response({"Message" : "Request Submitted"})

class Doc_FilterView(APIView):

    def post(self,request,*args, **kwargs):

        a_z = request.data.get('a_z',False)
        z_a = request.data.get('z_a',False)
        l_h = request.data.get('l_h',False)
        h_l = request.data.get('h_l',False)

        if a_z:
            return Response(DoctorSerializer(Doctor.objects.all().order_by("Name"),many=True).data)
        if z_a:
            return Response(DoctorSerializer(Doctor.objects.all().order_by("-Name"),many=True).data)
        if l_h:
            return Response(DoctorSerializer(Doctor.objects.all().order_by("Fee"),many=True).data)
        if h_l:
            return Response(DoctorSerializer(Doctor.objects.all().order_by("-Fee"),many=True).data)

