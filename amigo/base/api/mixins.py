# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals


class ListSerializerMixin(object):
    """
    Add custom serializer for list view
    """
    def get_serializer_class(self):
        if self.action == "list" and hasattr(self, "list_serializer_class"):
            return self.list_serializer_class

        return super(ListSerializerMixin, self).get_serializer_class()
