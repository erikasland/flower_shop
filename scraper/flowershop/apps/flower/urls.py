from django.conf.urls import url
from views import Index, Log, Reg, Main, Logout, AddToCart, Checkout

urlpatterns = [
    url(r'^$', Index.as_view()),
    url(r'^login$', Log.as_view()),
    url(r'^logout$', Logout.as_view()),
    url(r'^register$', Reg.as_view()),
    url(r'^main$', Main.as_view()),
    url(r'^cart$', AddToCart.as_view()),
    url(r'^checkout$', Checkout.as_view()),
    ]