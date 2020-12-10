from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.forms import inlineformset_factory
from crispy_forms.helper import FormHelper
from .models import Bucket, Item, Identifier, IdentifierType
from .forms import ItemForm, IdentifierForm, BucketItemForm, SearchForm
import logging


# @login_required()
def index(request):
    buckets = {b: Item.objects.filter(bucket=b) for b in Bucket.objects.all()}
    identifier_types = {i.id: i.name
                        for i in IdentifierType.objects.all()}
    identifier_types.update({0: 'Name'})

    # for the new item form
    item = Item()
    IdentifierFormSet = inlineformset_factory(
        Item,
        Identifier,
        form=IdentifierForm,
        fields=('type', 'value'),
        can_delete=False,
        extra=0
    )

    context = {
        'bucket_list': buckets,
        'identifier_types': identifier_types,
        'item_form': ItemForm(instance=item),
        'formset': IdentifierFormSet(instance=item),
        'search_form': SearchForm()
    }

    return render(request, 'inventory/index.html', context)


# @login_required
def bucket(request, bucket_id):
    bucket = get_object_or_404(Bucket, pk=bucket_id)
    items = Item.objects.filter(bucket=bucket)
    buckets = Bucket.objects.all().exclude(pk=bucket_id)

    # for the new item form
    item = Item()
    item.bucket = bucket
    IdentifierFormSet = inlineformset_factory(
        Item,
        Identifier,
        form=IdentifierForm,
        fields=('type', 'value'),
        can_delete=False,
        extra=0
    )

    context = {
        'bucket': bucket,
        'item_list': items,
        'bucket_list': buckets,
        'item_form': BucketItemForm(instance=item),
        'formset': IdentifierFormSet(instance=item),
        'search_form': SearchForm()
    }

    return render(request, 'inventory/bucket.html', context)


def add(request, bucket_id=None):
    item = ItemForm(request.POST)

    # check item validity, but don't save just yet
    if item.is_valid():
        item = item.save(commit=False)
    else:
        context = {
            'error_text': 'Invalid Item: ' + item.errors.as_json()
        }
        return render(request, 'inventory/error.html', context)

    IdentifierForm = inlineformset_factory(
        Item,
        Identifier,
        fields=('type', 'value'),
        can_delete=False,
    )
    identifier = IdentifierForm(request.POST, instance=item)

    # check identifier(s) validity, save item and identifier(s)
    if identifier.is_valid():
        item.save()
        identifier.save()
    else:
        context = {
            'error_text': 'Invalid Identifier: ' + identifier.errors.as_json(escape_html=False)
        }
        return render(request, 'inventory/error.html', context)

    # send user to reasonable view
    if bucket_id:
        return redirect('inventory:bucket', bucket_id=bucket_id)

    return redirect('inventory:index')


def item(request, item_id):
    return render(request, 'inventory/item.html')


def move(request, item_id, bucket_id):
    item = get_object_or_404(Item, pk=item_id)
    bucket = get_object_or_404(Bucket, pk=bucket_id)
    return_path = request.GET['return']

    # move to new bucket and save
    old_id = item.bucket.id
    item.bucket = bucket
    item.save()

    # send user to reasonable view
    if 'bucket' in return_path:
        return redirect('inventory:bucket', bucket_id=old_id)

    return redirect('inventory:index')


def search(request):
    search = SearchForm(request.POST)
    context = {
        'bucket_list': Bucket.objects.all(),
        'search_form': search,
        'bucket_as_property': True
    }

    if search.is_valid():
        # special case: search by name
        if search.cleaned_data['search_property'] == 0:
            context['item_list'] = Item.objects.filter(
                name__contains=search.cleaned_data['search_keyword']
            )
        else:
            context['item_list'] = Item.objects.filter(
                identifier__type=search.cleaned_data['search_property'],
                identifier__value=search.cleaned_data['search_keyword']
            )

    return render(request, 'inventory/search.html', context)
