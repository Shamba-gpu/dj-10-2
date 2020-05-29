from collections import Counter

from django.shortcuts import render_to_response

# Для отладки механизма ab-тестирования используйте эти счетчики
# в качестве хранилища количества показов и количества переходов.
# но помните, что в реальных проектах так не стоит делать
# так как при перезапуске приложения они обнулятся
counter_show = Counter()
counter_click = Counter()


def index(request):
    # Реализуйте логику подсчета количества переходов с лендига по GET параметру from-landing
    arg = request.GET.get("from-landing")
    if arg:
        if arg == 'original':
            counter_click['original'] += 1
        elif arg == 'test':
            counter_click['test'] += 1

    return render_to_response('index.html')


def landing(request):
    # Реализуйте дополнительное отображение по шаблону app/landing_alternate.html
    # в зависимости от GET параметра ab-test-arg
    # который может принимать значения original и test
    # Так же реализуйте логику подсчета количества показов
    arg = request.GET.get("ab-test-arg")
    if arg:
        if arg == 'original':
            counter_show['original'] += 1
            return render_to_response('landing.html')
        elif arg == 'test':
            counter_show['test'] += 1
            return render_to_response('landing_alternate.html')
    else:
        return render_to_response('landing.html')


def stats(request):
    # Реализуйте логику подсчета отношения количества переходов к количеству показов страницы
    # Чтобы отличить с какой версии лендинга был переход
    # проверяйте GET параметр marker который может принимать значения test и original
    # Для вывода результат передайте в следующем формате:
    
    # print(f'show: {counter_show}')
    # print(f'click: {counter_click}')

    if counter_show['test'] > 0:
        test_conversion = round(counter_click['test'] / counter_show['test'], 2)
    else:
        test_conversion = 0

    if counter_show['original'] > 0:
        original_conversion = round(counter_click['original'] / counter_show['original'], 2)
    else:
        original_conversion = 0

    return render_to_response('stats.html', context={
        'test_conversion': test_conversion,
        'original_conversion': original_conversion
    })
