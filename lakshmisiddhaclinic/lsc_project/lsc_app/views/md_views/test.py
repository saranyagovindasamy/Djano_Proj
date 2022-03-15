#####################################################################
# Copyright 2021 Lakshmi Siddha Clinic. All Rights Reserved.
# Owner       :  Karthik Sivaraman
# Created Date:  11/12/2021
# Updater     :  Karthik Sivaraman
# Updated Date:  11/12/2021
#####################################################################

from django.shortcuts import render


def test_home(request):

    return render(request, "lsc_app/md_template/test_home.html",)

