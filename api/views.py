from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.models import Post
from api.serializers import PostSerializer


@api_view(['GET'])
def index(request):
    return Response({"Success": "The setup was successful"})


@api_view(['GET'])
def get_all_post(request):
    get_posts = Post.objects.all()  # This endpoint goes and gets all the posts in database
    serializer = PostSerializer(get_posts, many=True)  # The data is converted to the correct format
    return Response(serializer.data)  # The suitable data is used by the response class


@api_view(['GET', 'POST'])
def create_post(request):
    data = request.data
    serializer = PostSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response({"Success": "The post was successfully created"}, status=201)
    else:
        return Response(serializer.errors, status=400)


@api_view(['DELETE'])
def delete(request):
    post_id = request.data.get('post_id')
    try:
        post = Post.objects.get(id=post_id)
        post.delete()
        return Response({"Success": "The post was successfully deleted"}, status=200)
    except Post.DoesNotExist:
        return Response({"Error": "The post does not exist"}, status=404)


@api_view(['GET'])
def get_post(request):
    post_id = request.data.get('post_id')
    try:
        post = Post.objects.get(id=post_id)
        serializer = PostSerializer(post)
        return Response(serializer.data)
    except Post.DoesNotExist:
        return Response({"Error": "The post does not exist"}, status=404)


@api_view(['PUT'])
def update_post(request):
    post_id = request.data.get('post_id')
    get_new_name = request.data.get('new_name')
    get_new_price = request.data.get('new_price')
    get_new_stock = request.data.get('new_stock')
    get_new_description = request.data.get('new_description')
    try:
        post = Post.objects.get(id=post_id)
        if get_new_name:
            post.title = get_new_name
        if get_new_price:
            post.price = get_new_price
        if get_new_stock:
            post.stock = get_new_stock
        if get_new_description:
            post.description = get_new_description
        post.save()
        return Response({"Success": "The post was successfully updated"}, status=200)
    except Post.DoesNotExist:
        return Response({"Error": "The post does not exist"}, status=404)
