from django.urls import path
from . import views

urlpatterns = [

    path(
        "",
        views.candidate_list,
        name="candidate_list"
    ),

    path(
        "upload/",
        views.upload_candidate,
        name="upload_candidate"
    ),

    path(
        "apply/",
        views.apply_candidate,
        name="apply"
    ),

    path(
        "<int:id>/",
        views.candidate_detail,
        name="candidate_detail"
    ),

]