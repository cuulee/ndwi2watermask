library(mongolite)
library(sf)
library(tidyr)
library(dplyr)
library(jsonlite)

oid <- read.table("./latestIngestions.tbl")

m <- mongo("sar2watermask","sar2watermask","mongodb://localhost:27017/")

sflist <- list()

for(i in 1:nrow(oid))
{
    poly = m$find(paste0('{"_id":{"$oid" : "',oid[i,1],'"}}'))
    if(class(poly$geometry$coordinates[[1]])=="list")
    {
        cat(i,"  type: MultiPolygon\n")
        latlong <- list()
        for(j in 1:length(poly$geometry$coordinates[[1]]))
        {
            if(length(dim(poly$geometry$coordinates[[1]][[j]]))==2) latlong[[j]] <- poly$geometry$coordinates[[1]][[j]] %>% list
            if(length(dim(poly$geometry$coordinates[[1]][[j]]))==3) latlong[[j]] <- rbind(poly$geometry$coordinates[[1]][[j]][,,1],poly$geometry$coordinates[[1]][[j]][,,2]) %>% t %>% list
        }
        ii <- lapply(latlong,is.null) %>% unlist
        sfgPl <- st_multipolygon(latlong[!ii])
    } else if(class(poly$geometry$coordinates[[1]])=="array")
    {
        cat(i,"  type: Polygon\n")
        latlong <- rbind(poly$geometry$coordinates[[1]][,,1],poly$geometry$coordinates[[1]][,,2]) %>% t
        sfgPl <- st_polygon(list(latlong))
    }

    sflist[[i]] <- st_geometry(sfgPl) %>% st_sf(.,crs=4326) %>% bind_cols(.,poly$properties)
}


sfPl <- do.call("rbind",sflist)
