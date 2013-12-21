from django.db import models

class DataSource(models.Model):
    """ A datasource, such as an external API. """
    name = models.CharField(max_length=200)
    url = models.URLField()
    description = models.TextField(null=True)

    created = models.DateTimeField(auto_now_add=True)

    # TODO disabled, etc
    STATUS_NONE = 0
    STATUS_CHOICES = (
        (STATUS_NONE, 'No status'),
    )
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES,
        default=0)


    def __unicode__(self):
        return self.name


# TODO
#class QuestionPattern(models.Model):
#


class Module(models.Model):
    """ Responsible for answering a single category of question """
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(null=True)

    data_sources = models.ManyToManyField('codata.DataSource')

    # TODO disabled, etc
    STATUS_NONE = 0
    STATUS_CHOICES = (
        (STATUS_NONE, 'No status'),
    )
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES,
        default=0)

    # TODO
    #patterns = models.ManyToManyField('civomega.data.QuestionPattern')

    def __unicode__(self):
        return self.name
