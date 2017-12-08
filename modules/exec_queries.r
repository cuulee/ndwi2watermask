library(mongolite)
library(sf)
library(tidyr)
library(dplyr)

m <- mongo("sar2watermask","sar2watermask","mongodb://localhost:27017/")

pipeline = '[{
        "$group":
            {
                "_id" : "$properties.id_cogerh",
                "timeSeries" : { "$push" : { "time" : "$properties.ingestion_time" , "area" : "$properties.area"} }
            }        
    }]'

pipeline = '[
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
    ]'


polys=m$aggregate(pipeline,'{"allowDiskUse":true}')

poly = m$find('{"properties.id_cogerh" : 26969}')
