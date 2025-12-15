from django.core.exceptions import PermissionDenied

class UserIsOwnerMixin(object):
    def dispatch(self, request, *args, **kwargs):
        instance = self.get_object()

        owner = getattr(instance, "author", None) or getattr(instance, "creator", None)

        if owner is None or owner != self.request.user:
            raise PermissionDenied("You haven't permission for this object")
        return super().dispatch(request, *args, **kwargs)