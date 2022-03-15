#####################################################################
# Copyright 2021 Tamilboomi Technologies,Inc. All Rights Reserved.
# Owner       :  Saranya Govindasamy
# Created Date:  08/11/2021
# Updater     :  Saranya Govindasamy
# Updated Date:  09/11/2021
#####################################################################

from django.http.response import HttpResponse
from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from tb_track_app.models import *
from tb_track_app.serializers import *
# Create your views here.


def groupprofile_api(request):
        if request.method =='GET':
            groupprofile = GroupProfile.objects.all()
            serializer = GroupProfileSerializer(groupprofile,many=True)
            return JsonResponse(serializer.data,safe=False)

        elif request.method == 'POST':
            data = JSONParser().parse(request)
            serializer = GroupProfileSerializer(data = data)


        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data,status=201)
        return JsonResponse(serializer.errors,status=400)


def userprofile_api(request):
        if request.method =='GET':
            user = UserProfile.objects.all()
            serializer = UserProfileSerializer(user,many=True)
            return JsonResponse(serializer.data,safe=False)

        elif request.method == 'POST':
            data = JSONParser().parse(request)
            serializer = UserProfileSerializer(data = data)


        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data,status=201)
        return JsonResponse(serializer.errors,status=400)



def programmingLanguage_api(request):
    if request.method =='GET':
        program = ProgrammingLanguage.objects.all()
        serializer = ProgrammingLanguageSerializer(program,many=True)
        return JsonResponse(serializer.data,safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = ProgrammingLanguageSerializer(data = data)


    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data,status=201)
    return JsonResponse(serializer.errors,status=400)


def course_api(request):
    if request.method =='GET':
        course = Course.objects.all()
        serializer = CourseSerializer(course,many=True)
        return JsonResponse(serializer.data,safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = CourseSerializer(data = data)


    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data,status=201)
    return JsonResponse(serializer.errors,status=400)


def upcomingbatch_api(request):
    if request.method =='GET':
        upcomebatch = UpcomingBatch.objects.all()
        serializer = UpcomingBatchSerializer(upcomebatch,many=True)
        return JsonResponse(serializer.data,safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = UpcomingBatchSerializer(data = data)


    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data,status=201)
    return JsonResponse(serializer.errors,status=400)


def md_api(request):
    if request.method =='GET':
        md = MD.objects.all()
        serializer = MDSerializer(md,many=True)
        return JsonResponse(serializer.data,safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = MDSerializer(data = data)


    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data,status=201)
    return JsonResponse(serializer.errors,status=400)


def trainer_api(request):
    if request.method =='GET':
        trainer = Trainer.objects.all()
        serializer = TrainerSerializer(trainer,many=True)
        return JsonResponse(serializer.data,safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = TrainerSerializer(data = data)


    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data,status=201)
    return JsonResponse(serializer.errors,status=400)


def batch_api(request):
    if request.method =='GET':
        batch = Batch.objects.all()
        serializer = BatchSerializer(batch,many=True)
        return JsonResponse(serializer.data,safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = BatchSerializer(data = data)


    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data,status=201)
    return JsonResponse(serializer.errors,status=400)


def trainee_api(request):
    if request.method =='GET':
        trainee = Trainee.objects.all()
        serializer = TraineeSerializer(trainee,many=True)
        return JsonResponse(serializer.data,safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = TraineeSerializer(data = data)


    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data,status=201)
    return JsonResponse(serializer.errors,status=400)


def traineeenroll_api(request):
    if request.method =='GET':
        traineeenroll = TraineeEnroll.objects.all()
        serializer = TraineeEnrollSerializer(traineeenroll,many=True)
        return JsonResponse(serializer.data,safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = TraineeEnrollSerializer(data = data)


    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data,status=201)
    return JsonResponse(serializer.errors,status=400)


def attendance_api(request):
    if request.method =='GET':
        attendance = Attendance.objects.all()
        serializer = AttendanceSerializer(attendance,many=True)
        return JsonResponse(serializer.data,safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = AttendanceSerializer(data = data)


    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data,status=201)
    return JsonResponse(serializer.errors,status=400)



def attendancereport_api(request):
    if request.method =='GET':
        attendancereport = AttendanceReport.objects.all()
        serializer = AttendanceReportSerializer(attendancereport,many=True)
        return JsonResponse(serializer.data,safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = AttendanceReportSerializer(data = data)


    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data,status=201)
    return JsonResponse(serializer.errors,status=400)