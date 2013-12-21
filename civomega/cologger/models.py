from django.db import models

class QuestionLog(models.Model):
    content = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    user_id = models.ForeignKey('auth.User', null=True)

    # "null" if question wasn't answerable
    answer = models.ForeignKey('cologger.AnswerLog', null=True)

    # use this as a flag of some sort
    STATUS_NONE = 0
    STATUS_CHOICES = (
        (STATUS_NONE, 'No status'),
    )
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES,
        default=0)

class AnswerLog(models.Model):
    content = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)

    module = models.ForeignKey('codata.Module')
    load_time = models.DecimalField(max_digits=5, decimal_places=2) # max 999.99

    # use this as a flag of some sort
    STATUS_NONE = 0
    STATUS_CHOICES = (
        (STATUS_NONE, 'No status'),
    )
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES,
        default=0)
