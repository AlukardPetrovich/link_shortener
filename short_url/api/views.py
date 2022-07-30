import time

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from nanoid import generate
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from api.models import TargetURL, UserMetaInfo
from api.serializers import TargetURLSerializer
from short_url.settings import DOMAIN_NAME, URL_LENGTH


@api_view(['POST', ])
def post_full_url(request):
    current_ip = request.META['REMOTE_ADDR']
    current_user_agent = request.META['HTTP_USER_AGENT']
    user = request.user
    if not UserMetaInfo.objects.filter(
        user=user,
        ip=current_ip,
        user_agent=current_user_agent
    ).exists():
        UserMetaInfo.objects.create(
            user=user,
            ip=current_ip,
            user_agent=current_user_agent
        )
    full_url = request.data['full_url']
    check = TargetURL.objects.filter(
        full_url=full_url,
        lifetime__gt=time.time()
    )
    if len(check) > 0:
        serializer = TargetURLSerializer(check[0])
        return Response(serializer.data, status=status.HTTP_200_OK)
    lifetime = request.data['lifetime']
    short_url = DOMAIN_NAME + '/' + generate(size=URL_LENGTH)
    serializer = TargetURLSerializer(data={
        'full_url': full_url,
        'lifetime': lifetime,
        'short_url': short_url
    })
    if serializer.is_valid(raise_exception=True):
        serializer.validated_data['lifetime'] = (
            int(time.time()) + serializer.validated_data['lifetime']
        )
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors)


@api_view(['GET', ])
@permission_classes([AllowAny, ])
def get_full_url(request):
    short_url = DOMAIN_NAME + request.get_full_path()
    target_url = get_object_or_404(TargetURL, short_url=short_url)
    serializer = TargetURLSerializer(target_url)
    print(serializer.data['full_url'])
    return HttpResponseRedirect(redirect_to=serializer.data['full_url'])
