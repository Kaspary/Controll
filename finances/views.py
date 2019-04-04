import json
from datetime import date
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from .models import *
from core.models import SystemUser


@login_required(login_url='login:login')
def finances_management(request):
    context = {
        'system_user': SystemUser.objects.get(user=request.user)
    }

    return render(request, 'finances_management.html', context)

def get_finances(request):

    if request.method == 'POST' and request.is_ajax():
        try:

            d = json.loads(request.POST.get('date', None))

            earnings = list(SystemUser.objects.get(user=request.user).earnings.filter(date__year=d['year'], date__month=d['month']).values('id', 'title', 'value', 'fixed'))
            expense = list(SystemUser.objects.get(user=request.user).expense.filter(date__year=d['year'], date__month=d['month']).values('id', 'title', 'value', 'category', 'fixed'))
            category = list(SystemUser.objects.get(user=request.user).expense_category.all().values('id', 'title'))

            return JsonResponse({
                'status': 'success',
                'message_title': 'Finanças iniciadas',
                'earnings': {
                    'earnings': earnings,
                    'total': _get_total_earnings(d, request.user)
                },
                'expense': {
                    'expense':expense,
                    'category': category,
                    'total': _get_total_expense(d, request.user)
                }
            })
        except Exception as e:
            print('ERROR: ', str(e))
            return JsonResponse({'status': 'error', 'message_title': 'Erro ao iniciar finanças'})

def save_earnings(request):
    if request.method == 'POST' and request.is_ajax():
        try:
            d = json.loads(request.POST.get('date', None))

            earning=Earnings.objects.create(
                title=request.POST['title'],
                value=request.POST['value'],
                date=date(d['year'], d['month'], d['day'])
            )

            SystemUser.objects.get(user=request.user).earnings.add(earning)

            return JsonResponse({
                'status': 'success',
                'message_title': 'Salvo com sucesso',
                'earning':{
                    'earning':{
                        'id': earning.pk,
                        'title': earning.title,
                        'value': float(earning.value),
                        'fixed': earning.fixed,
                        'date': earning.date
                    },
                    'total': _get_total_earnings(d, request.user)
                }
            })

        except Exception as e:
            print('ERROR: ',str(e))
            return JsonResponse({'status': 'error', 'message_title': 'Erro ao salvar'})

def edit_earnings(request):
    if request.method == 'POST' and request.is_ajax():
        try:

            d = json.loads(request.POST.get('date', None))

            Earnings.objects.filter(id=request.POST['id']).update(title=request.POST['title'], value=request.POST['value'])

            return JsonResponse({
                'status': 'success',
                'message_title': 'Editado com sucesso',
                'earning':{
                    'earning': {
                        'id': request.POST['id'],
                        'title': request.POST['title'],
                        'value': float(request.POST['value']),
                    },
                    'total': _get_total_earnings(d, request.user)
                }
            })
        except Exception as e:
            print('ERROR: ',str(e))
            return JsonResponse({'status': 'error', 'message_title': 'Erro ao editar'})

def fix_earnings(request):

    if request.method == 'POST' and request.is_ajax():
        try:
            if request.POST['fixed'] == 'true':
                Earnings.objects.filter(id=request.POST['id']).update(fixed=True)
                message_title = 'Fixado com sucesso'
            else:
                Earnings.objects.filter(id=request.POST['id']).update(fixed=False)
                message_title = 'Desfixado com sucesso'

            return JsonResponse({
                'status': 'success',
                'message_title': message_title,
                'earning': {
                    'earning': {
                        'id': request.POST['id'],
                        'fixed': request.POST['fixed']
                    }
                }

            })
        except Exception as e:
            print('ERROR: ',str(e))
            return JsonResponse({'status': 'error', 'message_title': 'Erro ao ficar'})

def remove_earnings(request):
    if request.method == 'POST' and request.is_ajax():
        try:

            d = json.loads(request.POST.get('date', None))

            Earnings.objects.get(id=request.POST['id']).delete()
            return JsonResponse({
                'status': 'success',
                'message_title': 'Excluido com sucesso',
                'earning':{
                    'earning': {
                        'id': request.POST['id'],
                    },
                    'total': _get_total_earnings(d, request.user)
                }
            })
        except Exception as e:
            print('ERROR: ',str(e))
            return JsonResponse({'status': 'error', 'message_title': 'Erro ao excluir'})

