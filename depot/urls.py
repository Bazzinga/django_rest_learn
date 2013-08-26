
from django.conf.urls.defaults import *
from models import *
from views import *


from django.conf.urls.defaults import *
from models import *
from views import *
from serializers import *


from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),

    (r'product/create/$', create_product),
    (r'product/list/$', list_product),
    (r'product/edit/(?P<id>[^/]+)/$', edit_product),
    (r'product/view/(?P<id>[^/]+)/$', view_product),
    (r'store/$', store_view),
    (r'cart/view/', view_cart),
    (r'cart/add/(?P<id>[^/]+)/$', add_to_cart),
    (r'cart/clean/', clean_cart),
    (r'API/cart/items/', RESTforCart),
    (r'API/cart/post/', PostCart),

    (r'^accounts/login/$', login_view),
    (r'^accounts/logout/$', logout_view),
)

urlpatterns += patterns('depot.views',
    url(r'^cleantha/$', 'snippet_list'),
    url(r'^cleantha/(?P<id>[0-9]+)/$', 'snippet_detail'),
)

urlpatterns += patterns('',

    (r'order/create/$', create_order),
    (r'order/list/$', list_order ),
    (r'order/edit/(?P<id>[^/]+)/$', edit_order),
    (r'order/view/(?P<id>[^/]+)/$', view_order),
    
)

urlpatterns += patterns('',
    url('^showmany/$', showPOManytoMany),
    (r'product/(?P<id>[^/]+)/who_bought$', atom_of_order),

)
