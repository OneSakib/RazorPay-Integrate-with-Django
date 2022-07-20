from django.shortcuts import render
from django.views.generic import TemplateView, FormView, View
from .forms import CoffeeForm, Coffee
import razorpay
from django.conf import settings


# Create your views here.
class IndexView(FormView):
    template_name = 'RazorPay/index.html'
    form_class = CoffeeForm
    success_url = '/'

    def form_valid(self, form):
        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        contact = form.cleaned_data['contact']
        address = form.cleaned_data['address']
        amount = int(form.cleaned_data['amount']) * 100
        # razorpay payment
        # client_key = "rzp_test_XB0DStFIyKrvv6"
        # secret_key = "q7i7bsYmBEi0x6U49EKGtIRO"
        client_key = settings.RAZORPAY_CLIENT_ID
        secret_key = settings.RAZORPAY_SECRET_ID

        client = razorpay.Client(auth=(client_key, secret_key))
        data = {"amount": amount, "currency": "INR", "receipt": "order_rcptid_11"}
        payment = client.order.create(data=data)
        form.instance.order_id = payment['id']
        if form.is_valid():
            context = {
                'form': form,
                'client_key': client_key,
                'payment': payment,
                'name': name,
                'email': email,
                'contact': contact,
                'address': address
            }
            form.save()
            return render(self.request, 'RazorPay/index.html', context)
        return super(IndexView, self).form_valid(form)


class SuccessView(View):
    def get(self, request):
        razorpay_payment_id = request.GET.get('razorpay_payment_id')
        razorpay_signature = request.GET.get('razorpay_signature')
        razorpay_order_id = request.GET.get('razorpay_order_id')
        try:
            obj = Coffee.objects.get(order_id__exact=razorpay_order_id)
            obj.payment_id = razorpay_payment_id
            obj.signature_id = razorpay_signature
            client = razorpay.Client(auth=(settings.RAZORPAY_CLIENT_ID, settings.RAZORPAY_SECRET_ID))
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': razorpay_payment_id,
                'razorpay_signature': razorpay_signature
            }
            check = client.utility.verify_payment_signature(params_dict)
            if check:
                obj.paid = True
                obj.save()
            else:
                raise ValueError
            context = {
                'obj': obj
            }
            return render(request, 'RazorPay/success.html', context)
        except Exception as e:
            code = request.GET.get('code')
            description = request.GET.get('description')
            source = request.GET.get('source')
            step = request.GET.get('step')
            reason = request.GET.get('reason')
            order_id = request.GET.get('order_id')
            payment_id = request.GET.get('payment_id')
            context = {
                'obj': e,
                'code': code,
                'description': description,
                'source': source,
                'step': step,
                'reason': reason,
                'order_id': order_id,
                'payment_id': payment_id
            }
            return render(request, 'RazorPay/pay_error.html', context)
