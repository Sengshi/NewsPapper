from django import template

register = template.Library()


@register.filter(name='censor')
def censor(value):
    words = value.split()
    count = 0
    while count < len(words):
        if "test" in words[count].lower():
            words[count] = "<censor>"
        count += 1
    return " ".join(words)

