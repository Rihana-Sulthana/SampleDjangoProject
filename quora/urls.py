from django.urls import path
from django.conf.urls import url
from .views import *





urlpatterns = [
    url(r'^users/register',  CreateUser.as_view()),
    url(r'^create_questions', cretae_question),
    url(r'^users/questions', get_user_questions),
    url(r'^users/answers', get_user_answers),
    url(r'^questions/(?P<question_id>.*)/answers', get_answers_of_an_question),
    url(r'^questions/(?P<answer_id>.*)/upvotes', get_question_upvotes),
    url(r'^questions/recent_upvotes', get_highest_upvoted_question, {"past_hour": True}),
]
