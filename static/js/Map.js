//服务器的


var map = new BMapGL.Map("allmap");
// map.setMapType(BMAP_SATELLITE_MAP);      // 设置地图类型为地球模式


// var Androidsocket = new WebSocket("ws:127.0.0.1:8000/android-websocket/");



// 获取用户当前位置

var geolocation = new BMapGL.Geolocation();
var gc = new BMapGL.Geocoder();//创建地理编码器
  // 开启SDK辅助定位
geolocation.enableSDKLocation();
geolocation.getCurrentPosition(function(result){

                var latitude = result.point.lat; // 获取纬度
                var longitude = result.point.lng; // 获取经度
                map.centerAndZoom(result.point, 19);

});
map.enableScrollWheelZoom(true);
// map.setMapStyleV2({
//   styleId: '6983dcb3181671e1aebd8f830f9574cc'
// });
var cityCtrl = new BMapGL.CityListControl();  // 添加城市列表控件
map.addControl(cityCtrl);
var Locate = new BMapGL.LocationControl();  // 添加城市列表控件
map.addControl(Locate);


// 创建地点搜索对象
var localSearch = new BMapGL.LocalSearch(map, {
  renderOptions: { map: map } // 将搜索结果显示在地图上
});

//引用前端搜索按钮、搜索框输入
var searchButton = document.getElementById("search-button");
var searchInput = document.getElementById("search-input");



//点击按钮检索所有相关地点
searchButton.addEventListener("click",function () {
  var locationName = searchInput.value;
 localSearch.search(locationName);
});


//如果搜索框内没有文字，搜索框具备可伸缩功能
searchButton.addEventListener("click", function() {
    var searchInput = document.getElementById("search-input");
    if(searchInput.value === "") {
        if (searchInput.style.display === "none") {
            // socket.send("hello")

            searchInput.style.display = "inline-block";
        } else {
            searchInput.style.display = "none";
        }
    }
});


/*以下是地理位置自动联想功能*/


// 创建自动完成对象
var autoComplete = new BMapGL.Autocomplete({
  input: searchInput,
  location: map,

});



var myValue;
autoComplete.addEventListener("onconfirm", function(event) {    //鼠标点击下拉列表后的事件
        var _value = event.item.value;
                myValue = _value.province +  _value.city +  _value.district +  _value.street +  _value.business;

                setPlace();
        });

        function setPlace(){
        //      map.clearOverlays();    //清除地图上所有覆盖物
                function myFun(){
                        var Locate = local.getResults().getPoi(0).point;    //获取第一个智能搜索的结果
                        map.centerAndZoom(Locate, 18);
                        map.addOverlay(new BMapGL.Marker(Locate));    //添加标注
                }
                var local = new BMapGL.LocalSearch(map, { //智能搜索
                  onSearchComplete: myFun
                });
                local.search(myValue);
        }


//自定义标记
function createGradientIcon(color,radius) {
  var canvas = document.createElement('canvas');
  var ctx = canvas.getContext('2d');
//  var radius = 10;

  canvas.width = radius * 2;
  canvas.height = radius * 2;

  var gradient = ctx.createRadialGradient(radius, radius, 0, radius, radius, radius);
  gradient.addColorStop(0, 'rgba(255, 255, 255, 1)');
  gradient.addColorStop(1, color);

  ctx.arc(radius, radius, radius, 0, Math.PI * 2, false);
  ctx.fillStyle = gradient;
  ctx.fill();

  return new BMapGL.Icon(canvas.toDataURL(), new BMapGL.Size(radius * 2, radius * 2), {
    imageSize: new BMapGL.Size(radius * 2, radius * 2),
    anchor: new BMapGL.Size(radius, radius)
  });
}



// 创建五角星图标对象
var starIcon = new BMapGL.Icon('static/img/ffgg.png', new BMapGL.Size(20, 20));




