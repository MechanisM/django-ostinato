from django.contrib.contenttypes.models import ContentType
from django.conf import settings


OSTINATO_PAGE_TEMPLATES = getattr(settings, 'OSTINATO_PAGE_TEMPLATES')


def get_template_by_name(template_name):
    for template in OSTINATO_PAGE_TEMPLATES:
        if template['name'] == template_name:
            return template
    raise Exception('Ostinato Page Template, %s, does not exist.' % template_name)


def get_zones_for(page):
    template = get_template_by_name(page.template)

    zones = []
    for index, zone in enumerate(template['zones']):
        zone_id = zone[0]
        app_label = zone[1].split('.')[0]
        model = zone[1].split('.')[1]

        ct = ContentType.objects.get(app_label=app_label, model=model)
        instance, created = ct.model_class().objects.get_or_create(
            page=page, zone_id=zone_id)

        zones.append(instance)

    return zones


def get_page_zone_by_id(page, zone_id):
    zones = get_zones_for(page)
    for z in zones:
        if z.zone_id == zone_id:
            return z

