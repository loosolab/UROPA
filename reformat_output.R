#!/usr/bin/env Rscript

## author afust
## reformat BestperQuery_Hits table to table with all information about one peak in one row
library(getopt)

## columns given with $3 should be unique and not be seprated by the delimiter
## with the aggregate function the same entries are sepereated by it, so this has to be adjusted
.reformat.keep.cols <- function(entry, delimiter){
	if(grepl(delimiter, entry)){
		entry <- unique(strsplit(entry, delimiter)[[1]])
	}
	return(entry)
}
#Script gets arguments
# 0 flag
# 1 mandatory parameter
# 2 optional parameter
options <- matrix(c(
	'input', 'i', 1, 'character', 'file which should be reformatted',
	'key', 'k', 1, 'character', 'key columns seperated by "," without spaces',
	'cols', 'c', 1, 'character', 'columns that should be kept ',
	'delimiter', 'd', 2, 'character', 'delimiter [,]',
	'threads', 't', 2, 'integer', 'cores to be used for reformatting',
	'help', 'h', 0, 'logical','Provides command line help.'
	), byrow=TRUE, ncol=5)
opt <- getopt(options)
#help
if (!is.null(opt$help)) { 
	cat(getopt(options, usage=TRUE))
	q(status=0) }
#check for mandatory input
if (is.null(opt$input) || !file.exists(opt$input)) { 
	cat("\nInput file to reformat is missing or not existend\n")
	q(status=1) 
}
if (is.null(opt$key)) { 
	cat("\nKey column is missing\n")
	q(status=1)
}
if (is.null(opt$cols)) { 
	cat("\nColumns to keep are missing\n")
	q(status=1) 
}
#set defaults
if (is.null(opt$delimiter)) { opt$delimiter <- "," }
if (is.null(opt$threads)) { opt$threads <- 1 }

# Process parameter
df.hits <- read.table(opt$input, header=TRUE, comment.char="#", sep="\t",check.names=FALSE, stringsAsFactors = FALSE)
cols <- colnames(df.hits)
key <- as.character(opt$key)
keep.cols <- unlist(sapply(unlist(strsplit(opt$cols,",")), function(t) eval(parse(text=t))))
delimiter <- as.character(opt$delimiter)

## create output
output <- dirname(normalizePath(opt$input))
filename <- strsplit(basename(opt$input),"[.]")[[1]][1]
filename <- paste0(filename,"_compact.txt")
output <- paste(output,filename,sep="/")
# if multiple cores are present, use them.
if(opt$threads > 1){
	cores <- as.numeric(opt$threads)
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
	if(opt$threads > 1){
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