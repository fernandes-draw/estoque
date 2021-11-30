from django.forms.models import inlineformset_factory
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, resolve_url
from projeto.estoque.forms import EstoqueForm, EstoqueItensForm
from projeto.produto.models import Produto

from .models import Estoque, EstoqueEntrada, EstoqueItens, EstoqueSaida


def estoque_entrada_list(request):
    template_name = "estoque_entrada_list.html"
    objects = EstoqueEntrada.objects.all()
    context = {"object_list": objects}
    return render(request, template_name, context)


def estoque_entrada_detail(request, pk):
    template_name = "estoque_entrada_detail.html"
    obj = EstoqueEntrada.objects.get(pk=pk)
    context = {"object": obj}
    return render(request, template_name, context)


def dar_baixa_estoque(form):
    """Pega os produtos a partir da instância do formulário (Estoque)"""
    produtos = form.estoques.all()
    for item in produtos:
        produto = Produto.objects.get(pk=item.produto.pk)
        produto.estoque = item.saldo
        produto.save()
    print("Estoque atualizado com sucesso!")
    return


def estoque_add(request, template_name, movimento, url):
    estoque_form = Estoque()
    item_estoque_form = inlineformset_factory(
        Estoque,
        EstoqueItens,
        form=EstoqueItensForm,
        extra=0,
        min_num=1,
        validate_min=True,
    )
    if request.method == "POST":
        form = EstoqueForm(request.POST, instance=estoque_form, prefix="main")
        formset = item_estoque_form(
            request.POST,
            instance=estoque_form,
            prefix="estoque",
        )
        if form.is_valid() and formset.is_valid():
            form = form.save()
            form.movimento = movimento
            form.save()
            formset.save()
            dar_baixa_estoque(form)
            return {"pk": form.pk}  # HttpResponseRedirect(resolve_url(url, form.pk))
    else:
        form = EstoqueForm(instance=estoque_form, prefix="main")
        formset = item_estoque_form(
            instance=estoque_form,
            prefix="estoque",
        )
    context = {"form": form, "formset": formset}
    return context


def estoque_entrada_add(request):
    template_name = "estoque_entrada_form.html"
    movimento = "e"
    url = "estoque:estoque_entrada_detail"
    context = estoque_add(request, template_name, movimento, url)
    if context.get("pk"):
        return HttpResponseRedirect(resolve_url(url, context.get("pk")))
    return render(request, template_name, context)


def estoque_saida_list(request):
    template_name = "estoque_saida_list.html"
    objects = EstoqueSaida.objects.all()
    context = {"object_list": objects}
    return render(request, template_name, context)


def estoque_saida_detail(request, pk):
    template_name = "estoque_saida_detail.html"
    obj = EstoqueSaida.objects.get(pk=pk)
    context = {"object": obj}
    return render(request, template_name, context)


def estoque_saida_add(request):
    template_name = "estoque_saida_form.html"
    movimento = "s"
    url = "estoque:estoque_saida_detail"
    context = estoque_add(request, template_name, movimento, url)
    if context.get("pk"):
        return HttpResponseRedirect(resolve_url(url, context.get("pk")))
    return render(request, template_name, context)
