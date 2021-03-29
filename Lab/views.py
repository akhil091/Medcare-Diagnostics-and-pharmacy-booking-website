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
from Doctors.models import Specialization, Doctor, Condition
from All_Users.otp import generate_otp, update_otp, get_otp
from Lab.models import NotSure,Tests,HealthPackage, Cart, Order, Address, ZipCode
from Lab.serializers import TestsSerializer, HealthPackageSerializer, ConditionSerializer, CartSerializer, OrderSerializers, AddressSerializers

def home(request):
    testitem = Tests.objects.all()
    hlthpkgitem = HealthPackage.objects.all()
    speciality = Specialization.objects.all()
    condition = Condition.objects.all()
    doc = Doctor.objects.all()
    context={ 'testitem':testitem, 'hlthpkgitem':hlthpkgitem,'speciality':speciality, 'condition':condition, 'doc':doc}
    return render(request, 'index.html',context)



def testprofile(request,id):
    testitem = Tests.objects.filter(id=id)
    return render(request, 'testdetails.html', {'testitem':testitem[0]})

def hlthpkgprofile(request,id):
    hlthpkgitem = HealthPackage.objects.filter(id=id)
    return render(request, 'hlthpkgdetails.html', {'hlthpkgitem':hlthpkgitem[0]})

class ConditionView(APIView):

    def get(self,request):
        return Response(ConditionSerializer(Condition.objects.all()).data)

