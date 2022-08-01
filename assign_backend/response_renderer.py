from rest_framework.utils import json
from rest_framework.renderers import BaseRenderer


class CustomResponseRenderer(BaseRenderer):
    media_type = 'application/json'
    format = 'txt'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = {
            'status': renderer_context['response'].status_code,
            'message': None,
            'data': None,
            'error': None
        }

        if data.get('message'):
            response['message'] = data.get('message')
        if data.get('data'):
            response['data'] = data.get('data')
        if data.get('error'):
            response['error'] = data.get('error')
        elif 'ErrorDetail' in str(data):
            response['error'] = data

        return json.dumps(response)