// 标记经纬度和网络信号强度
function markLocation(latitude, longitude, signalStrength, CellID,operator,Users) {

    //console.log(latitude);
    // var point = new BMapGL.Point(longitude, latitude);
    // var marker = new BMapGL.Marker(point);
    // map.addOverlay(marker);

    var point = new BMapGL.Point(longitude, latitude);




    if(signalStrength >= -60 && signalStrength < 0){
        var markerOptions = {
        icon: createGradientIcon('#FF0000',6), // 设置标记的图标，可自定义颜色
        offset: new BMapGL.Size(0, 0) // 设置标记的偏移量
  };
    }




    if(signalStrength < -60 && signalStrength >= -80){
        var markerOptions = {
        icon: createGradientIcon('#fca106',6), // 设置标记的图标，可自定义颜色
        offset: new BMapGL.Size(0, 0) // 设置标记的偏移量
  };
    }

    if(signalStrength < -80 && signalStrength >= -100){
        var markerOptions = {
        icon: createGradientIcon('#41ae3c',6), // 设置标记的图标，可自定义颜色
        offset: new BMapGL.Size(0, 0) // 设置标记的偏移量
  };
    }


    if(signalStrength < -100){

        var markerOptions = {
        icon: createGradientIcon('#0f95b0',6), // 设置标记的图标，可自定义颜色
        offset: new BMapGL.Size(0, 0) // 设置标记的偏移量
  };
    }


    if(signalStrength >= 1 && signalStrength<=20){

        // var markerOptions = {
        //  icon: starIcon,
        //  offset: new BMapGL.Size(0, 0) // 设置标记的偏移量
        // };

    }

    if(signalStrength == 0){
        var markerOptions = {
        icon: createGradientIcon('#1c0d1a',10), // 设置标记的图标，可自定义颜色
        offset: new BMapGL.Size(0, 0) // 设置标记的偏移量
        };
    }



      var marker = new BMapGL.Marker(point, markerOptions);
      map.addOverlay(marker);

      if(signalStrength <= 0) {
          marker.addEventListener('mouseover', function () {
               var content = 'SignalStrength: ' + signalStrength + '<br>' +
              'CellID: ' + CellID + '<br>' +
              'Operator: ' + operator + '<br>' +
              'Users: ' + Users;

              var infoWindow = new BMapGL.InfoWindow(content, {height: 120,offset: new BMapGL.Size(20, -10)});
              marker.openInfoWindow(infoWindow);
          });

          marker.addEventListener('mouseout', function () {
              map.closeInfoWindow(); // 关闭InfoWindow
          });
      }

     // marker.addEventListener('mouseover', function() {
     //    var infoWindow = new BMapGL.InfoWindow(signalStrength.toString(), { offset: new BMapGL.Size(20, -10) });
     //    marker.openInfoWindow(infoWindow);
     //  });
     //
     //  marker.addEventListener('mouseout', function() {
     //    map.closeInfoWindow(); // 关闭InfoWindow
     //  });



}


// 发送AJAX请求，获取数据
function fetch_operator_Data(which_operator) {
  // 发送GET请求到后端视图函数的URL
    var url = "/get_operator_Data?which_operator=" + encodeURIComponent(which_operator);
  fetch(url)
    .then(response => response.json())
    .then(data => {
      // 将数据渲染到页面上
      map.clearOverlays();  
      renderData(data);
    })
    .catch(error => {
      console.error("Error:", error);
    });
}



// 渲染数据到页面
function renderData(data) {
     var operatorData = data.operator_data;
        operatorData.forEach(item => {
      var latitude = item.latitude;
      var longitude = item.longitude;
      var signalStrength = item.signalStrength;
      var CellID = item.CellID;
      var operator = item.operator;
      var Users = item.Users;

    markLocation(latitude, longitude, signalStrength, CellID, operator,Users);

    });
}




var myDropdown = document.getElementById("myDropdown");

myDropdown.addEventListener("change", function() {
  var selectedOption = myDropdown.value;
  // 在这里执行选项触发事件的操作
  console.log("选择了：" + selectedOption);
  if(selectedOption === "全部运营商"){
        fetch_operator_Data(0);
  }
  if(selectedOption === "中国移动"){
        fetch_operator_Data(1);
  }
   if(selectedOption === "中国电信"){
        fetch_operator_Data(2);
  }
   if(selectedOption === "中国联通"){
        fetch_operator_Data(3);
  }
});



 var socket = new WebSocket("ws:39.101.76.7:8000/room/hony");

socket.onopen = function(event) {
    console.log('WebSocket连接已建立');
    socket.send('start_query');
    // socket.send(JSON.stringify({
    //     'type': 'join_group',
    //     'group_name': 'your_group_name',
    // }));
};


socket.onmessage = function(event) {
    // const data = JSON.parse(event.data);
     var parsedData = JSON.parse(event.data);

     parsedData.locations.forEach(function(location) {
           markLocation(location.latitude, location.longitude, location.signalStrength, location.CellID, location.operator,location.Users);
                
    });

    //
    //     // 标记为已接收
    // socket.send('received');
};



socket.onclose = function(e) {
  console.log('websocket 断开: ' + e.code + ' ' + e.reason + ' ' + e.wasClean);
  console.log(e);

};