class NotSureView(APIView):

    def post(self, request, *args, **kwargs):
        first_name = request.data.get('first',None)
        last_name = request.data.get('last',None)
        pincode = request.data.get('pin',None)
        prescription = request.FILES['prescription']
        phone = request.data.get('phone',None)
        send_otp = request.data.get('send_otp',None)
        otp = request.data.get('otp',None)

        if first_name is None and last_name is None and pincode is None and phone is None and send_otp is None:
            return Response({'message':"Some Fields are missing"},status=status.HTTP_404_NOT_FOUND)
        flag = bool(re.match('[\d]{10}', phone))
        if send_otp == True:
            if flag == False:
                return Response({'message': "Invalid Mobile Number"},status=status.HTTP_400_BAD_REQUEST)

            get_otp = generate_otp(phone)
            print(get_otp)
            if get_otp == '-1':
                return Response({'message': "Failed to send OTP"},status=status.HTTP_400_BAD_REQUEST)
            NotSure.objects.create(first_name=first_name,last_name=last_name,pincode=pincode,prescription=prescription,mobile=phone,otp=get_otp)
            return Response({'message': "OTP Send Successfully"},status=status.HTTP_200_OK)
        else:
            if otp is None:
                return Response({'message':"Enter OTP"},status=status.HTTP_404_NOT_FOUND)
            else:
                notsure_obj = NotSure.objects.filter(first_name=first_name,last_name=last_name,mobile=phone).order_by('-id')
                if notsure_obj.exists():
                    notsure_obj_recent = notsure_obj[0]
                    if notsure_obj_recent.otp == otp:
                        notsure_obj_recent.valid = True
                        notsure_obj_recent.save()
                        return Response({'message':"OTP Matched"},status=status.HTTP_200_OK)
                    else:
                        return Response({'message':"Invalid OTP"},status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({'message':"Enter Details"},status=status.HTTP_400_BAD_REQUEST)
            return Response({'message': "ERROR"},status=status.HTTP_400_BAD_REQUEST)

class GetTestView(APIView):

    def post(self, request, *args, **kwargs):
        a_z = request.data.get('a_z',False)
        z_a = request.data.get('z_a',False)
        l_h = request.data.get('l_h',False)
        h_l = request.data.get('h_l',False)

        test = request.data.get('test',False)
        package = request.data.get('package',False)
        condition = request.data.get('condition',None)

        test_obj = Tests.objects.all()
        package_obj = HealthPackage.objects.all()

        if condition is not None:
            if test:
                test_obj = test_obj.filter(conditions=condition)
            if package:
                package_obj = package_obj.filter(conditions=condition)


        if test:
            if condition is not None:
                try:
                    test_obj = test_obj.filter(conditions=condition)
                except:
                    pass
            if a_z:
                test_obj = test_obj.order_by("Name")
            elif z_a:
                test_obj = test_obj.order_by("-Name")
            if l_h:
                test_obj = test_obj.order_by("Discount_Price")
            elif h_l:
                test_obj = test_obj.order_by("-Discount_Price")
            return Response(TestsSerializer(test_obj,many=True).data)

        if package:
            if condition is not None:
                try:
                    package_obj = package_obj.filter(conditions=condition)
                except:
                    pass
            if a_z:
                package_obj = package_obj.order_by("Name")
            elif z_a:
                package_obj = package_obj.order_by("-Name")
            if l_h:
                package_obj = package_obj.order_by("Discount_Price")
            elif h_l:
                package_obj = package_obj.order_by("-Discount_Price")
            return Response(HealthPackageSerializer(package_obj,many=True).data)
        return Response({'message': "ERROR"},status=status.HTTP_400_BAD_REQUEST)

class TestAPI(APIView):

    def get(self, request, *args, **kwargs):
        type = kwargs.get("type")
        if type == "test":
            obj = get_object_or_404(Tests, pk=kwargs.get("pk"))
            return Response(TestsSerializer(obj).data)
        else:
            obj = get_object_or_404(HealthPackage, pk=kwargs.get("pk"))
            return Response(HealthPackageSerializer(obj).data)
"""
@api_view(['GET'])
def TestView(request, pk,format=None):

    try:
        test_obj = Tests.objects.get(pk=pk)
    except Tests.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        return Response(TestsSerializer(test_obj).data)
"""

class add_to_cart(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self,request,*args, **kwargs):
        id = request.data.get('id',None)
        single_test = request.data.get('test',None)

        if id is None:
            return Response({'message': "Invalid Request"},status=status.HTTP_400_BAD_REQUEST)

        if single_test:
            lab_test = get_object_or_404(Tests,id=id)
            cart_obj, created = Cart.objects.get_or_create(Patient=self.request.user,Test = lab_test)
            order_qs = Order.objects.filter(Patient=self.request.user,Ordered=False)
            if order_qs.exists():
                order_qs = order_qs[0]
                print(cart_obj)
                if order_qs.Tests.filter(Test__id = id).exists():
                    return Response({'message': "Already Ordered"},status=status.HTTP_200_OK)
                else:
                    order_qs.Tests.add(cart_obj)
                    order_qs.total_amount = order_qs.get_total()
                    order_qs.save()
                    return Response({'message': "Added"},status=status.HTTP_200_OK)
            else:
                ordered_date = timezone.now()

                order = Order.objects.create(Patient = request.user,Ordered_Date=ordered_date,service_status="Incart")

                order.Tests.add(cart_obj)
                order.total_amount = order.get_total()
                order.save()
                return Response({'message': "Added"},status=status.HTTP_200_OK)
        else:
            lab_test = get_object_or_404(HealthPackage,id=id)
            cart_obj, created = Cart.objects.get_or_create(Patient=self.request.user, Package = lab_test,Ordered=False)
            order_qs = Order.objects.filter(Patient=self.request.user,Ordered=False)
            if order_qs.exists():
                order_qs = order_qs[0]
                if order_qs.Packages.filter(Package__id = id).exists():
                    return Response({'message': "Already Ordered"},status=status.HTTP_200_OK)
                else:
                    order_qs.Packages.add(cart_obj)
                    order_qs.total_amount = order_qs.get_total()
                    order_qs.save()
                    return Response({'message': "Added"},status=status.HTTP_200_OK)
            else:
                ordered_date = timezone.now()
                order = Order.objects.create(Patient = request.user,Ordered_Date=ordered_date)
                order.Packages.add(cart_obj)
                order.total_amount = order.get_total()
                order.save()
                return Response({'message': "Added"},status=status.HTTP_200_OK)

class remove_from_cart(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request,*args, **kwargs):
        id = request.data.get('id',None)
        # single_test = request.data.get('test',None)

        if id is None:
            return Response({'message': "Invalid Request"},status=status.HTTP_400_BAD_REQUEST)
        cart_obj = Cart.objects.get(id=id)
        if cart_obj.Test is not None:
            id = cart_obj.Test.id

            lab_test = get_object_or_404(Tests,id=id)
            order_qs = Order.objects.filter(Patient=self.request.user,Ordered=False)
            if order_qs.exists():
                order_qs = order_qs[0]
                if order_qs.Tests.filter(Test__id = id).exists():
                    order_service = Cart.objects.filter(Test=id,Patient=self.request.user,Ordered=False)[0]
                    order_qs.Tests.remove(order_service)
                    order_service.delete()
                    if len(Cart.objects.all()) == 0:
                        order_qs.delete()
                    return Response({'message': "Item Removed"},status=status.HTTP_200_OK)
                else:
                    return Response({'message': "Nothing to remove"},status=status.HTTP_200_OK)
            else:
                return Response({'message': "Don't have any active order"},status=status.HTTP_200_OK)
        else:
            id = cart_obj.Package.id
            lab_test = get_object_or_404(Tests,id=id)
            order_qs = Order.objects.filter(Patient=self.request.user,Ordered=False)
            if order_qs.exists():
                order_qs = order_qs[0]
                if order_qs.Packages.filter(Package__id = id).exists():
                    order_service = Cart.objects.filter(Package__id=id,Patient=self.request.user,Ordered=False)[0]
                    order_qs.Tests.remove(order_service)
                    order_service.delete()
                    if len(Cart.objects.all()) == 0:
                        order_qs.delete()
                    return Response({'message': "Item Removed"},status=status.HTTP_200_OK)
                else:
                    return Response({'message': "Nothing to remove"},status=status.HTTP_200_OK)
            else:
                return Response({'message': "Don't have any active order"},status=status.HTTP_200_OK)

class CartView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self,request):
        cart_res = CartSerializer(Cart.objects.filter(Patient=self.request.user,Ordered=False),many=True).data
        if len(cart_res) == 0:
            return Response({"Message":"Cart is Empty"})
        return Response(cart_res)

    def post(self,request,*args, **kwargs):
        id = request.data.get("id",None)
        date = request.data.get("date",None)
        obj = get_object_or_404(Cart,id=id)
        obj.when = date
        obj.save()
        return Response({"Message" : "Time is fixed"},status=status.HTTP_201_CREATED)

