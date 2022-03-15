#####################################################################
# Copyright 2021 Tamilboomi Technologies,Inc. All Rights Reserved.
# Owner       :  Saranya Govindasamy
# Created Date:  08/11/2021
# Updater     :  Saranya Govindasamy
# Updated Date:  09/11/2021
#####################################################################

from rest_framework import serializers
from . models import *

class GroupProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model= GroupProfile
        fields='__all__'


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model= UserProfile
        fields='__all__'


class ProgrammingLanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model= ProgrammingLanguage
        fields='__all__'


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model= Course
        fields='__all__'


class UpcomingBatchSerializer(serializers.ModelSerializer):
    class Meta:
        model= UpcomingBatch
        fields='__all__'

class MDSerializer(serializers.ModelSerializer):
    class Meta:
        model= MD
        fields='__all__'

class TrainerSerializer(serializers.ModelSerializer):
    class Meta:
        model= Trainer
        fields='__all__'

class BatchSerializer(serializers.ModelSerializer):
    class Meta:
        model= Batch
        fields='__all__'

class TraineeSerializer(serializers.ModelSerializer):
    class Meta:
        model= Trainee
        fields='__all__'

class TraineeEnrollSerializer(serializers.ModelSerializer):
    class Meta:
        model= TraineeEnroll
        fields='__all__'

class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model= Attendance
        fields='__all__'

class AttendanceReportSerializer(serializers.ModelSerializer):
    class Meta:
        model= AttendanceReport
        fields='__all__'