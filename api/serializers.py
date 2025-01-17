from rest_framework import serializers
from rest_framework.serializers import ReadOnlyField

from api.models import Post, SubJob, Employee
from .models import User
#================ Blog =========================
# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['username', 'email']
#
# class BlogSerializer(serializers.ModelSerializer):
#     author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
#
#     class Meta:
#         model = Post
#         fields = '__all__'
#================ == =========================

class PostModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

class SubJobSerializer(serializers.ModelSerializer):
    class Meta:
        model=SubJob
        fields='__all__'


class EmployeeSerializer(serializers.ModelSerializer):
    first_name=ReadOnlyField(source='user.first_name')
    last_name=ReadOnlyField(source='user.last_name')
    class Meta:
        model=Employee
        fields='first_name,last_name'


class PostModelSerializer2(serializers.ModelSerializer):
    first_name = ReadOnlyField(source='customer.first_name')
    last_name = ReadOnlyField(source='customer.last_name')
    class Meta:
        model=Post
        fields="first_name","last_name","title","description"


# Tasks for Homework


#Task 1
class CurrentUserPostSerializer(serializers.ModelSerializer):
    first_name = ReadOnlyField(source='customer.first_name')
    last_name=ReadOnlyField(source='customer.last_name')
    class Meta:
        model=Post
        fields="title",'status','deadline','description','first_name','last_name'


#Task 2
class TopCustomerSerializer(serializers.ModelSerializer):
    customer_name = serializers.SerializerMethodField()
    post_count = serializers.IntegerField()

    class Meta:
        model = User
        fields = ['customer_name', 'post_count']

    def get_customer_name(self, object):
        return f"{object.first_name} {object.last_name}"

#Task 3
class TopFiveEmployeeSerializer(serializers.ModelSerializer):
    first_name = ReadOnlyField(source='employee.first_name')
    last_name = ReadOnlyField(source='employee.last_name')
    class Meta:
        model = Employee
        fields="first_name","last_name","rating","experience","lincedin"

#Task 4
class SubjobSerializer(serializers.ModelSerializer):
    first_name = ReadOnlyField(source='user.first_name')
    last_name = ReadOnlyField(source='user.last_name')
    class Meta:
        model = Employee
        fields = "first_name",'last_name', 'experience', 'rating'

class EmployeeSubJobSerializer(serializers.ModelSerializer):
    subjob_name = serializers.SerializerMethodField()
    employees=serializers.SerializerMethodField()
    class Meta:
        model=SubJob
        fields='subjob_name','employees'

    def get_subjob_name(self, object):
        return f"{object.name}"
    def get_employees(self, object):
        employees=object.employees.filter(experience__gte=3)
        serializer=SubjobSerializer(employees,many=True).data
        return serializer







