from mss_app.views import home, client, import_views, accounts
from django.urls import path, re_path
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView
from mss_app.form import LoginForm
from mss_app.views.transactions import auto_refill,credit,debit,mcash,transaction

favicon_view = RedirectView.as_view(
    url='/static/favicon.ico', permanent=True)


urlpatterns = [
    re_path(r'^favicon\.ico$', favicon_view),

    path('', home.home, name='home'),
    path('home/', home.home, name='home'),
    path('progress/', home.index, name='progress'),

    # Accounts
    path(r'login/', accounts.user_login, name='login'),
    path(r'logout/', accounts.user_logout, name='logout'),
    # path(r'login/', auth_views.LoginView.as_view(template_name="mss_app/accounts/login.html",
                                                #   authentication_form=LoginForm), name="login"),
    # path(r'logout/', auth_views.LogoutView.as_view(
    #     template_name="mss_app/accounts/logged_out.html"), name="logout"),

    #Transactions
    path('credit/new ', credit.credit_transaction_create, name='credit-new'),
    path('debit/new ', debit.debit_transcation_create, name='debit-new'),
    path('mcash/', mcash.mcash_transcation_create, name='mcash'),
    path('transcations/', transaction.transcation_per_client, name='transcations-per-client'),


    # Client
    path('client/add', client.client_profile_create, name='client-add'),
    path('client_edit/<client_id>', client.client_edit, name='client_edit'),
    path('client_edit_save', client.client_edit_save, name='client_edit_save'),


    # Import views
    path('auto-refill/import', import_views.auto_refil_import,
         name='autorefill-import'),
    path('import/client', import_views.client_import, name='import-client'),

    #Summary
    path('debitsales/', debit.debit_sales_bycategory, name='debitsales'),
    path('creditsales/', credit.credit_sales_bycategory, name='creditsales'),
    path('credit/summary ', credit.credit_transaction_summary, name='credit-summary'),
    path('debit/summary ', debit.debit_transcation_summary, name='debit-summary'),
    path('auto-refill/summary ', auto_refill.auto_refill_summary, name='autorefill-summary'),
    path('client/summary', client.client_details, name='client-details'),

    # AJAX Request URL
    path(r'load_client_ajax/', client.load_client_ajax, name='load_client_ajax/'),
    path(r'load_mcash_ajax/', mcash.load_mcash_ajax, name='load_mcash_ajax/'),
    path(r'load_client_by_id_ajax/', client.load_client_by_id_ajax, name='load_client_by_id_ajax/'),
    path(r'load_client_transcation_by_id_ajax/', transaction.load_client_transcation_by_id_ajax, name='load_client_transcation_by_id_ajax/'),
    
]
