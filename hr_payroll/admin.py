from django.apps import apps
from django.contrib import admin


admin.site.site_header = "Nómina"
admin.site.site_title = "Nómina"
admin.site.index_title = "Nómina"


class ListAdminMixin(object):
    def __init__(self, model, admin_site):
        self.list_display = [field.name for field in model._meta.fields]

        self.search_fields = []
        self.list_filter = []

        for field in model._meta.fields:

            if field.get_internal_type() in ('CharField', 'DateField', 'DateTimeField'):
                self.search_fields.append(field.name)

            if field.is_relation or field.get_internal_type() in ('BooleanField', 'DateField', 'DateTimeField'):
                self.list_filter.append(field.name)

        super(ListAdminMixin, self).__init__(model, admin_site)


for app in apps.get_app_configs():
    models = app.get_models()
    for model in models:
        admin_class = type(
            'AdminClass', (ListAdminMixin, admin.ModelAdmin), {})
        try:
            admin.site.register(model, admin_class)
        except admin.sites.AlreadyRegistered:
            pass
