import aiohttp
from fastapi import Request, Response, status
import json

from .network import make_request
from .settings import *


async def route(request: Request):
    request_path = request.get('path')
    method = request.get('method').lower()
    headers = request.headers
    payload = await request.body()

    main_service_urls = ('/counterparties', '/movements', '/orders', '/procurements', '/tmvs', '/warehouses')
    auth_service_urls = ('/auth', '/users')
    authentication_required = False
    if request_path.startswith(main_service_urls):
        authentication_required = True
        service_url = f'{settings.MAIN_SERVICE_URL}{request_path}'
    elif request_path.startswith(auth_service_urls):
        service_url = f'{settings.AUTH_SERVICE_URL}{request_path}'
        if request_path == '/users' and method == 'get':
            authentication_required = True

    if authentication_required:
        verification_service_url = f'{settings.AUTH_SERVICE_URL}/auth/verify'
        token_data = {'token': headers['authorization'].split(' ')[1]}
        response_data, status_code_from_service = \
            await make_request(url=f'{verification_service_url}', method='post', headers={}, data=token_data)

        if status_code_from_service == 401:
            response_data = json.dumps(response_data)
            return Response(content=response_data, status_code=status_code_from_service, media_type='application/json')

    try:
        service_response_data, service_response_status = await make_request(
            url=service_url,
            method=method,
            headers=headers,
            data=payload
        )
    except aiohttp.client_exceptions.ContentTypeError:
        return Response(
            content=json.dumps({'detail': 'Service error.'}),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            media_type='application/json'
        )
    except aiohttp.client_exceptions.ClientConnectorError:
        return Response(
            content=json.dumps({'detail': 'Service is unavailable.'}),
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            media_type='application/json'
        )
    else:
        return Response(
            content=json.dumps(service_response_data),
            status_code=service_response_status,
            media_type='application/json')
