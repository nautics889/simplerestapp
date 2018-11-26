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
        #check email by EmailHunter
        #if it's failed, send status 400
        hunter = PyHunter(EMAIL_HUNTER_API_KEY)
        verify = hunter.email_verifier(request.data['email'])
        if verify.get('result', {}) == 'undelivarable':
            return Response(status=status.HTTP_400_BAD_REQUEST)

        #enrich account by first name and last name using clearbit
        clearbit.key = CLEARBIT_APY_KEY
        res = clearbit.Enrichment.find(email=request.data['email'])
        try:
            request.data['first_name'] = res['person']['name'].get('givenName', '')
            request.data['last_name'] = res['person']['name'].get('familyName', '')
        except (TypeError, KeyError):
            #if enrichment is failed, set fields as empty strings
            request.data['first_name'] = request.data['last_name'] = ''

        #serialize data from request
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        #and create a user
        self.perform_create(serializer)

        #define headers and respond to client
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