class OrderView(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            order = Order.objects.get(Patient=self.request.user,Ordered=False)
            order.total_amount = order.get_total()
            order.save()
            return Response(OrderSerializers(order).data)
        except:
            return Response({'Message' : "You don't have any order"})

    def post(self,request,*args, **kwargs):
        date = request.data.get("date",None)
        obj = Order.objects.get(Patient=self.request.user,Ordered=False)
        obj.when = date
        obj.save()
        return Response({"Message" : "Time is fixed"},status=status.HTTP_201_CREATED)

class AddressView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request, *args, **kwargs):
        First_Name = request.data.get('First_Name',None)
        Last_Name = request.data.get('Last_Name',None)
        Address1 = request.data.get('Address',None)
        Landmark = request.data.get('Landmark',None)
        Extra = request.data.get('Extra',None)
        Phone = request.data.get('Phone',None)
        PinCode = request.data.get('PinCode',None)
        default = request.data.get('default',False)
        secondary_address = request.data.get('secondary_address',False)

        use_default = request.data.get('use_default',False)
        use_secondary_address = request.data.get('use_secondary_address',False)
        print("----",PinCode," ",len(PinCode))

        if use_default:

            order = Order.objects.get(Patient=self.request.user,Ordered=False)
            address_qs = Address.objects.get(Patient=self.request.user,default=True)

            order.shipping_address = address_qs
            order.Delivery_Charges = ZipCode.objects.get(PinCode=address_qs.PinCode).Charges
            order.save()
            return Response({"message" : "Default Address is Applicated"},status=status.HTTP_200_OK)

        if use_secondary_address:

            order = Order.objects.get(Patient=self.request.user,Ordered=False)
            address_qs = Address.objects.get(Patient=self.request.user,secondary_address=True)

            order.shipping_address = address_qs
            order.Delivery_Charges = ZipCode.objects.get(PinCode=address_qs.PinCode).Charges
            order.save()
            return Response({"message" : "Secondary Address is Applicated"},status=status.HTTP_200_OK)

        # if bool(re.match('[\d]{6}', PinCode)) or False:
        #     return Response({'Message' : "Enter Valid Pincode"}, status=status.HTTP_406_NOT_ACCEPTABLE)

        # if ZipCode.objects.filter(PinCode=PinCode).exists() or False:
        #     return Response({'Message' : "We Don't Deliver here. Please contact us"})


        if default:
            if Address.objects.filter(Patient=self.request.user,default=True).exists():
                address_obj = Address.objects.get(Patient=self.request.user,default=True)
                address_obj.default = False
                address_obj.save()
                address_created = Address.objects.create(
                    Patient = self.request.user,
                    First_Name = First_Name,
                    Last_Name  = Last_Name,
                    Address = Address1,
                    Landmark = Landmark,
                    Extra = Extra,
                    Phone = Phone,
                    PinCode = PinCode,
                    default = True,
                )
            else:
                address_created = Address.objects.create(
                    Patient = self.request.user,
                    First_Name = First_Name,
                    Last_Name  = Last_Name,
                    Address = Address1,
                    Landmark = Landmark,
                    Extra = Extra,
                    Phone = Phone,
                    PinCode = PinCode,
                    default = True,
                )
            return Response({"message" : "Done"})
        if secondary_address:
            if Address.objects.filter(Patient=self.request.user,secondary_address=True).exists():
                address_obj = Address.objects.get(Patient=self.request.user,secondary_address=True)
                address_obj.secondary_address = False
                address_obj.save()
                address_created = Address.objects.create(
                    Patient = self.request.user,
                    First_Name = First_Name,
                    Last_Name  = Last_Name,
                    Address = Address1,
                    Landmark = Landmark,
                    Extra = Extra,
                    Phone = Phone,
                    PinCode = PinCode,
                    secondary_address = True,
                )
            else:
                address_created = Address.objects.create(
                    Patient = self.request.user,
                    First_Name = First_Name,
                    Last_Name  = Last_Name,
                    Address = Address1,
                    Landmark = Landmark,
                    Extra = Extra,
                    Phone = Phone,
                    PinCode = PinCode,
                    secondary_address = True,
                )
            return Response({"message" : "Done"})
        address_created = Address.objects.create(
            Patient = self.request.user,
            First_Name = First_Name,
            Last_Name  = Last_Name,
            Address = Address1,
            Landmark = Landmark,
            Extra = Extra,
            Phone = Phone,
            PinCode = PinCode,
        )
        order = Order.objects.get(Patient=self.request.user,Ordered=False)
        order.shipping_address = address_created
        order.Delivery_Charges = ZipCode.objects.get(PinCode=address_created.PinCode).Charges
        order.save()
        return Response({"message" : "Done"})


class PlaceOrderAPI(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self,request):
        order_qs = Order.objects.filter(Patient=self.request.user,Ordered=False)[0]
        order_qs.service_status = "Order Placed"
        order_qs.Ordered = True
        order_qs.save()
        return Response({"Message" : "Your Order is Placed Successfully"},status=status.HTTP_200_OK)