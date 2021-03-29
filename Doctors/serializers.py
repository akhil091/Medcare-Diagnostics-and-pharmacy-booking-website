from rest_framework import serializers
from Doctors.models import Doctor,Specialization,Condition,AllBooking


class SpecializationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialization
        fields = '__all__'

class ConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Condition
        fields = '__all__'

class DoctorSerializer(serializers.ModelSerializer):

    Condition = serializers.SerializerMethodField()
    Specialization = serializers.SerializerMethodField()
    doc_timing = serializers.SerializerMethodField()
    avaliablity = serializers.SerializerMethodField()

    class Meta:
        model = Doctor
        fields = (
            'id',
            'Name',
            'Specialization',
            'week_timing',
            'Condition',
            'Qualification',
            'Gender',
            'Overall_Exp',
            'Description',
            'doc_timing',
            'Fee',
            'Profile_pic',
            'avaliablity',
        )

    def get_Condition(self,obj):
        return ConditionSerializer(obj.Condition).data

    def get_Specialization(self,obj):
        return SpecializationSerializer(obj.Specialization).data

    def get_doc_timing(self,obj):
        return obj.get_doc_timing()

    def get_avaliablity(self,obj):
        return obj.get_avaliablity()

class AllBookingSerializers(serializers.ModelSerializer):
    Doctor_Detail = serializers.SerializerMethodField()

    class Meta:
        model = AllBooking
        fields = (
            'First_Name',
            'Last_Name',
            'Email',
            'Age',
            'Phone',
            'Date',
            'Fee',
            'paid',
            'Allot_Time',
            'Doctor_Detail',
        )

    def get_Doctor_Detail(self,obj):
        return DoctorSerializer(obj.Doctor).data

