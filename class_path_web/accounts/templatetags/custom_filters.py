from django import template

from ..models import Scores

register = template.Library()

@register.filter
def get_scores(student, course):
    scores, _ = Scores.objects.get_or_create(
        student=student,
        course=course
    )
    
    return scores
