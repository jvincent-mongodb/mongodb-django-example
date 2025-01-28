from django.shortcuts import render
from django.http import JsonResponse, StreamingHttpResponse
from django.views.decorators.csrf import csrf_protect
from videoStreamApp.models import User
from bson.objectid import ObjectId

from videoStreamApp.mongodb_connection import MongoDBConnection
from videoStreamApp.models import User

mongo = MongoDBConnection()

async def index(request):
    uploaded_videos = mongo.fs.find()
    videos = await uploaded_videos.to_list()
    titles = []
    for video in videos:
       titles.append(video['filename'])

    return render(request, 'index.html', {'uploaded_videos': titles})

# async def user_detail(request, username=None):
#     if not username:
#         return JsonResponse({"error": "Username is required."}, status=400)
#     user = await mongo.user_collection.find_one({"user.username": username})
#     if not user:
#         return JsonResponse({"error": "User not found."}, status=404)

#     return JsonResponse(user['user'], status=200)

# async def user(request):
#     if request.method == "POST":
#         user = {
#         "username": request.POST.get("username"),
#         "password": request.POST.get("password"),
#         "email":request.POST.get("email"),
#         }
#         mongo.user_collection.insert_one({"user": user})
#         user = await mongo.user_collection.find_one({"user.username": user["username"]})

#         return JsonResponse(user['user'], status=200)

def user_detail(request, username=None):
    if not username:
        return JsonResponse({"error": "Username is required."}, status=400)
    user = User.objects.get(username=username)
    
    if not user:
        return JsonResponse({"error": "User not found."}, status=404)

    response = {}
    for k, v in user.__dict__.items():
        if k == 'username':
            response[k] = v
        if k == 'email':
            response[k] = v

    return JsonResponse(response, status=200)

def user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        user = User(
            username=username,
            password=request.POST.get("password"),
            email=request.POST.get("email"),
        )
        user.save()
        user = User.objects.get(username=username)
        response = {}
        for k, v in user.__dict__.items():
            if k == 'username':
                response[k] = v
            if k == 'email':
                response[k] = v

        return JsonResponse(response, status=200)



async def upload_video(request):
    if request.method == "POST":
        video = request.FILES.get("file")
        filename = f"{video.name}"
        grid_in = mongo.fs.open_upload_stream_with_id(
            ObjectId(), filename, metadata={'contentType': 'video/mp4'})
        data = video.read()
        await grid_in.write(data)
        await grid_in.close()
    return JsonResponse({"video uplaoded": filename}, status=200)

async def stream_video(request, filename):
    grid_out = await mongo.fs.open_download_stream_by_name(filename)

    async def read():
        while grid_out.tell() < grid_out.length:
            yield await grid_out.readchunk()

    return StreamingHttpResponse(read(), content_type='video/mp4', 
        headers={'Content-Length': str(grid_out.length)})
