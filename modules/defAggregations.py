from pymongo import MongoClient
import json
from bson import json_util
import os
import sys 
from datetime import datetime,timedelta

def getLatestPolys(s2w):
    pipeline = [
        { "$sort" : {"properties.id_cogerh" : 1, "properties.ingestion_time" : 1 }},
        {
            "$group":
            {
                "_id" : "$properties.id_cogerh",
                "latestIngestion" : {
                    "$last":"$properties.ingestion_time"
                }
            }
        }
    ]

    aggrLatest=list(s2w.aggregate(pipeline=pipeline))
    
    latest=list()
    
    for feat in aggrLatest:
        poly = s2w.find({'properties.id_cogerh' : feat['_id'],'properties.ingestion_time':feat['latestIngestion']})
        latest.append(poly[0])
    return(latest)

def getLatestIngestionTime(s2w):
    pipeline = [
        { "$sort" : {"properties.id_cogerh" : 1, "properties.ingestion_time" : 1 }},
        {
            "$group":
            {
                "_id" : "$properties.id_cogerh",
                "latestIngestion" : {
                    "$last":"$properties.ingestion_time"
                }
            }
        }
    ]

    aggrLatest=list(s2w.aggregate(pipeline=pipeline))
    latest=list()
    
    for feat in aggrLatest:
        poly = s2w.find({'properties.id_cogerh' : feat['_id'],'properties.ingestion_time':feat['latestIngestion']},{'properties.id_cogerh' : 1,'properties.ingestion_time' : 1})
        latest.append(poly[0])
    return(latest)


def getLatestIngestionTimeMinusOne(s2w):
    thresh_date=datetime.now() - timedelta(days=30)
    pipeline = [
        { "$match" : {"properties.ingestion_time" : {"$lte" : thresh_date}}},
        { "$sort" : {"properties.id_cogerh" : 1, "properties.ingestion_time" : 1 }},
        {
            "$group":
            {
                "_id" : "$properties.id_cogerh",
                "latestIngestion" : {
                    "$last":"$properties.ingestion_time"
                }
            }
        }
    ]
    
    aggrLatest=list(s2w.aggregate(pipeline=pipeline))
    latest=list()
    
    for feat in aggrLatest:
        poly = s2w.find({'properties.id_cogerh' : feat['_id'],'properties.ingestion_time':feat['latestIngestion']})
        latest.append(poly[0])
    return(latest)


def getLatestPolysMinusX(s2w,x):
    thresh_date=datetime.now() - timedelta(days=x*30)
    pipeline = [
        { "$match" : {"properties.ingestion_time" : {"$lte" : thresh_date}}},
        { "$sort" : {"properties.id_cogerh" : 1, "properties.ingestion_time" : 1 }},
        {
            "$group":
            {
                "_id" : "$properties.id_cogerh",
                "latestIngestion" : {
                    "$last":"$properties.ingestion_time"
                }
            }
        }
    ]
    
    aggrLatest=list(s2w.aggregate(pipeline=pipeline))
    
    latest=list()
    
    for feat in aggrLatest:
        poly = s2w.find({'properties.id_cogerh' : feat['_id'],'properties.ingestion_time':feat['latestIngestion']})
        latest.append(poly[0])
    return(latest)



def getTimeSeries(s2w):
    pipeline = [
        {
            "$group":
            {
                "_id" : "$properties.id_cogerh",
                "timeSeries" : { "$push" : { "time" : "$properties.ingestion_time" , "area" : "$properties.area"} }
            }
            
        }
    ]

    TimeSeries = list(s2w.aggregate(pipeline=pipeline))
    return(TimeSeries)


def aggr2geojson(polys):
    feats=[]
    for poly in polys:
        oid=json.loads(json.dumps(poly['_id'],default=json_util.default))
        dttm=poly['properties']['ingestion_time']
        dttmstr=dttm.strftime("%Y-%m-%d %H:%M:%S")
        poly['properties']['ingestion_time']=dttmstr
        del poly['_id']
        poly['properties']['oid']=oid['$oid']

        if len(poly['geometry']['coordinates'])>1:
            mp=geojson.MultiPolygon()

        if len(poly['geometry']['coordinates'])==1:
            mp=geojson.Polygon()

        mp['coordinates']=poly['geometry']['coordinates']

        feats.append(geojson.Feature(geometry=mp,properties=poly['properties']))

    feat_col=geojson.FeatureCollection(feats)
    return(feat_col)
