from django.views import generic

from roster.models import Resident, GovboardPosition, GovboardMember

class PeopleView(generic.ListView):
    template_name = 'roster/people.html'
    context_object_name = 'roster'

    def get_queryset(self):
        return Resident.objects.all()

class GovboardView(generic.ListView):
    template_name = 'roster/govboard.html'
    context_object_name = 'govboard'

    def get_queryset(self):
        return GovboardPosition.objects.all()

    def get_context_data(self, **kwargs):
        context = super(GovboardView, self).get_context_data(**kwargs)
        context['seplen'] = len(self.get_queryset())/2
        return context