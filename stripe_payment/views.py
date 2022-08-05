from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.generics import GenericAPIView
import stripe
from product.models import (
                            Product,
                            Image
                        )
from .serializers import (
                        OrderSerializer,
                        CreateCheckoutSessionSerializer
                    )

stripe.api_key = settings.STRIPE_SECRET_KEY


# Create your views here.
class CreateCheckoutSessionView(GenericAPIView):
    serializer_class = CreateCheckoutSessionSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=False):
            try:
                product = Product.objects.get(id=serializer.data.get('product_id'))
                images = Image.objects.filter(product_id=product.id)

                checkout_session = stripe.checkout.Session.create(
                    line_items=[
                        {
                            'price_data': {
                                'currency': 'usd',
                                'unit_amount': int(product.price) * 100,
                                'product_data': {
                                    'name': product.name,
                                    'images': [image.image_url for image in images[0:1]]
                                }
                            },
                            'quantity': serializer.data.get('quantity')
                        }
                    ],
                    metadata={
                        'product_id': product.id,
                        'quantity': serializer.data.get('quantity'),
                        'price': int(product.price) * 100,
                    },
                    mode='payment',
                    payment_method_types=['card'],
                    billing_address_collection='required',
                    success_url=f'http://localhost:4200/product-details/{product.id}?purchase=success',
                    cancel_url=f'http://localhost:4200/product-details/{product.id}',
                )
                response = {
                    'message': 'Stripe checkout session created successfully!',
                    'data': {
                        'publishable_key': settings.STRIPE_PUBLISHABLE_KEY,
                        'session_id': checkout_session.id
                    }
                }
                return Response(response, status=status.HTTP_200_OK)
            except Product.DoesNotExist:
                response = {
                    'message': 'Product does not exist!'
                }
                return Response(response, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                response = {
                    'message': 'Operation failed!',
                    'error': str(e)
                }
                return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            response = {
                'message': 'Invalid request payload!',
                'error': serializer.errors
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['POST'])
def session_completed_webhook(request):
    event = None
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_KEY
        )
    except ValueError as e:
        response = {
            'message': 'Invalid request payload!',
            'error': str(e)
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
    except stripe.error.SignatureVerificationError as e:
        response = {
            'message': 'Stripe signature could not be verified.',
            'error': str(e)
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    if event['type'] == 'checkout.session.completed':
        session_data = event['data']['object']
        session_metadata = session_data['metadata']
        customer_details = session_data['customer_details']

        order_data = {
            'product_id': session_metadata['product_id'],
            'unit_price': session_metadata['price'],
            'quantity': session_metadata['quantity'],
            'payment_status': session_data['payment_status'],
            'customer_email': customer_details['email'],
            'customer_name': customer_details['name'],
            'customer_address': f'''{customer_details["address"]["line1"]}, 
                                        {customer_details["address"]["line2"]}, 
                                        {customer_details["address"]["city"]}, 
                                        {customer_details["address"]["state"]}, 
                                        {customer_details["address"]["country"]}''',
            'customer_zipcode': customer_details["address"]["postal_code"]
        }

        serializer = OrderSerializer(data=order_data)
        if serializer.is_valid():
            serializer.save()
            response = {
                'message': 'Order details saved!'
            }
            return Response(response, status=status.HTTP_200_OK)
        else:
            response = {
                'message': 'Invalid request payload!',
                'error': serializer.errors
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
    else:
        response = {
            'message': 'Session incomplete!',
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
