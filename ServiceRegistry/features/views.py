# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models import Count
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import list_route

from .serializers import ServiceAddSerializer, ServiceRetriveSerializer

from .models import Service


class ServiceViewSet(viewsets.ViewSet):
    """
    It's return servics, add and update service records and also return search records.
    Now following end points of this view set.
        ***
            route url is : /api/v1/
            endpoints are : 
            **    /services/
            **    /services/search-services-without-version/
            **    /services/search-services-with-version/
        ***

        Following below method accpeted:
        ***
            get, post, put, delete

        ***
    """
    serializer_class = ServiceRetriveSerializer

    def list(self, request):
        """
        It's return all service records and endpoints of the API is
            ***
                Endpoints : /services/
                Accepted method : GET
            ***
        """
        queryset = Service.objects.exclude(change='removed')
        serializer = self.serializer_class(queryset, many=True)

        return Response({
            'status': status.HTTP_200_OK,
            'message': 'List of service records.',
            'data': serializer.data
        })
    

    @list_route( methods=['get'], url_path='search-services-with-version')
    def search_service_with_version(self, request):
        """
        It's return all service records on search records basesand endpoints of 
        the API is
            ***
                Endpoints : /services/search-services-with-version/
                Accepted method : GET
                Required param : service and version
            ***
        """
        service = request.GET.get('service')
        version = request.GET.get('version')
        
        if service and version:
            services = Service.objects.filter(version=version, service=service).exclude(
                    change='removed').values('service', 'version').annotate(count=Count('service'))

            services = services[0] if services else {'service' : service, 'version' : version, 'count': 0}
            
            return Response({
                    'status': status.HTTP_200_OK,
                    'message': 'List of service records.',
                    'data': services
                })

        return Response({
                'status': status.HTTP_400_BAD_REQUEST,
                'message': 'send service and version name',
            })

    @list_route( methods=['get'], url_path='search-services-without-version')
    def search_service_without_version(self, request):
        """
        It's return all service records on search records basesand endpoints of 
        the API is
            ***
                Endpoints : /services/search-services-without-version/
                Accepted method : GET
                Required param : service
            ***
        """
        service = request.GET.get('service')
        
        if service:
            services = Service.objects.filter(service=service).exclude(
                    change='removed').values('service').annotate(count=Count('service'))

            services = services[0] if services else {'service' : service, 'count': 0}

            
            return Response({
                    'status': status.HTTP_200_OK,
                    'message': 'List of service records.',
                    'data': services
                })

        return Response({
                'status': status.HTTP_400_BAD_REQUEST,
                'message': 'send service name.',
            })

    def update(self, request, pk):
        """
        It's update service records on service ID bases, it's endpoint of the API
            ***
                Endpoints : /services/id/
                Accepted method : PUT
                Required param : Id
                requried form param is : service and version
            ***
        """
        add_serializer = ServiceAddSerializer
        
        try:
            service = Service.objects.get(id=pk)
        except Service.DoesNotExist as e:
            service = None
        
        if service:
            serializer = add_serializer(data=request.data, instance=service)

            if serializer.is_valid():
                service = serializer.save()
                service.change = 'changed'
                service.save()
                services = Service.objects.filter(id=service.id)
                serializer = add_serializer(services, many=True)

                return Response({
                    'status': status.HTTP_201_CREATED,
                    'message': 'Successfully service updated.',
                    'data': serializer.data })

            return Response({
                'status': status.HTTP_400_BAD_REQUEST,
                'message': 'Please provided required fields.',
                'error' : serializer.errors
            })

        return Response({
                'status': status.HTTP_404_NOT_FOUND,
                'message': 'Related id has no record.',
            })

    def create(self, request):
        """
        It's create service record, endpoint of the API is
            ***
                Endpoints : /services/
                Accepted method : POST
                requried form param is : service and version
            ***
        """
        add_serializer = ServiceAddSerializer

        serializer = add_serializer(data=request.data)
        
        if serializer.is_valid():
            service = serializer.save()
            services = Service.objects.filter(id=service.id)
            serializer = add_serializer(services, many=True)

            return Response({
                'status': status.HTTP_201_CREATED,
                'message': 'Successfully service created.',
                'data': serializer.data })

        return Response({
            'status': status.HTTP_400_BAD_REQUEST,
            'message': 'Please provided required fields.',
            'error' : serializer.errors
        })

    def destroy(self, request, pk=None):
        """
        It's delete service records on service ID bases, it's endpoint of the API
            ***
                Endpoints : /services/id/
                Accepted method : DELETE
                Required param : Id
            ***
        """
        try:
            service = Service.objects.get(id=pk)
        except Service.DoesNotExist as e:
            service = None
        
        if service:
            service.archeive = True
            service.change = 'removed'
            service.save()
            
            record = {'service' : service.service, 'change' : service.change}

            return Response({
                'status': status.HTTP_200_OK,
                'message': 'Successfully removed service.',
                'data': record
            })

        return Response({
            'status': status.HTTP_404_NOT_FOUND,
            'message': 'Related id has no record.',
        })