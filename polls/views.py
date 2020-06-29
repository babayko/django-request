from django.http import HttpResponse

from polls.models import Question


def index(request):
    Question.objects.count()
    return HttpResponse("Hello, world. You're at the polls index.")
