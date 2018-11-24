from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User

from pyhunter import PyHunter

from .serializers import UserSerializer
from .permissions import IsOwnerOrReadOnly
from restfulapp.dev_settings import EMAIL_HUNTER_API_KEY, CLEARBIT_APY_KEY

import clearbit

class CreateUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        hunter = PyHunter(EMAIL_HUNTER_API_KEY)
        verify = hunter.email_verifier(request.data['email'])
        if verify.get('result', {}) == 'undelivarable':
            return Response(status=status.HTTP_400_BAD_REQUEST)

        clearbit.key = CLEARBIT_APY_KEY
        res = clearbit.Enrichment.find(email=request.data['email'])
        request.data['first_name'] = res['person']['name'].get('givenName', '') if res else ''
        request.data['last_name'] = res['person']['name'].get('familyName', '') if res else ''

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

