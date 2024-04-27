from channels.generic.websocket import WebsocketConsumer
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import LocationData
from app.consumers import MyConsumer
from channels.exceptions import StopConsumer
from channels.layers import get_channel_layer
from django.core import serializers

channel_layer = get_channel_layer()
import json

class AndroidComsumers(WebsocketConsumer):
    def connect(self):
         self.accept()
         print('连接已建立')
         AllData = LocationData.objects.values('latitude', 'longitude', 'signal_strength','Operator')
         json_list = [json.dumps(item) for item in AllData]  # 将每条数据转换为JSON字符串
         result = ''.join(json_list)
         self.send(result)        

    def disconnect(self, close_code):
	     raise StopConsumer()


    def receive(self, text_data):
        # 处理从 Android 客户端接收到的数据
        print("合成和")
        print(text_data)
        global global_var
        global_var = 0
        message = json.loads(text_data)

        # 将数据保存到数据库
       
              
        Current_Latitude = message.get('latitude')
        Current_Longitude = message.get('longitude')
        rsrp_value = message.get('rsrpValue')
        rsrq_value = message.get('rsrqValue')
        rssnr_Value = message.get('rssnrValue')
        operator = message.get('operator')
        Users = message.get('User')
        obj = message.get('obj')
        Time = message.get('Time')
	


        Data = LocationData(latitude=Current_Latitude, longitude=Current_Longitude, signal_strength=rsrp_value, Operator=operator, Users = Users, obj = obj, rsrq=rsrq_value, rssnr=rssnr_Value, Time = Time)

        Data.save()
        global_var += 1
        self.send(str(global_var)) 
       # AllData = LocationData.objects.values('latitude', 'longitude', 'signal_strength')
       # serialized_data = serializers.serialize('json', AllData)
       # self.send(serialized_data)
       # json_list = [json.dumps(item) for item in AllData]  # 将每条数据转换为JSON字符串
       # result = ''.join(json_list)
       # self.send(result)



# class AndroidComsumers(AsyncWebsocketConsumer):
#     async def connect(self):
#         await self.accept()
#         print('连接已建立')
#
#     async def disconnect(self, close_code):
#         pass
#
#     async def receive(self, text_data):
#         # 处理从 Android 客户端接收到的数据
#         print("合成和")
#         # 将数据推送给 Web 客户端
#         print(text_data)
#         # web_consumer = MyConsumer()  # 创建 Web 客户端消费者的实例
#         # web_consumer.scope = self.scope  # 设置 Web 客户端消费者的 scope
#         # web_consumer.connect()  # 建立 WebSocket 连接
#         # web_consumer.receive(text_data)  # 将数据推送给 Web 客户端
#
#         # await self.channel_layer.group_send("webcomsumer", {
#         #     "type": "forward_to_web_frontend",
#         #     "data": text_data
#         # })
#
#         await self.send_to_js(text_data)
#
#     async def send_to_js(self, data):
#         print("哈哈哈哈哈哈哈")
#         await self.send(text_data=data)
