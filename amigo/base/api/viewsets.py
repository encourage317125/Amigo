# Third Party Stuff
from rest_framework import viewsets as drf_viewsets

from .mixins import ListSerializerMixin


class ViewSet(ListSerializerMixin, drf_viewsets.ViewSet):
    """
    The base ViewSet class does not provide any actions by default.
    """
    pass


class ModelCrudViewSet(ListSerializerMixin, drf_viewsets.ModelViewSet):
    pass
