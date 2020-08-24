import string

from django.core.exceptions import FieldError
from django.db.models import SlugField
from django.utils.crypto import get_random_string


class RandomSlugField(SlugField):
    """Random ASCII based slug."""

    def __init__(self, length, *args, **kwargs):
        kwargs.setdefault('blank', True)
        kwargs.setdefault('editable', False)
        kwargs.setdefault('unique', True)
        kwargs.setdefault('max_length', length)

        self.length = length
        self.chars = string.ascii_lowercase + string.digits

        super(RandomSlugField, self).__init__(*args, **kwargs)

    def generate_slug(self, model_instance):
        queryset = model_instance.__class__._default_manager.all()

        # Only count slugs that match current length to prevent issues when
        # pre-existing slugs are a different length.
        lookup = {'{}__regex'.format(self.attname): r'^.{{{}}}$'.format(self.length)}
        if queryset.filter(**lookup).count() >= len(self.chars) ** self.length:
            raise FieldError('No available slugs remaining.')

        slug = get_random_string(self.length, self.chars)

        # Exclude the current model instance from the queryset used in finding
        # next valid slug.
        if model_instance.pk:
            queryset = queryset.exclude(pk=model_instance.pk)

        # Form a kwarg dict used to implement any unique_together constraints.
        kwargs = {}
        for params in model_instance._meta.unique_together:
            if self.attname in params:
                for param in params:
                    kwargs[param] = getattr(model_instance, param, None)
        kwargs[self.attname] = slug

        # Ensure the uniqueness of the slug.
        while queryset.filter(**kwargs):
            slug = get_random_string(self.length, self.chars)
            kwargs[self.attname] = slug

        return slug

    def pre_save(self, model_instance, add):
        value = getattr(model_instance, self.attname)
        if not value:
            value = self.generate_slug(model_instance)
            setattr(model_instance, self.attname, value)

        return value

    def deconstruct(self):
        name, path, args, kwargs = super(RandomSlugField, self).deconstruct()
        kwargs['length'] = self.length

        return name, path, args, kwargs
