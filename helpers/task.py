from django.conf import settings


def get_estimations():
    # Get estimation mapping for select form for x-editable plugin
    print settings.HOURS_IN_A_DAY
    empty_set = [{'value': 0, 'text': 'Empty'}]
    hours_set = [{'value': h, 'text': '{}h'.format(h)} for h in range(1, settings.HOURS_IN_A_DAY)]
    days_set = [{'value': d * settings.HOURS_IN_A_DAY, 'text': '{}d'.format(d)} for d in range(1, 7)]
    weeks_set = [{'value': w * 7 * settings.HOURS_IN_A_DAY, 'text': '{}w'.format(w)} for w in range(1, 4)]
    return empty_set + hours_set + days_set + weeks_set