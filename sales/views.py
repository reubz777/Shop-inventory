from django.db.models import ExpressionWrapper, F, DecimalField, Count, Sum, Avg, Q
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView
from .forms import SaleCreateForm
from .models import Sale


# Create your views here.
class SaleListView(ListView):
    model = Sale
    template_name = 'sales/sales.html'
    context_object_name = 'sales'
    ordering = ['-sale_date']
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()

        queryset = queryset.select_related('product')

        queryset = queryset.annotate(
            total_price=ExpressionWrapper(
                F('quantity') * F('product__price'),
                output_field=DecimalField(max_digits=10, decimal_places=2)
            )
        )

        search_name = self.request.GET.get('search', None)
        date_start = self.request.GET.get('start_date', None)
        date_end = self.request.GET.get('end_date', None)

        filters = Q()

        if search_name:
            filters &= Q(product__name__icontains=search_name)

        if date_start:
            filters &= Q(sale_date__gte=date_start)

        if date_end:
            filters &= Q(sale_date__lte=date_end)


        if filters:
            queryset = queryset.filter(filters)


        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        stats = Sale.objects.aggregate(
            total_sales=Count('id'),
            total_revenue=Sum(F('product__price') * F('quantity')),
            average_receipt=Avg(F('product__price') * F('quantity')),
        )

        context.update(stats)

        return context


class CreateSaleView(CreateView):
    model = Sale
    form_class = SaleCreateForm
    template_name = 'sales/modal_sale_create.html'
    success_url = reverse_lazy('sales:sales-list')

    def form_valid(self, form):
        sale = form.save(commit = False)

        product = sale.product
        quantity = sale.quantity

        if product.quantity < quantity:
            form.add_error('quantity', f'Недостаточно товара на складе. Доступно: {product.quantity}')
            return self.form_invalid(form)

        product.quantity -=quantity
        product.save()
        sale.save()

        return redirect(self.success_url)
