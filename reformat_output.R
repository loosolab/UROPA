#!/usr/bin/env Rscript
## author afust NEU
## reformat BestperQuery_Hits table to table with all information about one peak in one row


## columns given with $3 should be unique and not be seprated by the delimiter
## with the aggregate function the same entries are sepereated by it, so this has to be adjusted
.reformat.keep.cols <- function(entry, delimiter){
	if(grepl(delimiter, entry)){
		entry <- unique(strsplit(entry, delimiter)[[1]])
	}
	return(entry)
}

#Script gets arguments
args <- commandArgs(TRUE)
# argument the scipt gets
# $1 file which should be reformatted
# $2 key column
# $3 columns that should be kept 
# $4 delimiter
# $5 #cores
if(length(args)>=4 && length(args)<=5){
	print(Sys.time())
	# Process arguments
	df.hits <- read.table(args[1], header=TRUE, comment.char="#", sep="\t",check.names=FALSE, stringsAsFactors = FALSE)
	key <- as.character(args[2])
	keep.cols <- unlist(sapply(unlist(strsplit(args[3],",")), function(t) eval(parse(text=t))))
	delimiter <- as.character(args[4])
	cols<- colnames(df.hits)
	## create output
	output <- dirname(normalizePath(args[1]))
	filename <- strsplit(basename(args[1]),"[.]")[[1]][1]
	filename <- paste0(filename,"_compact.txt")
	output <- paste(output,filename,sep="/")
	# if multiple cores are present, use them.
	if(length(args)==5){
		cores <- as.numeric(args[5])
		library(snow)
  		c <- makeSOCKcluster(rep("localhost",cores))
  		## replace occurence of delimiter in data
  		if(delimiter != ";"){
			df.hits[] <- parLapply(c,df.hits, gsub, pattern=delimiter, replacement=";", fixed=TRUE)
		} else {
			df.hits[] <- parLapply(c,df.hits, gsub, pattern=delimiter, replacement=",", fixed=TRUE)
		}

	} else {
		## replace occurence of delimiter in data
		if(delimiter != ";"){
			df.hits[] <- lapply(df.hits, gsub, pattern=delimiter, replacement=";", fixed=TRUE)
		} else {
			df.hits[] <- lapply(df.hits, gsub, pattern=delimiter, replacement=",", fixed=TRUE)
		}
	}
	# combind data by key column
	df.reformat <- aggregate(.~df.hits[,key], data=df.hits, FUN=paste, collapse=delimiter, na.action=na.pass)
	# remove key column and replace by aggregated column
	df.reformat[,key] <- NULL
	cols.new <- colnames(df.reformat)
	cols.new[1] <- key
	colnames(df.reformat) <- cols.new
	#original column order
	df.reformat <- df.reformat[,cols]
	# transform columns that should be kept
	for(i in 1:length(cols[keep.cols])){
		if(length(args)==5){
			col.unique <- parLapply(c, df.reformat[,keep.cols[i]], .reformat.keep.cols, delimiter)
			df.reformat[,keep.cols[i]] <- unlist(col.unique)
			if(i==length(cols[keep.cols])){
				stopCluster(c)
			}
		} else {
			col.unique <- lapply(df.reformat[,keep.cols[i]], .reformat.keep.cols, delimiter)
			df.reformat[,keep.cols[i]] <- unlist(col.unique)
		}
		
	}
	#write to file
 	write.table(df.reformat, output, append =FALSE, quote=FALSE,sep='\t', eol='\n',row.names = FALSE, col.names = TRUE)
 } else {
 	cat("ERROR	wrong usage of script, use like this:\nRscript reformat.R <input> <key> <keep.cols> <delimiter> <<#threads>>\n\nFor example: Rscript reformat.R besthits.txt peak_id 1:3,5 ',' 5\nOr: Rscript reformat.R besthits.txt peak_id 1,3,5 '#'\nLast argument is optional, a number of threads can be added.\n")
 }
