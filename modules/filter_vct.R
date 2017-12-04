require(sf)
require(dplyr)
library(lubridate)
library(reshape2)
orson=TRUE

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

cogerh <- st_read(paste0(proj,"/auxdata/cogerh/cogerh.gml")) %>%
    as_tibble %>%
    st_as_sf() %>%
    st_set_crs(32724) %>%
    select(-fid)

#st_write(cogerh,paste0(proj,"/auxdata/cogerh/cogerh.gml"))

### read, remove small parts, remove DN==0 (land), simplify with threshold between 10 and 15 preserving topology. It should reduce size of vector by a factor of at least 3.
for(f in flist)
    {
        p <- st_read(paste0(wmIn,"/",f)) %>%
            as_tibble %>%
            st_as_sf %>%
            st_set_crs(4326) %>%
            filter(DN>0) %>%
            st_transform(crs=32724) %>%
            mutate(ingestion_time=strsplit(f,"_")[[1]][5] %>%
                       ymd_hms()) %>%
            mutate(id_in_scene=row_number(),area=st_area(.)) %>%
            filter(as.numeric(area)>1000) %>%
            select(-fid,-DN)
        
        psimpl <- st_simplify(p,preserveTopology=TRUE,dTolerance=11)
        ints <- st_intersects(psimpl,cogerh,sparse=TRUE) %>% unclass(.) %>% melt(.)

        ids=data_frame(id_cogerh=cogerh$id[ints$value],id_in_scene=psimpl$id_in_scene[ints$L1])
        
        #pfilter <- left_join(ids,psimpl) %>% st_as_sf %>% split(.$id_cogerh) %>% lapply(st_union) %>% do.call(c,.) %>% st_cast
        pfilter <- left_join(ids,psimpl) %>%
            st_as_sf %>%
            group_by(id_cogerh) %>%
            summarize(ingestion_time=first(ingestion_time),area=sum(area)) %>%
            st_transform(crs=4326) ## back to latlong
        
        if(!file.exists(paste0(wmIn,"/",f,"_simplified.gml")))
            {
                st_write(pfilter,paste0(wmIn,"/",f,"_simplified.gml"),driver="GML")
            }
        if(file.exists(paste0(wmIn,"/",f))) file.remove(paste0(wmIn,"/",f))
    }