def save_expense(request):
    if request.method == 'POST' and request.is_ajax():
        try:
            d = json.loads(request.POST.get('date', None))

            expense=Expense.objects.create(
                title=request.POST['title'],
                value=request.POST['value'],
                category=ExpensesCategory.objects.get(id=request.POST['category']),
                date=date(d['year'], d['month'], d['day'])
            )

            SystemUser.objects.get(user=request.user).expense.add(expense)

            category = SystemUser.objects.get(user=request.user).expense_category.all()
            category_json=[]
            for c in category:
                category_json.append({
                    'id': c.id,
                    'title': c.title,
                })

            return JsonResponse({
                'status': 'success',
                'message_title': 'Salvo com sucesso',
                'expense':{
                    'expense':{
                        'id': expense.pk,
                        'title': expense.title,
                        'value': float(expense.value),
                        'category': expense.category.pk,
                        'fixed': expense.fixed,
                        'date': expense.date
                    },
                    'category': category_json,
                    'total': _get_total_expense(d, request.user)
                }
            })

        except Exception as e:
            print('ERROR: ',str(e))
            return JsonResponse({'status': 'error', 'message_title': 'Erro ao salvar'})

def edit_expense(request):
    if request.method == 'POST' and request.is_ajax():
        try:
            d = json.loads(request.POST.get('date', None))
            Expense.objects.filter(id=request.POST['id']).update(
                title=request.POST['title'],
                value=request.POST['value'],
                category=ExpensesCategory.objects.get(id=request.POST['category']))

            return JsonResponse({
                'status': 'success',
                'message_title': 'Editado com sucesso',
                'expense':{
                    'expense':{
                        'id': request.POST['id'],
                        'title': request.POST['title'],
                        'value': float(request.POST['value']),
                        'category': request.POST['category'],
                    },
                    'total': _get_total_expense(d, request.user)
                }
            })
        except Exception as e:
            print('ERROR: ',str(e))
            return JsonResponse({'status': 'error', 'message_title': 'Erro ao editar'})

def fix_expense(request):
    if request.method == 'POST' and request.is_ajax():
        try:
            if request.POST['fixed'] == 'true':
                Expense.objects.filter(id=request.POST['id']).update(fixed=True)
                message_title = 'Fixado com sucesso'
            else:
                Expense.objects.filter(id=request.POST['id']).update(fixed=False)
                message_title = 'Desfixado com sucesso'

            return JsonResponse({
                'status': 'success',
                'message_title': message_title,
                'expense': {
                    'expense': {
                        'id': request.POST['id'],
                        'fixed': request.POST['fixed']
                    }
                }

            })
        except Exception as e:
            print('ERROR: ',str(e))
            return JsonResponse({'status': 'error', 'message_title': 'Erro ao ficar'})

def remove_expense(request):
    if request.method == 'POST' and request.is_ajax():
        try:
            d = json.loads(request.POST.get('date', None))
            Expense.objects.get(id=request.POST['id']).delete()
            return JsonResponse({
                'status': 'success',
                'message_title': 'Excluido com sucesso',
                'expense':{
                    'expense':{
                        'id': request.POST['id'],
                    },
                    'total': _get_total_expense(d, request.user)
                }
            })
        except Exception as e:
            print('ERROR: ',str(e))
            return JsonResponse({'status': 'error', 'message_title': 'Erro ao excluir'})


def _get_total_earnings(date, user):
    try:
        total_value = SystemUser.objects.get(user=user).earnings.filter(date__year=date['year'], date__month=date['month']).aggregate(Sum('value'))
        return total_value['value__sum'] or 0.0
    except Exception as e:
        print('ERROR: ', str(e))
        return 0.0


def _get_total_expense(date, user):
    try:
        total_value = SystemUser.objects.get(user=user).expense.filter(date__year=date['year'], date__month=date['month']).aggregate(Sum('value'))
        return total_value['value__sum'] or 0.0
    except Exception as e:
        print('ERROR: ', str(e))
        return 0.0