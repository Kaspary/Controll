from django.conf.urls import url
from .views import *
app_name='finances'

urlpatterns = [
    url(r'^finances_management$', finances_management, name='finances_management'),
    url(r'^qr_scanner$', qr_scanner, name='qr_scanner'),

    #AJAX METHODS
    url(r'^save_expense_of_qr_code', save_expense_of_qr_code, name='save_expense_of_qr_code'),

    
    url(r'^get_finances', get_finances, name='get_finances'),

    url(r'^save_earnings', save_earnings, name='save_earnings'),
    url(r'^edit_earnings', edit_earnings, name='edit_earnings'),
    url(r'^fix_earnings', fix_earnings, name='fix_earnings'),
    url(r'^remove_earnings', remove_earnings, name='remove_earnings'),

    url(r'^save_expense', save_expense, name='save_expense'),
    url(r'^edit_expense', edit_expense, name='edit_expense'),
    url(r'^fix_expense', fix_expense, name='fix_expense'),
    url(r'^remove_expense', remove_expense, name='remove_expense'),

    url(r'^get_expenses_category', get_expenses_category, name='get_expenses_category'),
    url(r'^save_category_expense', save_category_expense, name='save_category_expense'),
    url(r'^edit_category_expense', edit_category_expense, name='edit_category_expense'),
    url(r'^remove_category_expense', remove_category_expense, name='remove_category_expense'),
]