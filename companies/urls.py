from django.conf.urls import url
from .views import RegisterView, LoginView, InvestView, CompanyRegisterView, CompanyUpdateView, InvestRView

urlpatterns = [
    url(r'register',RegisterView.as_view(), name="userList"),
    url(r'login', LoginView.as_view(), name="login"),
    url(r'get_invest/(?P<pk>\d+)$', InvestView.as_view(), name="get_invest"),
    url(r'add_invest', InvestRView.as_view(), name="add_invest"),
    url(r'update_invest/(?P<pk>\d+)$', InvestView.as_view(), name="update_invest"),
    url(r'add', CompanyRegisterView.as_view(), name="company"),
    url(r'update/(?P<pk>\d+)$',CompanyUpdateView.as_view(), name="update"),
    url(r'delete/(?P<pk>\d+)$',CompanyUpdateView.as_view(), name="update"),
    url(r'get',CompanyUpdateView.as_view(),name="get")
]