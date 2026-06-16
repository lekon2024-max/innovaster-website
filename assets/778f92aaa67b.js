//创建和初始化地图函数：
var maps = $(".map-content"),
    mapType = maps.eq(0).data("type");

window.initGoogleMap = function() {
    window.map = [];
    for (var i = 0; i < maps.length; i++) {
        var el = maps.eq(i),
            mapData = {};

        mapData = maps.data();

        map[i] = new google.maps.Map(el[0], {
            center: new google.maps.LatLng(mapData.latitude, mapData.longitude),
            zoom: 15
        });

        var marker = new google.maps.Marker({
            title: mapData.company,
            position: map[i].getCenter(),
            map: map[i]
        });

        var infowindow = new google.maps.InfoWindow();
        infowindow.setContent('<b>' + mapData.company + '</b><br>Add: ' + mapData.address + '');
        marker.addListener('click', function() {
            this.map.setZoom(18);
            this.map.setCenter(marker.getPosition());
            infowindow.open(this.map, marker);
        });
    }
};

window.initBaiduMap = function() {
    window.map = [];
    for (var i = 0; i < maps.length; i++) {
        var el = maps.eq(i),
            mapData = {};

        createMap(i, el.attr("id")); //创建地图
        setMapEvent(i); //设置地图事件
        addMapControl(i); //向地图添加控件
        addMarker(i); //向地图中添加marker
    }
}

//创建地图函数：
function createMap(index, el) {
    var map = new BMap.Map(el); //在百度地图容器中创建一个地图
    mapData = $(map.Va).data();
    var point = new BMap.Point(mapData.longitude, mapData.latitude); //定义一个中心点坐标
    map.centerAndZoom(point, 15); //设定地图的中心点和坐标并将地图显示在地图容器中
    window.map[index] = map; //将map变量存储在全局
}

//地图事件设置函数：
function setMapEvent(index) {
    map[index].enableDragging(); //启用地图拖拽事件，默认启用(可不写)
    map[index].enableScrollWheelZoom(); //启用地图滚轮放大缩小
    map[index].enableDoubleClickZoom(); //启用鼠标双击放大，默认启用(可不写)
    map[index].enableKeyboard(); //启用键盘上下左右键移动地图
}

//地图控件添加函数：
function addMapControl(index) {
    //向地图中添加缩放控件
    var ctrl_nav = new BMap.NavigationControl({
        anchor: BMAP_ANCHOR_TOP_LEFT,
        type: BMAP_NAVIGATION_CONTROL_LARGE
    });
    map[index].addControl(ctrl_nav);

    //向地图中添加比例尺控件
    var ctrl_sca = new BMap.ScaleControl({
        anchor: BMAP_ANCHOR_BOTTOM_LEFT
    });
    map[index].addControl(ctrl_sca);
}

//创建marker
function addMarker(index) {

    //标注点数组
    var markerArr = [{
        title: mapData.company,
        content: mapData.address,
        point: mapData.longitude + "|" + mapData.latitude,
        isOpen: 1,
        isOpen: 1,
        icon: {
            w: 23,
            h: 25,
            l: 46,
            t: 21,
            x: 9,
            lb: 12
        }
    }];

    //创建InfoWindow
    function createInfoWindow(i) {
        var json = markerArr[i];
        var iw = new BMap.InfoWindow("<b class='iw_poi_title' title='" + json.title + "'>" + json.title + "</b><div class='iw_poi_content'>" + json.content + "</div>");
        return iw;
    }

    for (var i = 0; i < markerArr.length; i++) {
        var json = markerArr[i];
        var p0 = json.point.split("|")[0];
        var p1 = json.point.split("|")[1];
        var point = new BMap.Point(p0, p1);
        var iconImg = createIcon(json.icon);
        var marker = new BMap.Marker(point, {
            icon: iconImg
        });
        var iw = createInfoWindow(i);
        var label = new BMap.Label(json.title, {
            "offset": new BMap.Size(json.icon.lb - json.icon.x + 10, -20)
        });
        marker.setLabel(label);
        map[index].addOverlay(marker);
        label.setStyle({
            dispaly: 'none',
            borderColor: "#808080",
            color: "#333",
            cursor: "pointer"
        });

        (function() {
            var index = i;
            var _iw = createInfoWindow(i);
            var _marker = marker;
            _marker.addEventListener("click", function() {
                this.openInfoWindow(_iw);
            });
            _iw.addEventListener("open", function() {
                _marker.getLabel().hide();
            })
            _iw.addEventListener("close", function() {
                _marker.getLabel().show();
            })
            label.addEventListener("click", function() {
                _marker.openInfoWindow(_iw);
            })
            if (!!json.isOpen) {
                label.hide();
                _marker.openInfoWindow(_iw);
            }
        })()
    }
}

//创建一个Icon
function createIcon(json) {
    var icon = new BMap.Icon("http://map.baidu.com/image/us_cursor.gif", new BMap.Size(json.w, json.h), {
        imageOffset: new BMap.Size(-json.l, -json.t),
        infoWindowOffset: new BMap.Size(json.lb + 5, 1),
        offset: new BMap.Size(json.x, json.h)
    })
    return icon;
}

function loadJScript() {
    var script = document.createElement("script");
    script.type = "text/javascript";
    script.async = "async";

    mapType == "baidu" ?
        script.src = "https://api.map.baidu.com/api?v=2.0&ak=pe2p3HxSfMtADyac1Phe4L9kaSKVIfVB&callback=initBaiduMap" :
        script.src = "https://maps.googleapis.com/maps/api/js?key=AIzaSyCA0oxvo5ss47clK49L29HnTkdL_Zup8mA&language=en-US&callback=initGoogleMap";

    document.body.appendChild(script);
}

loadJScript(); //创建和初始化地图