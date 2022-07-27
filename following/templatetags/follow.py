from django import template
from following.models import Following
register = template.Library()


@register.filter
def follow_status_template(me,other):
    value = Following.user_takipcilerim_status(me,other)
    if value:
        return 'Takibi burax'
    return 'Takib et'