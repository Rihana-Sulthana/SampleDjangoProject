from django.shortcuts import render
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from datetime import datetime, timedelta
from django.db.models import Count

from django.views.decorators.csrf import csrf_exempt


class CreateUser(APIView):

    def post(self, request):
        post_data = request.data
        serializer = UserSerializer(data=post_data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(data={'user': serializer.data})

        return Response(data={'user': serializer.errors})


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def cretae_question(request):
    '''
     cretaes questions
    :param request:
    :return:
    '''
    question = request.data.get('question')
    Questions.objects.create(user=request.user, question=question)
    return Response('Question submitted successfully')


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_user_questions(request):
    '''
       Returns questions raised by user
    :param request:
    :return: list of questions
    '''
    questions = list(Questions.objects.filter(user=request.user.id).values_list('questions', flat=True))
    return Response(questions)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_user_answers(request):
    '''
     Returns answers given by user for all questions or specific question
    :request_param question_id: id of the question
    :return: list of dicts
    '''
    question_id = request.GET.get('question_id')
    res_obj = Answers.objects.filter(answer_by=request.user.id)
    if question_id:
        res_obj = res_obj.filter(question=question_id)
    answers = res_obj.values('question__question', 'answer')
    return Response(answers)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def upvotes_by_user(request):
    '''
       returns upvote done by the user
    :param request:
    :return: list of dicts
    '''
    resp = []
    upvotes = UpVotes.objects.filter(upvoted_by=request.user.id)
    for upvote in upvotes:
        data = {
            "question": upvote.answer.question.question,
            "answer": upvote.answer.answer
        }
        resp.append(data)

    return Response(data)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_answers_of_an_question(request, question_id):
    '''
     Returns answers for the questions
    :param question_id:  id of the question
    :return: list of answers of the question
    '''
    answers = list(Answers.objects.filter(question=question_id).values_list('answer__answer'))
    return Response(answers)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_question_upvotes(request, answer_id):
    '''
       Returns upvotes of an question
    :param request:
    :param question_id: id of the question
    :return:  upvoters
    '''

    upvotes = list(UpVotes.objects.filter(answer=answer_id).values_list('upvoted_by__name'))
    return Response(upvotes)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_highest_upvoted_question(request, past_hour=False):
    '''
     Returns question with highest upvotes
    :param past_hour: indicate return results for past one hour
    :return: question with highest upvotes
    '''
    upvote_obj = UpVotes.objects.all()
    if past_hour:
        time_threshold = datetime.now() - timedelta(hours=1)
        upvote_obj = upvote_obj.filter(date_created__lte=time_threshold)

    answer = upvote_obj.values('answer').annotate(count=Count('answer')).order_by('-count')[:1]
    answer_id = answer[0].get('answer_id')
    question = Answers.objects.filter(pk=answer_id).values('question__question')
    return Response(question)
