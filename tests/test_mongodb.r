library(sf)
#library(mongolite)
library(ggplot2)
library(dplyr)
#library(geojsonio)
library(lubridate)
#library(geosphere)
library(rgeos)

wm_in <- "~/scratch/watermasks/"

flist <- list.files(wm_in,pattern=".gml")

f <- flist[1]

### read, remove small parts, remove DN==0 (land), simplify with threshold between 10 and 15 preserving topology. It should reduce size of vector by a factor of at least 3.

p <- st_read(paste0(wm_in,f)) %>%
    as_tibble %>%
    st_as_sf %>%
    filter(DN>0) %>%
    st_transform(crs=32724) %>%
    mutate(ingestion_time=strsplit(f,"_")[[1]][5] %>% ymd_hms()) %>%
    mutate(id_in_scene=row_number(),area=st_area(.)) %>%
    filter(as.numeric(area)>1000) %>%
    select(-fid,-DN)

psimpl <- st_simplify(p,preserveTopology=TRUE,dTolerance=11)

st_write(psimpl,"/home/delgado/TMP/psimpl3",driver="GeoJSON")

sfcPl <- st_geometry(p)[1]
sfgPl <- st_geometry(p)[[1]]

class(sfPl)
class(sfcPl)
class(sfgPl)


m <- mongo(collection = "test",  db = "test", url = "mongodb://localhost")

m$insert(geojson_json(psimpl))

cat(geojson_json(psimpl))

m$find('{"features.properties.id_in_scene":"4"}')
