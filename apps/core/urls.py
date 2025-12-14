from rest_framework.routers import DefaultRouter

from apps.core import views

router = DefaultRouter()

router.register('companies', views.CompanyViewSet, 'companies')
router.register('queues', views.QueueViewSet, 'queues')
router.register('queue-entries', views.QueueEntryViewSet, 'queue-entries')

urlpatterns = router.get_urls()
