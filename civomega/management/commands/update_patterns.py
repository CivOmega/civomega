from django.conf import settings
from django.core.management.base import NoArgsCommand, CommandError

from civomega.codata.models import Module, QuestionPattern, pattern_to_autocomplete_str

class Command(NoArgsCommand):
    help = 'Populates the database with question data from every installed CivOmega module.'

    def handle_noargs(self, **options):
        modules = settings.CIVOMEGA_MODULES
        for pymodule in modules:
            # Do we have a Module record for this software package?
            # If not, we'll initialize one
            mod, created_mod = Module.objects.get_or_create(
                pymodule=pymodule,
                defaults=dict(name=pymodule, status=Module.STATUS_NONE)
            )

            if created_mod:
                print "Created Module(id=%d, pymodule=%s)" % (mod.id, mod.pymodule)
            else:
                print "Loaded Module(id=%d, pymodule=%s)" % (mod.id, mod.pymodule)

            _pymod = __import__(pymodule, globals(), locals(), ['patterns'], -1)
            patterns = _pymod.patterns
            for pattern in patterns.PATTERNS:
                # Do we have a Module record for this software package?
                # If not, we'll initialize one
                pypattern, created_pattern = QuestionPattern.objects.get_or_create(
                    module=mod,
                    pattern_str=pattern,
                    defaults=dict(autocomplete_str=pattern_to_autocomplete_str(pattern))
                )
                if created_mod:
                    print "Created QuestionPattern(id=%d, module=%d, pattern_str=%s, autocomplete_str=%s)" % (
                        pypattern.id, mod.id, pattern, pattern_to_autocomplete_str(pattern))
                else:
                    pypattern.autocomplete_str = pattern_to_autocomplete_str(pattern)
                    pypattern.save()
                    print "Loaded QuestionPattern(id=%d, module=%d, pattern_str=%s, autocomplete_str=%s)" % (
                        pypattern.id, mod.id, pattern, pattern_to_autocomplete_str(pattern))
