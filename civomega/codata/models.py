# coding=utf-8
from django.db import models
from importlib import import_module

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


class Module(models.Model):
    """ Responsible for answering a single category of question """
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(null=True)

    # name of the python module we'll need to import (and have installed)
    # to actually execute and answer this class of question
    pymodule = models.CharField(max_length=40)

    # TODO
    # for when we get fancy in the future (and don't rely on manually forking
    # and installing modules), we could maybe automate the pip install step
    # by sort of including the requirement string here?
    #git_url = models.CharField(...)

    data_sources = models.ManyToManyField('codata.DataSource')

    # TODO disabled, etc
    STATUS_NONE = 0
    STATUS_CHOICES = (
        (STATUS_NONE, 'No status'),
    )
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES,
        default=0)

    def __unicode__(self):
        return self.name

    def render_answer_html(self, answer_data):
        # simulate "from MODULENAME import parser" and dynamically load
        # the python library defined in this module (pymodule)
        _mod = __import__(self.pymodule, globals(), locals(), ['parser'], -1)
        parser = _mod.parser

        return parser.render_answer_html(answer_data)

    def render_answer_json(self, answer_data):
        # simulate "from MODULENAME import parser" and dynamically load
        # the python library defined in this module (pymodule)
        _mod = __import__(self.pymodule, globals(), locals(), ['parser'], -1)
        parser = _mod.parser

        return parser.render_answer_json(answer_data)


class QuestionPattern(models.Model):
    module = models.ForeignKey('codata.Module')
    pattern_str = models.CharField(max_length=200)

    def answer(self, args):
        # simulate "from MODULENAME import parser" and dynamically load
        # the python library defined in this pattern's module (see
        # Module.pymodule, above)
        _mod = __import__(module.pymodule, globals(), locals(), ['parser'], -1)
        parser = _mod.parser

        return parser.answer_pattern(self.pattern_str, args)
