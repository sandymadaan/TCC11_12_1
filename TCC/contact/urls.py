from TCC.contact.forms import *
from django.conf.urls.defaults import *
urlpatterns = patterns("TCC.contact.views",
    (r"^contact(\d+)/$", "contact"),
)

