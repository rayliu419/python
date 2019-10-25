# -*- coding: utf-8 -*-
import math
import sys
import importlib

importlib.reload(sys)

X_PI = 3000 * 0.0174532925194
PI = 3.14159265358979324
RAD = PI / 180.0
EARTH_RADIUS = 6370996.81


def GetDistance(xlng, xlat, ylng, ylat):
    """计算两点之间的距离
    
    Parameters
    ----------
    xlng : float
        x点的纬度
    xlat : float
        x点的经度
    ylng : float
        y点的纬度
    ylat : float
        y点的经度
    
    Returns
    -------
    float : 两点之间的距离，单位为米
    """
    
    radLat1 = xlat * RAD
    radLat2 = ylat * RAD
    a = radLat1 - radLat2
    b = (xlng - ylng) * RAD
    s = 2 * math.asin(math.sqrt(pow(math.sin(a/2), 2) + math.cos(radLat1) * math.cos(radLat2) * pow(math.sin(b/2), 2)))
    dis = s * EARTH_RADIUS
    return dis


def GCJtoBD(gg):
    """火星坐标系转百度坐标系
    
    Parameters
    ----------
    gg : tuple
        (lng, lat)
    
    Returns
    -------
    tuple : (lng, lat)
    """
    gg_lng, gg_lat = gg
    if (gg_lng < 1) or (gg_lat < 1):
        return (0, 0)
    x = gg_lng
    y = gg_lat
    z = math.sqrt(x * x + y * y) + 0.00002 * math.sin(y * X_PI)
    theta = math.atan2(y, x) + 0.000003 * math.cos(x * X_PI)
    bd_lng = z * math.cos(theta) + 0.0065
    bd_lat = z * math.sin(theta) + 0.006
    # return (bd_lng, bd_lat)
    return (round(bd_lng, 6), round(bd_lat, 6))


def BDtoGCJ(bd):
    """百度坐标系转火星坐标系
    
    Parameters
    ----------
    bd : tuple
        (lng, lat)
    
    Returns
    -------
    tuple : (lng, lat)
    """
    bd_lng, bd_lat = bd
    if (bd_lng < 1) or (bd_lat < 1):
        return (0, 0)
    x = bd_lng - 0.0065
    y = bd_lat - 0.006
    z = math.sqrt(x * x + y * y) - 0.00002 * math.sin(y * X_PI)
    theta = math.atan2(y, x) - 0.000003 * math.cos(x * X_PI)
    gg_lng = z * math.cos(theta)
    gg_lat = z * math.sin(theta)
    return (round(gg_lng, 6), round(gg_lat, 6))


if __name__ == '__main__':
    # x = GCJtoBD((116.30638534768, 40.030599745567))
    # x = GCJtoBD((116.300209, 40.023994))
    print(BDtoGCJ((116.32787,39.901721)))
    print(BDtoGCJ((116.327765,39.900508)))
    # print GetDistance(116.3213, 39.9010131, 116.327765, 39.900508)
    # baidu API: 120.17381544168, 30.260044442462
    # print x
