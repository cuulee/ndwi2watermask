require(sf)
require(dplyr)
library(lubridate)
library(rgeos)

orson=FALSE

if(orson)
{
    proj="/users/stud09/martinsd/proj/sar2watermask"
    scratch="/mnt/scratch/martinsd"
} else
{
    proj="/home/delgado/proj/sar2watermask"
    scratch="/home/delgado/scratch"
}
    
sardir=paste0(scratch,"/s1a_scenes")
sarIn=paste0(sardir,"/in")
sarOut=paste0(sardir,"/out")
wmIn <- paste0(scratch,"/watermasks")

flist <- list.files(wmIn,pattern=".gml")

### read, remove small parts, remove DN==0 (land), simplify with threshold between 10 and 15 preserving topology. It should reduce size of vector by a factor of at least 3.
for(f in flist)
    {
        p <- st_read(paste0(wmIn,"/",f)) %>%
            as_tibble %>%
            st_as_sf %>%
            filter(DN>0) %>%
            st_transform(crs=32724) %>%
            mutate(ingestion_time=strsplit(f,"_")[[1]][5] %>% ymd_hms()) %>%
            mutate(id_in_scene=row_number(),area=st_area(.)) %>%
            filter(as.numeric(area)>1000) %>%
            select(-fid,-DN)
        
        psimpl <- st_simplify(p,preserveTopology=TRUE,dTolerance=11) %>%
            st_transform(crs=4326) ## back to latlong

        
        st_write(psimpl,paste0(wmIn,"/",f,"_simplified.gml"),driver="GML")
    }
