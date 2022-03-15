#####################################################################
# Copyright 2021 Tamilboomi Technologies,Inc. All Rights Reserved.
# Owner       :  Arun Madhu
# Created Date:  28/10/2021
# Updater     :  Arun Madhu
# Updated Date:  28/10/2021
#####################################################################

from django.shortcuts import render


def test_home(request):
    # Fetching All Students under Staff
    subject_list = []
    attendance_list = []
    trainee_list = []
    trainee_list_attendance_present = []
    trainee_list_attendance_absent = []
    context ={

        
        "trainees_count": 2,
        "attendance_count": 2,
        "leave_count": 2,
        "subject_count": 2,
        "subject_list": subject_list,
        "attendance_list": attendance_list,
        "trainee_list": trainee_list,
        "attendance_present_list": trainee_list_attendance_present,
        "attendance_absent_list": trainee_list_attendance_absent,

    }

    return render(request, "tb_track_app/md_template/test_home.html", context)

