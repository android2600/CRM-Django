from django.shortcuts import render,reverse
import random
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from leads.models import Agent
from .mixins import OrganisorAndLoginRequiredMixin
from .forms import AgentModelForm
from django.core.mail import send_mail

class AgentListView(OrganisorAndLoginRequiredMixin,generic.ListView):
    template_name="agent_list.html"

    def get_queryset(self):
        organization=self.request.user.userprofile
        return Agent.objects.filter(organization=organization)
        #return Agent.objects.all()

class AgentCreateView(OrganisorAndLoginRequiredMixin,generic.CreateView):
    template_name="agent_create.html"
    form_class=AgentModelForm

    def get_success_url(self) -> str:
        return reverse("agents:agent-list")
    
    def form_valid(self,form):
        user=form.save(commit=False)
        user.is_agent=True
        user.is_organisor=False
        user.set_password(f'{random.randint(0,1000000)}')
        user.save()
        Agent.objects.create(
            user=user,
            organization=self.request.user.userprofile
        )
        send_mail(
            subject="You are invited to be an Agent",
            message="You were added as an agent on DJCRM. Please Login to your account to find details.",
            from_email="admin@test.com",
            recipient_list=[user.email]
        )
        # agent.organization= self.request.user.userprofile
        # agent.save()
        return super(AgentCreateView,self).form_valid(form)

class AgentDetailView(OrganisorAndLoginRequiredMixin,generic.DetailView):
    template_name="agent_detail.html"
    context_object_name="agent"

    def get_queryset(self):
        return Agent.objects.all()
    

class AgentUpdateView(OrganisorAndLoginRequiredMixin,generic.UpdateView):
    template_name="agent_update.html"
    form_class=AgentModelForm
    context_object_name="agent"
    def get_success_url(self) -> str:
        return reverse("agents:agent-list")
    
    def get_queryset(self):
        return Agent.objects.all()
    


class AgentDeleteView(OrganisorAndLoginRequiredMixin,generic.DeleteView):
    template_name="agent_delete.html"
    context_object_name="agent"

    def get_success_url(self):
        return reverse("agents:agent-list")
    
    def get_queryset(self):
        organization=self.request.user.userprofile
        print(Agent.objects.filter(organization=organization))
        return Agent.objects.filter(organization=organization)
        #return Agent.objects.all()

