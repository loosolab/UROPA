## author afust
## reformat all hits table to table with all hits in one row

merged.not.unique <- c()  

## merges and combines all information annotated for one peak
## called for each peak in unique peak list hits in main function
.merge.peak.info <- function(df.current.hit, df.merged, keep.cols, delimiter){
	## peak info stays the same as it is, only feature info will be merged
	
	
	df.tmp <- df.current.hit[,keep.cols]
	## identify columns that should be kept in reformatted table, but have more than one entry
	## than by default only the first entry is kept, but for a warning it is analyzed which columns have multiple entries
	for(col in 1:ncol(df.tmp)){
		unique.entries <- unique(df.tmp[,col])
		unique.entries <- unique.entries[!is.na(unique.entries)]
		if(length(unique.entries)>1){	
			merged.not.unique <<- unique(c(merged.not.unique,colnames(df.tmp[col])))

		}
	}
	df.tmp <- df.tmp[1,]
	df.current.hit <- df.current.hit[,-(keep.cols)]
	

	for(col in 1:ncol(df.current.hit)){
		col.name <- colnames(df.current.hit)[col]
		col.entry <- df.current.hit[,col.name]
		#cat("\ncol.name",col.name,"col.entry",col.entry)
		col.entry.unique <- unique(col.entry)
		
		if(length(col.entry.unique)!=1){
			col.entry <- paste(col.entry, collapse=delimiter)
		} else {
			col.entry <- col.entry.unique
		}
		df.tmp[,col.name] <- col.entry
	}
	if(nrow(df.merged)==0){
		df.merged <- df.tmp
	} else {
		df.merged <- rbind(df.merged,df.tmp)
	}

	return(df.merged)
}




#Script gets arguments
args <- commandArgs(TRUE)
# argument the scipt gets
# $1 = file which should be reformatted
# $2 key column
# $3 columns that should be kept 
# $4 delimiter


if(length(args)==4){
# Process arguments
	#cat("Load input..")
	df.hits <- read.table(args[1], header=TRUE, sep="\t",check.names=FALSE, stringsAsFactors = FALSE, nrow=500)
	cols.df.hits <- colnames(df.hits)
	key <- as.character(args[2])
	keep.cols <- unlist(sapply(unlist(strsplit(args[3],",")), function(t) eval(parse(text=t))))
	
	delimiter <- as.character(args[4])
	## create output
	
	output <- dirname(normalizePath(args[1]))
	filename <- basename(args[1])
	filename <- strsplit(filename,".txt")[[1]]
	filename <- paste0("Reformatted_",filename,".txt")
	output <- paste(output,filename,sep="/")
	
	#cat("done.\nkey:", key, "\nkept columns:", colnames(df.hits)[keep.cols], "\ncombi columns:",colnames(df.hits)[-keep.cols],"\ndelimiter:",delimiter,"\n\nReformat:\n")
	df.merged <- data.frame()
	
	## distinguish between cases where the peak have ids or not
	## if there is no distinct peak id, the peak start position is taken as identifier 
	first.peak.id.entry <- as.character(df.hits[1,key])
	if(first.peak.id.entry !="."){
				## distinct peak id/key column given 
		## identify number of peaks that where annotated in this run
		hits <- unique(as.character(df.hits[,key]))
		## merge information for each peak to one row
		## different queries are seperated by "/"
		## if there are more than one annotations for one query, they are seperated by ","
		## for each peak there will be one row with all annotations, those are stored in df.merged
		n <- length(hits)
		for(i in 1:n){
			## print process
			#if(i %% 10 == 0){
				#cat("\r",i,"/",n)
			#}
			df.current.hit <- subset(df.hits, df.hits[,key]==hits[i])
			df.merged <- .merge.peak.info(df.current.hit,df.merged, keep.cols, delimiter)
		}
	} else {
		#cat("\nThe key column is filled with dots.\nThe peak start position (p_start) will be taken as key coulmn:\n")
		## no distinct peak id only for uropa internal usage
		hits <- unique(df.hits$p_start)
		n <- length(hits)
		for(i in 1:n){
			## print process
			if(i %% 10 == 0){
				cat("\r",i,"/",n)
			}
			df.current.hit <- subset(df.hits, df.hits$p_start==hits[i])
			df.merged <- .merge.peak.info(df.current.hit,df.merged, keep.cols, delimiter)
		}
	}
	df.merged <- df.merged[,cols.df.hits]
	
 	#cat("\nWrite to file..")
 	write.table(df.merged, output, append =FALSE, quote=FALSE,sep='\t', eol='\r\n',row.names = FALSE, col.names = TRUE)
  	#cat("done.\n")

   	if(length(merged.not.unique)>0){
  		cat("WARNING: There are different entries in:", merged.not.unique,"\nThe first entry is kept. Sure you want to keep it?\n")
  	}
 } else {
 	cat("ERROR	wrong usage of script, use like this:\nRscript reformat.R <input> <key> <keep.cols> <delimiter>\n\nFor example: Rscript reformat.R besthits.txt peak_id 1:3,5 ','\nOr: Rscript reformat.R besthits.txt peak_id 1,3,5 '#'\n\nNecessary libraries:'plyr'\n")
 }