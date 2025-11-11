from django import forms
from .models import Livro, Leitor, Emprestimo


class LivroForm(forms.ModelForm):
    class Meta:
        model = Livro
        fields = ["titulo", "autor", "ano_publicacao", "disponivel"]


class LeitorForm(forms.ModelForm):
    class Meta:
        model = Leitor
        fields = ["nome", "email"]


class EmprestimoForm(forms.ModelForm):
    class Meta:
        model = Emprestimo
        fields = ["livro", "leitor"]

    def clean(self):
        cleaned_data = super().clean()
        livro = cleaned_data.get("livro")
        if livro and not livro.disponivel:
            raise forms.ValidationError("Este livro não está disponível para empréstimo.")
        return cleaned_data