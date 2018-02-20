from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def clean_phone(value):
    if not value is None:
        dig = [str(x) for x in range(10)]
        # print (dig)
        for c in value:
          # print (c)
          if not c in dig:
                raise ValidationError(_('%(value)s Contians charachters, only digits are allowed!'),
                                      params={'value': value},)
    # return value
