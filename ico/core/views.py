from rest_framework.views import APIView, Response
from django.shortcuts import render
from ico.core.utils import make_response
from rest_framework import status
from rest_framework.exceptions import ValidationError

from rest_framework.parsers import MultiPartParser, FormParser

from rest_framework.permissions import IsAuthenticated

from django.db import transaction

from django.conf import settings

from datetime import datetime

import os

from rest_framework import viewsets
from .models import Query, Version, Worker, QueryFile, HandleVersion
from .serializers import QuerySerializer, VersionSerializer, WorkerSerializer, QueryFileSerializer, HandleVersionSerializer

class WorkerView(APIView):
    """
    """
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            worker_serialized = WorkerSerializer(data=request.data)
            if worker_serialized.is_valid(raise_exception=True):
                worker_serialized.save()
            else:
                return make_response(status_message="errors.catastrophe", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, status_params=worker_serialized.errors)
        except ValidationError as error:
            params = {}
            for (value, message) in error.detail.items():
                params[value] = message[0].code
            return make_response(status_message="errors.missing-parameters", status_code=status.HTTP_400_BAD_REQUEST, status_params=params)

        return make_response(status_code=status.HTTP_201_CREATED, status_message="errors.none", data=worker_serialized.data)
    
    def get(self, request, user_id):
        try:
            worker_obj = Worker.objects.get(user=user_id)
        except Worker.DoesNotExist:
            return make_response(status_message="errors.worker-not-found", status_code=status.HTTP_404_NOT_FOUND, status_params={"worker", user_id})
        
        worker_serialized = WorkerSerializer(worker_obj)
        
        return make_response(status_code=status.HTTP_200_OK, status_message="errors.none", data=worker_serialized.data)
    
    def put(self, request, worker_id):
        try:
            worker_obj = Worker.objects.get(id=worker_id)
        except Worker.DoesNotExist:
            return make_response(status_message="errors.worker-not-found", status_code=status.HTTP_404_NOT_FOUND, status_params={"worker", worker_id})
        
        worker_serialized = WorkerSerializer(worker_obj, data=request.data, partial=True)
        if worker_serialized.is_valid(raise_exception=True):
            worker_serialized.save()
        else:
            return make_response(status_message="errors.catastrophe", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, status_params=worker_serialized.errors)
        
        return make_response(status_code=status.HTTP_200_OK, status_message="errors.none", data=worker_serialized.data)


class VersionView(APIView):
    """
    """
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        
        try:
            worker_obj = Worker.objects.get(id=request.data['workers'][0])
        except Worker.DoesNotExist:
            return make_response(status_message="errors.worker-not-found", status_code=status.HTTP_404_NOT_FOUND, status_params={"worker", request.data['workers'][0]})
        
        
        version_obj = Version.objects.filter(workers__in=request.data['workers'], ended_at__isnull=True).first()
        
        if not version_obj:
            versions_obj = Version.objects.filter(ended_at__isnull=True, workers__city=worker_obj.city).first()
            
            if versions_obj:
                version_obj = versions_obj
                version_obj.workers.add(worker_obj)
                version_obj.save()
                version_serialized = VersionSerializer(version_obj)
            else:
                try:
                    version_serialized = VersionSerializer(data=request.data)
                    if version_serialized.is_valid(raise_exception=True):
                        version_serialized.save()
                        pass
                    else:
                        return make_response(status_message="errors.catastrophe", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, status_params=version_serialized.errors)
                except ValidationError as error:
                    params = {}
                    for (value, message) in error.detail.items():
                        params[value] = message[0].code
                    return make_response(status_message="errors.missing-parameters", status_code=status.HTTP_400_BAD_REQUEST, status_params=params)
        else:
            version_serialized = VersionSerializer(version_obj)

        return make_response(status_code=status.HTTP_201_CREATED, status_message="errors.none", data=version_serialized.data)

class QueryView(APIView):
    """
    """
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            query_serialized = QuerySerializer(data=request.data)
            if query_serialized.is_valid(raise_exception=True):
                query_serialized.save()
            else:
                return make_response(status_message="errors.catastrophe", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, status_params=query_serialized.errors)
        except ValidationError as error:
            params = {}
            for (value, message) in error.detail.items():
                params[value] = message[0].code
            return make_response(status_message="errors.missing-parameters", status_code=status.HTTP_400_BAD_REQUEST, status_params=params)

        return make_response(status_code=status.HTTP_201_CREATED, status_message="errors.none", data=query_serialized.data)
    
class ListQueryByVersionView(APIView):
    """
    """
    # permission_classes = [IsAuthenticated]

    def get(self, request, version_id):
        
            version_obj = Version.objects.get(id=version_id)
            
            if version_obj:
                query_objs = Query.objects.filter(version_id=version_obj)
                
                try:
                    query_serialized = QuerySerializer(query_objs, many=True)
                except:
                    pass
        
                status_code = status.HTTP_200_OK
                response = make_response(status_code=status_code, status_message="errors.none", data=query_serialized.data)
                
            else:
                status_code = status.HTTP_404_NOT_FOUND
                response = make_response(status_code=status_code, status_message="erros.does-not-exist")
            return response

