from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
#from django.conf import settings
#from django.conf.urls.static import static


from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("<int:id>", views.index),
    path("create/", views.create, name="create"),
    path("gallery", views.gallery, name="gallery"),
    path("3D-prints", views.gallery3d, name="gallery3d"),
    path("videos", views.videos, name="videos"),
    path("carousel", views.carousel, name="carousel"),
    path("scrape", views.scrape, name="scrape"),
    path("weather", views.weather, name="weather"),
    path("stocks_prediction", views.prediction, name="prediction"),
    path("face_detection", views.face_detection, name="face_detection"),
    path("eye_detection", views.eye_detection, name="eye_detection"),
    path("video_feed", views.video_feed, name="video_feed"),
    path("video_feed1", views.video_feed1, name="video_feed1"),
    path("upload", views.upload, name="upload"),
    path("notes", views.notes, name="notes"),
    path("update/<int:id>", views.update, name="update"),
    path("delete-note", views.delete_note, name="delete_note"),
    path("obrazky_update", views.obrazky_update, name="obrazky_update"),
    path("return-files/<filename>", views.return_files, name="return_files"),
    path("delete-picture", views.delete_picture, name="delete_picture"),
]

#urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()