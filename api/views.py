from django.db.migrations import serializer
from django.db.models import Count
from django.http import JsonResponse
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import Post, User, SubJob, Job, Employee
from api.serializers import PostModelSerializer, SubJobSerializer, PostModelSerializer2, CurrentUserPostSerializer, \
    TopCustomerSerializer, TopFiveEmployeeSerializer, EmployeeSubJobSerializer


# class DRF(APIView):
#     def get(self, request):
#         name=request.GET.get('name')
#         return JsonResponse({'message':f'Hello {name}'})
#
# class DRF2(APIView):
#     def get(self,request):
#         name=request.GET.get('name')
#         lang_code=request.GET.get('language')
#         if lang_code=='uz':
#             return JsonResponse({'message':f'Salom {name}'})
#         elif lang_code=='en':
#             return JsonResponse({'message':f'Hello {name}'})
#         elif lang_code=='es':
#          return JsonResponse({'message':f'Hola {name}'})

# ===================== Blog Views Full ================================

# @api_view(['GET'])
# def posts_view(request):
#     posts=Post.objects.all()
#     serializer=BlogSerializer(posts,many=True)
#     return JsonResponse(serializer.data,safe=False)
#
#
# @api_view(['POST', 'GET'])
# def add_post_view(request):
#     if request.method == "GET":
#         posts = Post.objects.all()
#         serializer = BlogSerializer(posts, many=True)
#         return JsonResponse(serializer.data, safe=False)
#     elif request.method == "POST":
#         data = request.data.copy()
#         serializer = BlogSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse({'success': 'Post created'}, status=201)
#         else:
#             return JsonResponse(serializer.errors, status=400)
#
#
# @api_view(['GET', 'PUT', 'PATCH'])
# def update_post_view(request, pk):
#     try:
#         post = Post.objects.get(pk=pk)
#     except Post.DoesNotExist:
#         return JsonResponse({'error': 'Post not found'}, status=404)
#
#     if request.method == 'GET':
#         serializer = BlogSerializer(post)
#         return JsonResponse(serializer.data)
#
#     if request.method == 'PUT' or request.method == 'PATCH':
#         serializer = BlogSerializer(post, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse({'success': 'Post updated'}, status=200)
#         return JsonResponse(serializer.errors, status=400)
#
# @api_view(['DELETE'])
# def delete_post_view(request, pk):
#     try:
#         post=Post.objects.get(pk=pk)
#         post.delete()
#         posts=Post.objects.all()
#         seializer=BlogSerializer(posts,many=True)
#         response=[
#             {'success': 'Post deleted',
#              'posts': seializer.data}
#         ]
#         return Response(response, status=200)
#     except Post.DoesNotExist:
#         return JsonResponse({'error': 'Post not found'}, status=404)


# ===================== Blog Views Full ================================

@extend_schema(tags=['Posts'],request=PostModelSerializer)
@api_view(['GET'])

def posts_list_view(request):
    posts=Post.objects.all()
    serializer = PostModelSerializer(posts, many=True)
    return JsonResponse(serializer.data, safe=False)

@extend_schema(tags=['Posts'],request=PostModelSerializer)
@api_view(['POST'])
def create_post_view(request):
    serializer = PostModelSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)

@extend_schema(tags=['SubJob'],
        parameters=[
            OpenApiParameter(
                name="job-id",
                description=(
                    "Searches for the value in this query parameter returning "
                    "all the users that have this value as substring. Ignores lowercase and uppercase."
                ),
                type=str,
            )
        ]
    )
@api_view(['GET'])
def get_subjob_view(request):
    pk=request.query_params.get('job-id')
    subjobs=SubJob.objects.filter(job_id=pk)
    serializer=SubJobSerializer(subjobs,many=True)
    return JsonResponse(serializer.data, safe=False)

@extend_schema(tags=['Posts'],request=PostModelSerializer)
@api_view(['GET'])
def get_post_view(request):
    posts=Post.objects.all()
    serializer=PostModelSerializer2(posts,many=True)
    return Response(serializer.data)

@extend_schema(tags=['HomeWork'])
@api_view(['GET'])
def task1(request):
    posts=Post.objects.filter(customer=request.user)
    serializer=CurrentUserPostSerializer(posts,many=True)
    return Response(serializer.data)


@extend_schema(tags=['HomeWork'])
@api_view(['GET'])
def task2(request):
    top_customer = User.objects.annotate(post_count=Count('posts')).order_by('-post_count').first()

    if top_customer:
        serializer = TopCustomerSerializer(top_customer)
        return Response(serializer.data)
    else:
        return Response({"error": "No customers found"})


@extend_schema(tags=['HomeWork'])
@api_view(['GET'])
def task3(request):
    top5_employee=Employee.objects.all().order_by('-rating')
    if len(top5_employee)>=5:
        serializer=TopFiveEmployeeSerializer(top5_employee[0:5],many=True)
        return Response(serializer.data)
    return Response({'error':'Employees not found'})


@extend_schema(tags=['HomeWork'])
@api_view(['GET'])
def task4(request):
    subjobs = SubJob.objects.prefetch_related('employees').all()

    serializer = EmployeeSubJobSerializer(subjobs, many=True)
    return Response(serializer.data)



