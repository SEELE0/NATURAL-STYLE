from django.urls import path
from app01 import views

urlpatterns = [
    path('landing/',views.landing.as_view()),
    path('landing4/',views.landing4.as_view()),
    path('landing3/',views.landing3.as_view()),
    path('landing5/',views.landing5.as_view()),
    path('landing6/',views.landing6.as_view()),
    path('MOVIE/',views.MOVIE.as_view()),
    path('landing/Candy/',views.Candy.as_view()),
    path('landing/Cubist/',views.Cubist.as_view()),
    path('landing/Mosaic/',views.Mosaic.as_view()),
    path('landing/Muse/',views.Muse.as_view()),
    path('landing/Rain/',views.Rain.as_view()),
    path('landing/Screem/',views.Screem.as_view()),
    path('landing/Shipwreck/',views.Shipwreck.as_view()),
    path('landing/Strarry/',views.Strarry.as_view()),
    path('landing/Udnie/',views.Udnie.as_view()),
    path('landing/monet/',views.monet.as_view()),
    path('landing/ukiyoe/',views.ukiyoe.as_view()),
    path('landing/vangogh/',views.vangogh.as_view()),
]