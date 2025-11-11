from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django_filters.views import FilterView

from .models import Livro, Leitor, Emprestimo
from .forms import LivroForm, LeitorForm, EmprestimoForm
from .filters import LivroFilter


@login_required
def home(request):
    contagem = {
        "livros": Livro.objects.count(),
        "leitores": Leitor.objects.count(),
        "emprestimos": Emprestimo.objects.count(),
    }
    return render(request, "home.html", {"contagem": contagem})


class LivroListView(LoginRequiredMixin, FilterView):
    model = Livro
    filterset_class = LivroFilter
    template_name = "livros/list.html"
    context_object_name = "livros"
    paginate_by = 20


class LivroCreateView(LoginRequiredMixin, CreateView):
    model = Livro
    form_class = LivroForm
    template_name = "livros/form.html"
    success_url = reverse_lazy("livro_list")

    def form_valid(self, form):
        messages.success(self.request, "Livro cadastrado com sucesso.")
        return super().form_valid(form)


class LivroUpdateView(LoginRequiredMixin, UpdateView):
    model = Livro
    form_class = LivroForm
    template_name = "livros/form.html"
    success_url = reverse_lazy("livro_list")

    def form_valid(self, form):
        messages.success(self.request, "Livro atualizado com sucesso.")
        return super().form_valid(form)


class LivroDeleteView(LoginRequiredMixin, DeleteView):
    model = Livro
    template_name = "livros/confirm_delete.html"
    success_url = reverse_lazy("livro_list")

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Livro excluído com sucesso.")
        return super().delete(request, *args, **kwargs)


class LeitorListView(LoginRequiredMixin, ListView):
    model = Leitor
    template_name = "leitores/list.html"
    context_object_name = "leitores"
    paginate_by = 20


class LeitorCreateView(LoginRequiredMixin, CreateView):
    model = Leitor
    form_class = LeitorForm
    template_name = "leitores/form.html"
    success_url = reverse_lazy("leitor_list")

    def form_valid(self, form):
        messages.success(self.request, "Leitor cadastrado com sucesso.")
        return super().form_valid(form)


class LeitorUpdateView(LoginRequiredMixin, UpdateView):
    model = Leitor
    form_class = LeitorForm
    template_name = "leitores/form.html"
    success_url = reverse_lazy("leitor_list")

    def form_valid(self, form):
        messages.success(self.request, "Leitor atualizado com sucesso.")
        return super().form_valid(form)


class LeitorDeleteView(LoginRequiredMixin, DeleteView):
    model = Leitor
    template_name = "leitores/confirm_delete.html"
    success_url = reverse_lazy("leitor_list")

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Leitor excluído com sucesso.")
        return super().delete(request, *args, **kwargs)


class EmprestimoListView(LoginRequiredMixin, ListView):
    model = Emprestimo
    template_name = "emprestimos/list.html"
    context_object_name = "emprestimos"
    paginate_by = 20


class EmprestimoCreateView(LoginRequiredMixin, CreateView):
    model = Emprestimo
    form_class = EmprestimoForm
    template_name = "emprestimos/form.html"
    success_url = reverse_lazy("emprestimo_list")

    def form_valid(self, form):
        response = super().form_valid(form)
        # Marcar livro como indisponível
        emprestimo = self.object
        livro = emprestimo.livro
        if livro.disponivel:
            livro.disponivel = False
            livro.save()
            messages.success(self.request, "Empréstimo registrado com sucesso.")
        else:
            messages.error(self.request, "Este livro não está disponível.")
            return redirect("emprestimo_create")
        return response


@login_required
def devolver_emprestimo(request, pk):
    emprestimo = get_object_or_404(Emprestimo, pk=pk)
    if emprestimo.data_devolucao:
        messages.info(request, "Este empréstimo já foi devolvido.")
    else:
        emprestimo.data_devolucao = timezone.now().date()
        emprestimo.save()
        livro = emprestimo.livro
        livro.disponivel = True
        livro.save()
        messages.success(request, "Devolução registrada com sucesso.")
    return redirect("emprestimo_list")
