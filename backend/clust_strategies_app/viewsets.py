#from crypt import methods
import imp
from urllib import response
from rest_framework import viewsets
from . import models
from . import serializers


import csv

from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage

#from rest_framework import serializers, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend


fs = FileSystemStorage(location='tmp/')



class DataSetViewset(viewsets.ModelViewSet):
    queryset = models.DataSet.objects.all()
    serializer_class = serializers.DataSetSerializer

    @action(detail = False, methods=['GET'])
    def get_dataset(self, request):
        c_id = request.query_params["c_id"]

        dataset = models.DataSet.objects.filter(company_id = c_id)
        
        
        serializer = serializers.DataSetSerializer(dataset, many = True)

        return Response(serializer.data)
    


class ClientInfoViewset(viewsets.ModelViewSet):
    queryset = models.Client_Info.objects.all()
    serializer_class = serializers.ClientInfoSerialize

    @action(detail = False, methods=['GET'])
    def get_with_fk(self, request):
        #c_id = request.query_params["c_id"]
        d_id = request.query_params["d_id"]
        print(d_id)

        #aux = models.Client_Info.objects.get(company_id = c_id)
        client_info = models.Client_Info.objects.filter(dataset_id = d_id)
        print(client_info)
        serializer = serializers.ClientInfoSerialize(client_info, many = True)

        return Response(serializer.data)
    

    @action(detail=False, methods=['POST'])
    def upload_data(self, request):

        print(request.data)

        #print(request.FILES)
        return Response(":)")
        
        
        file = request.FILES["file"]
        
        c_id = request.data["c_id"]
        d_id = request.data["d_id"]
        #print(c_id,d_id)

        content = file.read()

        file_content= ContentFile(content)
        file_name = fs.save(
            "_tmp.csv",file_content
        )

        tmp_file = fs.path(file_name)

        csv_file = open(tmp_file,errors="ignore")
        reader = csv.reader(csv_file)
        next(reader)

        info_list = []
        print(1)
        for id_, row in enumerate(reader):
            (
                client_name,
                client_gender,
                client_income,
                client_expenses,
            ) = row

            info_list.append(
                models.Client_Info(
                    company_id = models.Company.objects.get(id=c_id),
                    dataset_id = models.DataSet.objects.get(id=d_id),
                    client_name = client_name,
                    client_gender = client_gender,
                    client_income = client_income,
                    client_expenses = client_expenses,
                )
            )
        models.Client_Info.objects.bulk_create(info_list)
        print(1)

        return Response("Data importada correctamente")