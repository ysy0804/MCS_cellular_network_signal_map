from django.shortcuts import render
from django.http import JsonResponse
import requests
from .models import LocationData
from django.views.decorators.csrf import csrf_exempt
import json
from .models import LocationData
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from urllib.parse import quote
import pymysql
# Create your views here.

def map_view(request):
    return render(request, 'Map.html')


# # 与数据库交互
# @csrf_exempt
# def process_request(request):
#     if request.method == 'POST':
#         # 解析请求数据
#         data = request.POST
#
#         # 连接到 MySQL 数据库
#         connection = pymysql.connect(
#             host='ysy',
#             user='ysy',
#             password='210804Ysy!',
#             database='ysydb'
#         )
#
#         # 执行数据库操作
#         cursor = connection.cursor()
#
#         #sql操作语句
#         cursor.execute("INSERT INTO your_table (column1, column2) VALUES (%s, %s)", (data['value1'], data['value2']))
#         connection.commit()
#
#         # 关闭数据库连接
#         cursor.close()
#         connection.close()
#
#         # 返回响应给 Android 客户端
#         return JsonResponse({'status': 'success'})




#与android交互
@csrf_exempt
def receive_data(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        Current_Latitude = data.get('latitude')
        Current_Longitude = data.get('longitude')
        rsrp_value = data.get('rsrpValue')
        print(request.POST)

        print(Current_Latitude)
        print('\n')
        print(Current_Longitude)
        print('\n')
        print(rsrp_value)
        # 在这里处理接收到的数据
        # ...

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)('your_group_name', {
            'type': 'send_data',
            'latitude': Current_Latitude,
            'longitude': Current_Longitude,
            'signal_strength': rsrp_value,
        })

#        Data = LocationData(latitude=Current_Latitude, longitude=Current_Longitude, signal_strength=rsrp_value)
#       Data.save()


        return JsonResponse({'status': 'success'})
        # return JsonResponse(response_data, status=200)
    else:
        # 处理非 POST 请求的情况
        response_data = {
            'error': 'Invalid request method'
        }
        return JsonResponse(response_data, status=400)



def get_latest_locations(request):
    locations = LocationData.objects.filter(is_ask=False)  # 获取未被处理的位置数据
    data = [
        {
            'latitude': loc.latitude,
            'longitude': loc.longitude,
            'signalStrength': loc.signal_strength
        }
        for loc in locations
    ]

    # 将is_ask字段修改为True
    locations.update(is_ask=True)

    return JsonResponse({'locations': data})











def get_operator_Data(request):
    which_operator = request.GET.get('which_operator')
    if which_operator == "0":
        choiceData = LocationData.objects.all()

    else:
        choiceData = LocationData.objects.filter(Operator=which_operator)

    data = [
        {
            'latitude': loc.latitude,
            'longitude': loc.longitude,
            'signalStrength': loc.signal_strength,
            'CellID': loc.obj,
            'operator': loc.Operator,
            'Users': loc.Users
        }
        for loc in choiceData
    ]

    if which_operator == "0":
        data = CellLocate(data)


    return JsonResponse({'operator_data': data})


def CellLocate(data):
    total_rsrp = 0
    total_rsrq = 0
    total_rssnr = 0
    Cell_latitude_rsrp = 0
    Cell_longitude_rsrp = 0
    Cell_latitude_rsrq = 0
    Cell_longitude_rsrq = 0
    Cell_latitude_rssnr = 0
    Cell_longitude_rssnr = 0
    # 获取基站编号列的所有唯一值作为类别
    categories = LocationData.objects.values('obj').distinct()

    # 遍历每个基站编号类别，并获取相应的数据
    for category in categories:
        category_value = category['obj']
        data_list = LocationData.objects.filter(obj=category_value).values()

        for item in data_list:
            rsrp_value = item['signal_strength']
            rsrq_value = item['rsrq']
            rssnr_value = item['rssnr'] + 21

            total_rsrp = total_rsrp + rsrp_value
            total_rsrq = total_rsrq + rsrq_value
            total_rssnr = total_rssnr + rssnr_value

        for item in data_list:
            latitude_value = item['latitude']
            longitude_value = item['longitude']
            rsrp_value = item['signal_strength']

            Cell_latitude_rsrp = Cell_latitude_rsrp + W_Value(rsrp_value, total_rsrp) * latitude_value
            Cell_longitude_rsrp = Cell_longitude_rsrp + W_Value(rsrp_value, total_rsrp) * longitude_value

        for item in data_list:
            latitude_value = item['latitude']
            longitude_value = item['longitude']
            rsrq_value = item['rsrq']

            Cell_latitude_rsrq = Cell_latitude_rsrq + W_Value(rsrq_value, total_rsrq) * latitude_value
            Cell_longitude_rsrq = Cell_longitude_rsrq + W_Value(rsrq_value, total_rsrq) * longitude_value

        for item in data_list:
            latitude_value = item['latitude']
            longitude_value = item['longitude']
            rssnr_value = item['rssnr'] + 21

            Cell_latitude_rssnr = Cell_latitude_rssnr + W_Value(rssnr_value, total_rssnr) * latitude_value
            Cell_longitude_rssnr = Cell_longitude_rssnr + W_Value(rssnr_value, total_rssnr) * longitude_value

        Cell_Lat = (Cell_latitude_rsrp + Cell_latitude_rsrq + Cell_latitude_rssnr) / 3
        Cell_Lon = (Cell_longitude_rsrp + Cell_longitude_rsrq + Cell_longitude_rssnr) / 3

        Cell_data = {
            'latitude': Cell_Lat,
            'longitude': Cell_Lon,
            'signalStrength': 0,
            'CellID': data_list[0]['obj'],
            'operator': data_list[0]['Operator'],
            'Users': ''
        }

        data.append(Cell_data)

        total_rsrp = 0
        total_rsrq = 0
        total_rssnr = 0
        Cell_latitude_rsrp = 0
        Cell_longitude_rsrp = 0
        Cell_latitude_rsrq = 0
        Cell_longitude_rsrq = 0
        Cell_latitude_rssnr = 0
        Cell_longitude_rssnr = 0

    return data



def W_Value(value, total):
        return value / total

