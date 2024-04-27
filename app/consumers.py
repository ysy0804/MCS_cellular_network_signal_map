from channels.generic.websocket import AsyncWebsocketConsumer
from channels.generic.websocket import WebsocketConsumer
from channels.layers import get_channel_layer
from .models import LocationData
import asyncio
import json
import time



channel_layer = get_channel_layer()


class MyConsumer(WebsocketConsumer):
    def connect(self):
       self.accept()
       self.channel_layer.group_add('your_group_name', self.channel_name)
       print('WebSocket连接已建立')

    def disconnect(self, close_code):
        self.channel_layer.group_discard('your_group_name', self.channel_name)
        print('WebSocket连接已关闭')




    def receive(self, text_data):
        # 接收到来自WebSocket的数据

        total_rsrp = 0
        total_rsrq = 0
        total_rssnr = 0
        Cell_latitude_rsrp = 0
        Cell_longitude_rsrp = 0
        Cell_latitude_rsrq = 0
        Cell_longitude_rsrq = 0
        Cell_latitude_rssnr = 0
        Cell_longitude_rssnr = 0
        print("接收到consumer2" + text_data)
        if text_data == 'start_query':
            locations = LocationData.objects.all()
            data = [
                {
                    'latitude': loc.latitude,
                    'longitude': loc.longitude,
                    'signalStrength': loc.signal_strength,
                    'CellID': loc.obj,
                    'operator': loc.Operator,
                    'Users': loc.Users
                }
                for loc in locations
            ]
            locations.update(is_ask=True)
            self.send(text_data=json.dumps({'locations': data}))


            # 获取基站编号列的所有唯一值作为类别
            categories = LocationData.objects.values('obj').distinct()

            # 遍历每个基站编号类别，并获取相应的数据
            for category in categories:
                category_value = category['obj']
                data_list = LocationData.objects.filter(obj=category_value).values()

                for item in data_list:
                    rsrp_value = item['signal_strength']
                    rsrq_value = item['rsrq']
                    rssnr_value = item['rssnr']+21

                    total_rsrp = total_rsrp + rsrp_value
                    total_rsrq = total_rsrq + rsrq_value
                    total_rssnr = total_rssnr + rssnr_value

                for item in data_list:
                    latitude_value = item['latitude']
                    longitude_value = item['longitude']
                    rsrp_value = item['signal_strength']

                    Cell_latitude_rsrp = Cell_latitude_rsrp + self.W_Value(rsrp_value, total_rsrp)*latitude_value
                    Cell_longitude_rsrp = Cell_longitude_rsrp + self.W_Value(rsrp_value, total_rsrp)*longitude_value

                for item in data_list:
                    latitude_value = item['latitude']
                    longitude_value = item['longitude']
                    rsrq_value = item['rsrq']


                    Cell_latitude_rsrq = Cell_latitude_rsrq + self.W_Value(rsrq_value, total_rsrq)*latitude_value
                    Cell_longitude_rsrq = Cell_longitude_rsrq + self.W_Value(rsrq_value, total_rsrq)*longitude_value


                for item in data_list:
                    latitude_value = item['latitude']
                    longitude_value = item['longitude']
                    rssnr_value = item['rssnr']+21

                    Cell_latitude_rssnr = Cell_latitude_rssnr + self.W_Value(rssnr_value, total_rssnr)*latitude_value
                    Cell_longitude_rssnr = Cell_longitude_rssnr + self.W_Value(rssnr_value, total_rssnr)*longitude_value


                Cell_Lat = (Cell_latitude_rsrp + Cell_latitude_rsrq + Cell_latitude_rssnr)/3
                Cell_Lon = (Cell_longitude_rsrp + Cell_longitude_rsrq + Cell_longitude_rssnr)/3


                Cell_data = {
                    'latitude': Cell_Lat,
                    'longitude':  Cell_Lon,
                    'signalStrength': 0,
                    'CellID': data_list[0]['obj'],
                    'operator': data_list[0]['Operator'],
                    'Users': ''
                }

                data.append(Cell_data)

                total_rsrp = 0
                total_rsrq = 0
                total_rssnr = 0
                Cell_latitude_rsrp =0
                Cell_longitude_rsrp = 0
                Cell_latitude_rsrq = 0
                Cell_longitude_rsrq = 0
                Cell_latitude_rssnr = 0
                Cell_longitude_rssnr = 0



            self.send(text_data=json.dumps({'locations': data}))




    def W_Value(self, value, total):
        return value / total


