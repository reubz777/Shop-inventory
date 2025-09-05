from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from django.db.models import Q, ProtectedError
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import BatchForm
from .models import Batch, Category, Product
from supplies.models import Supplier

class BatchList(ListView):
    model = Batch
    template_name = 'products/products.html'
    context_object_name = 'batches'

    def get_queryset(self):
        queryset = Batch.objects.select_related(
            'product',
            'product__category',
            'product__supplier'
        ).filter(quantity__gt = 0).order_by('-arrival_date')


        filters = Q()

        search_name = self.request.GET.get('search_name')
        if search_name:
            filters &= Q(product__name__icontains=search_name)

        category_id = self.request.GET.get('category')
        if category_id:
            filters &= Q(product__category_id=category_id)

        supplier_id = self.request.GET.get('supplier')
        if supplier_id:
            filters &= Q(product__supplier_id=supplier_id)

        if filters:
            queryset = queryset.filter(filters)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all().order_by('name')
        context['suppliers'] = Supplier.objects.all().order_by('name')
        context['get_params'] = self.request.GET
        return context


class CreateBatch(CreateView):
    model = Batch
    form_class = BatchForm
    template_name = 'products/modal_create.html'
    success_url = reverse_lazy('products:product-list')


class DeleteBatch(DeleteView):
    model = Batch
    template_name = 'products/modal_delete.html'
    success_url = reverse_lazy('products:product-list')
    context_object_name = 'batch'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        try:
            self.object.delete()
            return HttpResponseRedirect(reverse('products:product-list'))

        except ProtectedError as e:
            protected_objects = list(e.protected_objects)
            count = len(protected_objects)

            context = self.get_context_data(
                object=self.object,
                error=(
                    f'Невозможно удалить партию "{self.object}". '
                    f'Она связана с {count} продажами. '
                    f'Сначала удалите связанные продажи.'
                ),
                protected_objects=protected_objects
            )
            return self.render_to_response(context)

class ConsolidationBatch(View):

    def post(self, request, pk):
        
        product = get_object_or_404(Product, id=pk)
        batch = product.batches.order_by('-arrival_date').first()
        batches = product.batches.exclude(quantity=0).exclude(id=batch.id)

        total_quantity = sum(batch.quantity for batch in batches)
        batch.quantity += total_quantity

        batch.save()
        batches.update(quantity=0)


        return redirect('products:product-list')
