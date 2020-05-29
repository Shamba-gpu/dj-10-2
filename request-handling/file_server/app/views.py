import datetime, os

from django.shortcuts import render
from django.conf import settings


class DatePathConverter:
    regex = r'[0-9]{4}-[0-9]{1,2}-[0-9]{1,2}'
    dateformat = '%Y-%m-%d'

    def to_python(self, value: str) -> datetime.date:
        return datetime.datetime.strptime(value, self.dateformat).date()

    def to_url(self, value: datetime.date) -> str:
        return value.strftime(self.dateformat)


def file_list(request, date=None):
    template_name = 'index.html'
    
    # Реализуйте алгоритм подготавливающий контекстные данные для шаблона по примеру:
    all_files = os.listdir(settings.FILES_PATH)
    # print(all_files)

    request_list = list()
    for file in all_files:
        stat = os.stat(os.path.join(settings.FILES_PATH, file))

        request_list.append(
            {'name': file,
                           'ctime': datetime.datetime.fromtimestamp(stat.st_ctime),
                           'mtime': datetime.datetime.fromtimestamp(stat.st_mtime)
            }
        )

    context = {
        'files': request_list,
        'date': date  # Этот параметр необязательный
    }

    return render(request, template_name, context)


def file_content(request, name):
    # Реализуйте алгоритм подготавливающий контекстные данные для шаблона по примеру:
    with open(os.path.join(settings.FILES_PATH, name), 'r') as file:
        file_content = file.read()

    return render(
        request,
        'file_content.html',
        context={'file_name': name, 'file_content': file_content}
    )