class AliveView(APIView):
    """
    """
    # permission_classes = [IsAuthenticated]
    
    def put(self, request, pk):
        """
        Update superUser permission.
        For security, the user himself cannot change his credentials from/to superuser.
        """
        sid = transaction.savepoint()

        try:
            worker_obj = Worker.objects.get(pk=pk)
        except Worker.DoesNotExist:
            return make_response(status_code=status.HTTP_404_NOT_FOUND, status_message="errors.object-not-found", status_params={"worker": pk})
        
        try:
            worker_serialized = WorkerSerializer(worker_obj, data=request.data, partial=True)
            if worker_serialized.is_valid(raise_exception=True):
                worker_serialized.save()
            else:
                transaction.savepoint_rollback(sid)
                return make_response(status_message="errors.catastrophe", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, status_params=worker_serialized.errors)
        except ValidationError as error:
            transaction.savepoint_rollback(sid)
            params = {}
            for (value, message) in error.detail.items():
                params[value] = message[0].code
            return make_response(status_message="errors.missing-parameters", status_code=status.HTTP_400_BAD_REQUEST, status_params=params)

        return make_response(status_code=status.HTTP_200_OK, status_message="errors.none", data=worker_serialized.data)
    
class QueryFile(APIView):
    
    """_summary_

    Args:
        APIView (_type_): _description_
    """
    parser_classes = (MultiPartParser,)
        
    def post(self, request, format=None):
        
        serializer = QueryFileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            handle_obj = HandleVersion.objects.get(id=serializer.data['handle_id'])
            handle_obj.handled = True
            handle_obj.save()
            return make_response(status_code=status.HTTP_200_OK, status_message="errors.none", data=serializer.data)
        else:
            return make_response(status_message="errors.catastrophe", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, status_params=serializer.errors)
        
        
class HandleVersionExecution(APIView):
    """
    """
    # permission_classes = [IsAuthenticated]

    def post(self, request, version_id, worker_id):
        """
        Receives a version id and returnn a list of domains if version has not ended yet.
        """

        try:
            worker_obj = Worker.objects.get(pk=worker_id)
        except Worker.DoesNotExist:
            return make_response(status_code=status.HTTP_404_NOT_FOUND, status_message="errors.object-not-found", status_params={"worker": worker_id})
        
        try:
            version_obj = Version.objects.get(pk=version_id, workers__in=[worker_id])
        except Version.DoesNotExist:
            return make_response(status_code=status.HTTP_404_NOT_FOUND, status_message="errors.object-not-found", status_params={"version": version_id})
        
        
        
        if version_obj.ended_at is None:
            handle_obj = HandleVersion.objects.filter(version_id=version_obj, worker_id=worker_id, handled=False).first()
            handle_serializer = HandleVersionSerializer(handle_obj)
            if handle_obj:
                return make_response(status_code=status.HTTP_200_OK, status_message="errors.none", data=handle_serializer.data)
            else:
                last_handle_obj = HandleVersion.objects.filter(version_id=version_id).last()
                if last_handle_obj:
                    last_rank_end = last_handle_obj.rank_end
                    if last_rank_end < 1000000:
                        new_handle_obj = HandleVersion.objects.create(version_id=version_obj, worker_id=worker_obj, handled=False, rank_start=last_rank_end+1, rank_end=last_rank_end+100)
                        handle_serializer = HandleVersionSerializer(new_handle_obj)
                        return make_response(status_code=status.HTTP_200_OK, status_message="errors.none", data=handle_serializer.data)
                    else:
                        version_obj.ended_at = datetime.now()
                        version_obj.save()
                        return make_response(status_code=status.HTTP_200_OK, status_message="errors.none", data=[])
                else:
                    new_handle_obj = HandleVersion.objects.create(version_id=version_obj, worker_id=worker_obj, handled=False, rank_start=0, rank_end=100)
                    handle_serializer = HandleVersionSerializer(new_handle_obj)
                    return make_response(status_code=status.HTTP_200_OK, status_message="errors.none", data=handle_serializer.data)
                
        else:
            return make_response(status_code=status.HTTP_200_OK, status_message="errors.none", data={"handled": True})
        
    def update(self, request, handle_id):
        """
        Receives a version id and returnn a list of domains if version has not ended yet.
        """

        try:
            handle_obj = HandleVersion.objects.get(pk=handle_id)
        except HandleVersion.DoesNotExist:
            return make_response(status_code=status.HTTP_404_NOT_FOUND, status_message="errors.object-not-found", status_params={"handle_version": handle_id})
        
        if handle_obj:
            handle_obj.handled = True
            handle_obj.save()
        
        return make_response(status_code=status.HTTP_200_OK, status_message="errors.none", data={"handled": True})
    
