import json
import bcrypt
from django.shortcuts import render
from django.http import JsonResponse
from .models import *
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.tokens import RefreshToken
import random

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    refresh['id'] = user.id
    refresh['fullname'] = user.fullname
    refresh['username'] = user.username
    refresh['account_number'] = user.account_number
    refresh['balance'] = user.balance

    return {
        "access_token": str(refresh.access_token),
        "refresh_token": str(refresh),
    }

def generate_unique_account_number():
    while True:
        account_number = str(random.randint(10**12, 10**13 - 1))
        if not User.objects.filter(account_number=account_number).exists():
            return account_number

@csrf_exempt
def register(request):
    deserialize = json.loads(request.body)
    username = deserialize['username']

    if User.objects.filter(username=username).exists():
        return JsonResponse({"error": "Username already exists"}, status=400)
    else:
        hashing_password = bcrypt.hashpw(deserialize['password'].encode('utf-8'), bcrypt.gensalt())
        bcrypt_password = hashing_password.decode('utf-8')
        account_number = generate_unique_account_number()
        new_user = User.objects.create(fullname=deserialize['fullname'], username=username, password=bcrypt_password, account_number=account_number, balance=5000000)
        new_user.save()

        return JsonResponse({'message': 'User created successfully'}, status=201)

@csrf_exempt
def login(request):
    deserialize = json.loads(request.body)
    username = deserialize['username']
    password = deserialize['password']

    if not User.objects.filter(username=username).exists():
        return JsonResponse({"error": "Username does not exist"}, status=400)
    
    user = User.objects.get(username=username)

    if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        return JsonResponse({"error": "Invalid credentials"}, status=401)
    
    tokens = get_tokens_for_user(user)

    return JsonResponse({
            "message": "Login successful",
            "access_token": tokens["access_token"],
            "refresh_token": tokens["refresh_token"],
        }, status=200)

def get_user_by_id(request, user_id):
    user = User.objects.filter(id=user_id).first()
    if not user:
        return JsonResponse({"error": "User not found"}, status=404)

    return JsonResponse({
        "id": user.id,
        "fullname": user.fullname,
        "username": user.username,
        "account_number": user.account_number,
        "balance": user.balance
    }, status=200)

def get_user_by_account_number(request, account_number):
    user = User.objects.filter(account_number=account_number).first()
    if not user:
        return JsonResponse({"error": "User not found"}, status=404)

    return JsonResponse({
        "id": user.id,
        "fullname": user.fullname
    }, status=200)

@csrf_exempt
def add_friend(request):
    if request.method == "POST":
        try:
            deserialize = json.loads(request.body)
            user_id = deserialize['user_id']
            friend_id = deserialize['friend_id']

            if user_id == friend_id:
                return JsonResponse({"error": "Tidak bisa menambahkan diri sendiri sebagai teman"}, status=400)

            user = User.objects.filter(id=user_id).first()
            friend = User.objects.filter(id=friend_id).first()

            if not user or not friend:
                return JsonResponse({"error": "User tidak ditemukan"}, status=404)

            # Cek apakah pertemanan sudah ada
            if Friendship.objects.filter(user=user, friend=friend).exists():
                return JsonResponse({"error": "Pertemanan sudah ada"}, status=400)

            # Tambahkan hubungan pertemanan dua arah
            Friendship.objects.create(user=user, friend=friend)
            Friendship.objects.create(user=friend, friend=user)

            return JsonResponse({"message": "Pertemanan berhasil ditambahkan"}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Format JSON tidak valid"}, status=400)

    return JsonResponse({"error": "Method tidak diizinkan"}, status=405)

@csrf_exempt
def get_user_friends(request, user_id):
    if request.method == "GET":
        user = User.objects.filter(id=user_id).first()

        if not user:
            return JsonResponse({"error": "User tidak ditemukan"}, status=404)

        # Ambil semua teman user dari tabel Friendship
        friends = Friendship.objects.filter(user=user).select_related("friend")

        # Format data ke JSON
        friends_list = [
            {
                "id": friend.friend.id,
                "fullname": friend.friend.fullname,
                "username": friend.friend.username,
                "account_number": friend.friend.account_number,
            }
            for friend in friends
        ]

        return JsonResponse({"friends": friends_list}, status=200)

    return JsonResponse({"error": "Method tidak diizinkan"}, status=405)