library(mongolite)
library(sf)
library(tidyr)
library(dplyr)
library(jsonlite)

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

for(i in 1:10])
{ 
    poly = m$find(paste0('{"properties.id_cogerh" : ',polys$`_id`[i],'}'))
    if(poly$geometry$type=="MultiPolygon")
    {
        for(j in 1:poly$geometry$coordinates[[1]])
        {
            latlong[[j]] <- rbind(poly$geometry$coordinates[[1]][[i]][,,1],poly$geometry$coordinates[[1]][[i]][,,2]) %>% t
        }
        sfclist[[i]] <- lapply(latlong,st_multipolygon)
    } else if(poly$geometry$type=="Polygon")
    {
        latlong <- rbind(poly$geometry$coordinates[[1]][,,1],poly$geometry$coordinates[[1]][,,2]) %>% t
    }
}

poly = m$find('{"properties.id_cogerh" : 26946}')

sfgPl <- st_polygon(list(latlong)))
sfcPl <- st_geometry(sfgPl)
sfPl <- st_sf(sfcPl,crs=4326) %>% bind_cols(.,poly$properties)
