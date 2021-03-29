from rest_framework import serializers
from Lab.models import NotSure,Tests,HealthPackage, Condition, Cart, Order, Address, Lab_Result

class ConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Condition
        fields = (
            'name',
        )

class TestsSerializer(serializers.ModelSerializer):
    conditions = serializers.SerializerMethodField()

    class Meta:
        model = Tests
        fields = (
            'id',
            'Name',
            'Description',
            'Test_Type',
            'Pre_Test_Information',
            'Test_Components',
            'Report_Delivery',
            'Price',
            'Discount_Price',
            'Method',
            'conditions',
        )

    def get_conditions(self,obj):
        return ConditionSerializer(obj.conditions).data

class HealthPackageSerializer(serializers.ModelSerializer):
    conditions = serializers.SerializerMethodField()
    Tests_includes = serializers.SerializerMethodField()

    class Meta:
        model = HealthPackage
        fields = (
            'id',
            'Name',
            'Description',
            'Test_Type',
            'Pre_Test_Information',
            'Test_Components',
            'Report_Delivery',
            'Price',
            'Discount_Price',
            'Method',
            'conditions',
            'Tests_includes',
        )

    def get_conditions(self,obj):
        return ConditionSerializer(obj.conditions).data

    def get_Tests_includes(self,obj):
        return TestsSerializer(obj.Tests_includes,many=True).data


class CartSerializer(serializers.ModelSerializer):
    Original_Price = serializers.SerializerMethodField()
    Total_Price = serializers.SerializerMethodField()
    Test = serializers.SerializerMethodField()
    Package = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = (
            'id',
            'Patient',
            'Ordered',
            'Test',
            'Package',
            'Original_Price',
            'Total_Price',
        )

    def get_Original_Price(self,obj):
        return obj.get_original_price()

    def get_Total_Price(self,obj):
        return obj.get_total_price()

    def get_Test(self,obj):
        if obj.Test is None:
            return None
        return TestsSerializer(obj.Test).data

    def get_Package(self,obj):
        if obj.Package is None:
            return None
        return HealthPackageSerializer(obj.Package).data

class OrderSerializers(serializers.ModelSerializer):
    Tests = serializers.SerializerMethodField()
    Packages = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = (
            'Patient',
            'Tests',
            'Packages',
            'Ordered_Date',
            'Ordered',
            'total_amount',
        )

    def get_Tests(self,obj):
        if obj.Tests is None:
            return None
        return CartSerializer(obj.Tests.all(),many=True).data

    def get_Packages(self,obj):
        if obj.Packages is None:
            return None
        return CartSerializer(obj.Packages.all(),many=True).data


class AddressSerializers(serializers.ModelSerializer):

    class Meta:
        model = Address
        fields = '__all__'


class Lab_ResultSerializers(serializers.ModelSerializer):
    
    class Meta:
        model = Lab_Result
        fields = '__all__'