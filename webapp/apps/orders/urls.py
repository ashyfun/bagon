from django.urls import path, include

from webapp.apps.orders.views import OrderList


class OrderRouter:

    def __init__(self):
        self.urlpatterns = []

    def register(self, urlpatterns):
        for url, viewset in urlpatterns:
            self.urlpatterns.append(
                path(f'{url.strip(" /")}/', viewset.as_view()),
            )

    @property
    def routes(self):
        return include(self.urlpatterns)


order_router = OrderRouter()
order_router.register([
    (r'orders', OrderList),
])
