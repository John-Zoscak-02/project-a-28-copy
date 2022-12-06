from django import template

register = template.Library()


@register.filter
def in_schedule(course_number, class_list):
    for c in class_list:
        if c.section_number == int(course_number):
            return 1
    return 0
