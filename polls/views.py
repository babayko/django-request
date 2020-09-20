import json
import datetime

from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def save_client_log(request):
    """
    Сохраняет собранные данные с клиента в лог
    """
    logs = request.POST.get('logs', '[]')
    with open('request.log', 'a') as f:
        for log_str in json.loads(logs):
            f.write(json.dumps(log_str) + '\n')

    return HttpResponse()


def get_page_with_button(request):
    """
    Возвращает страницу с кнопкой
    """
    template = loader.get_template('polls/index.html')

    return HttpResponse(template.render({}, request))


def get_current_datetime(request):
    """
    Возвращает текущую дату и время
    """
    return HttpResponse(datetime.datetime.now())
