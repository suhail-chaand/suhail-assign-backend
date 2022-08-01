from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView
from .models import Product
from .serializers import ProductSerializer


class ProductView(RetrieveAPIView):
    serializer_class = ProductSerializer

    def get(self, request, *args, **kwargs):
        try:
            product = Product.objects.get(id=kwargs['pk'])

            serializer = self.serializer_class(product)

            response = {
                'message': 'Product fetched successfully!',
                'data': serializer.data
            }
            return Response(response, status=status.HTTP_200_OK)
        except KeyError:
            response = {
                'message': 'Product ID not specified!',
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
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
