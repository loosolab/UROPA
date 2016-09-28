## author afust
## this file will summarize UROPAs annotation

library(VennDiagram)
library(ggplot2)
library(jsonlite)
# script gets arguments
args <- commandArgs(TRUE)
# $1 is the best hits file from UROPA
# $2 config file
# $3 output pdf file
# only if there is more than one query...
# $4 is the merged best hits file from UROPA

# to display the pdf file
options(bitmapType='cairo')
options( warn = -1 )


# basic information independent if there are 3 or 4 input arguments, used otherwhere as .basic.summary
config.query <- data.frame()
queries <- c()
num.queries <- 0
num.features <- 0
num.peaks <- 0
features <- c()

# plot2: counts the occurence of different features present plot to bar plot if ther is more than one feature
.plot.feature.distribution <- function(df.uropa, header){
	if(num.features>1){
		occurence.features <- c()
		for(f in 1:num.features){
			feat <- features[f]
			o <- nrow(subset(df.uropa.best, df.uropa$feature==feat))
			occurence.features <- c(occurence.features,o)
		}
		names(occurence.features) <- features	
		barplot(occurence.features, ylab="occurence",main=header)
	}
}

# plot3: calculate bin width by max distance and plot distance per query per feature
.plot.distance.per.query.per.feature <- function(df.uropa.best){
	# get max distance to calculate binwidth
	dist <-  df.uropa.best[,"distance"]
	median.uropa.best <- median(dist)
	max.uropa.best <- max(dist)
	twentieth.max.uropa.best <- round(max.uropa.best/20)
	if(median.uropa.best + twentieth.max.uropa.best < max.uropa.best){
		considered.distance <- median.uropa.best + twentieth.max.uropa.best
	} else {
		considered.distance <- median.uropa.best
	}
	df.distance.query <- subset(df.uropa.best[,c("feature","distance","query")], (df.uropa.best[,"distance"] < considered.distance))
	max.distance.query <- round(max(as.numeric(df.distance.query[,"distance"])))
	bin.width <- round(max.distance.query/20)
	dpq <- qplot(df.distance.query[,2],data =df.distance.query, facets=query~feature, geom="histogram", binwidth=bin.width, xlab = "Distance to feature", ylab = "Total count", main = "Distance of query vs. feature")
	print(dpq)
}

# counts the occurence of each loci for pie charts (plot 4 and plot 6)
.count.occurence.unique.loci <- function(unique.loci, df.location){
	occurence.loci <- c()
	for(j in 1:length(unique.loci)){
		loci <- as.character(unique.loci[j])
		occurence <- length(grep(loci, df.location$genomic_location))
		occurence <- as.numeric(as.character(occurence))
		occurence.loci <- c(occurence.loci, occurence)
	}
	occurence.loci <- as.numeric(occurence.loci)
	return(occurence.loci)
}

# plot4 : identify genomic lovation per feature and plot it
.plot.genomic.location.per.feature <- function(df.uropa,pie.basic,feature=features){
	op <- par(no.readonly = TRUE)
	# layout of plot
	# if there is more than one feature, there should two columns and the according number of rows
	if(num.features>1){
		feature.rows <- round(num.features/2)
		#layout(matrix(c(1,1:feature.rows), 2, feature.rows+1, byrow = TRUE))
		par(mfrow=c(feature.rows,2))
	}
	#plot(0:10, type = "n", xaxt="n", yaxt="n", bty="n", xlab = "", ylab = "")
	#text(paste0("Genomic location of annotated peaks based on ",pie.basic," hits"))

	for(f in 1:length(feature)){
		feat <- feature[f]
		header <- paste0("Loci of peaks annotated for ",feat)
		df.feature <- subset(df.uropa, df.uropa$feature==feat)
		#if(nrow(df.feature)>0){
		unique.loci <- sort(unique(df.feature$genomic_location))
		occurence.loci <- .count.occurence.unique.loci(unique.loci, df.feature)
		pie(occurence.loci, labels=unique.loci, main=header,cex=.8,radius = 1,clockwise=TRUE)
		#}
		
	}
	title(paste0("Genomic location of annotated peaks based on ",pie.basic," hits"), outer=TRUE,line=-1)
	#par(oma=c(0,0,2,0)) 
	par(op)
}


# reformat every row of the config.query file to string for cover page
.print.query <- function(row){
	r <- paste(unname(as.vector(unlist(row))), collapse="    ")
	return(r)
}

# create cover page and load best hits file, will be done independent of the number  of queries
.basic.summary <- function(best.hits, conf){
	df.uropa.best <- read.table(best.hits, header=TRUE, sep="\t",stringsAsFactors = FALSE)

	# number of peaks annoteted with uropa run
	num.peaks <<- length(unique(df.uropa.best$peak_id))
	# stats is based on annoted peaks -> remove na rows
	df.uropa.best[,"distance"] <- as.numeric(df.uropa.best[,"distance"])
	df.uropa.best <- df.uropa.best[complete.cases(df.uropa.best),]
	anno.peaks <- nrow(df.uropa.best)
	# get infos from config for overview page
	config <- fromJSON(conf)
	config.query <<- as.data.frame(config$queries)
	config.cols <- colnames(config.query)
	priority <- config$priority

	# queries of uropa annotation run
	queries <<- sort.int(as.numeric(unique(df.uropa.best$query)))
	num.queries <<- length(queries)

	queries <<- sprintf("%02d", queries)
	features <<- as.character(unique(df.uropa.best$feature))
	num.features <<- length(features)
	if(grepl("T",priority) && num.queries>1){
		priority <- paste0(priority, "\nNote: pairwise comparison has no matches due to exclusiveness")
	}
	# add query to query data frame	
	config.query$query <<- paste("query",0:(nrow(config.query)-1), sep="_")
	config.query <<- config.query[,c("query", "feature", "distance", "feature.anchor","internals", "strand","direction","filter.attribute", "attribute.value","show.attributes")]
	# replaye "start,center,end" position by "any_pos" 
	config.query$feature.anchor <<- sapply(config.query$feature.anchor, function(x) if(length(x)==3){return("any_pos")}else{return(x)})
	
	# create front page
	overview <- paste("There were", num.peaks, "peaks in the input bed file.\nWith the given configuration (",num.queries,"query/ies ) UROPA annotated", anno.peaks, "peaks.\n", sep=" ")
	plot(0:10, type = "n", xaxt="n", yaxt="n", bty="n", xlab = "", ylab = "")
	text(5, 10, "UROPA summary", cex=2)
	text(1, 8, paste0("There were ", num.peaks, " peaks in the input bed file,\nUROPA annotated ", anno.peaks, " peaks\n"),pos=4)
	query.cols <- paste(colnames(config.query), collapse="  ")
	sum.query <- ""
	sum.query <- paste(sum.query, apply(config.query, 1, .print.query), collapse="\n")
	sum.query <- paste(query.cols, sum.query, sep="\n")
	text(1,5.8, sum.query, cex=.6,pos=4)
	if(num.queries != nrow(config.query)){
		text(1,4, paste("Only queries", paste(queries, collapse=","), "have annotated peaks", sep=" "), cex=.6,pos=4)	
	}

	text(1,3.8,paste0("priority: ", priority), cex=.6,pos=4)
	input <- paste("Input:",unlist(config$bed),collapse=" ")
	anno <- paste("Anno:",unlist(config$gtf),collapse=" ")
	input.anno <- paste(input,anno,sep="\n")
	text(1, 3, input.anno,cex=.6,pos=4)
	# return best hits data frame
	return(df.uropa.best)
}


if(length(args)==3){

	# there is only one query for uropa annotation -> no merged best hits file
	pdf(file=args[3])
	df.uropa.best <- .basic.summary(args[1],args[2])
	# plot 1: pairwise compare of queries will not be plotted because there is only one query 
	#plot.new()
	# plot 2: occurence per feature
	.plot.feature.distribution(df.uropa=df.uropa.best,header="Feature distribution across best hits")
	# plot 3: distance per query per feature
	.plot.distance.per.query.per.feature(df.uropa.best)
	# plot 4: genomic location per feature
	.plot.genomic.location.per.feature(df.uropa.best, "best")
	dev.off()

} else if(length(args)==4){
	# $1 best hits
	# $2 conf
	# $3 output
	# $4 merged best hits

	# there is more than one querey -> merged best hits file exists
	pdf(file=args[3])
	df.uropa.best <- .basic.summary(args[1],args[2])
	# add numbers of annotated peaks per query to cover page and create matrix from it to generate similarity matrix
	# matrix with peaks annotated per query
	
	# number of peaks that have been annotated for diffent queries
	len.queries <- c()
	# y position of the text
	text.y <- 2
	# ad columns to matrix and fill with nas
	.cfill <- function(...){
   	 	nm <- list(...) 
    	nm <- lapply(nm, as.matrix)
    	n <- max(sapply(nm, nrow)) 
    	do.call(cbind, lapply(nm, function (x) 
        rbind(x, matrix(, n-nrow(x), ncol(x))))) 
	}	
	if(num.queries>1){
	m.query.anno <- matrix()
		for(q in 1:num.queries){
			# identify peaks that have been annotated with this query
			peaks.query <- unique(df.uropa.best[as.numeric(df.uropa.best$query)==as.numeric(queries[q]),"peak_id"])
			len.queries <- c(len.queries, length(peaks.query))
			text(1, text.y, paste0("query", queries[q], " annotated ", length(peaks.query), " peaks."),cex=.6,pos=4)
			m.query.anno <- .cfill(m.query.anno,peaks.query)
			text.y <- text.y-0.2
		}
	# add colnames/names to created matrix and vector
		m.query.anno <- m.query.anno[,-1]
		colnames(m.query.anno) <- paste0("query",queries)
		names(len.queries) <- paste("query",queries,sep="")
	# create similarity matrix (calculate overlaps)
		similarity.matrix <- matrix(nrow=num.queries,ncol=num.queries)
		for(col in 1:ncol(m.query.anno)){
			for(compare in 1:ncol(m.query.anno)){	
				if(col == compare){
				# a query should not be compared to itselve
					matches <- 0
				} else {
					initial.query <- as.character(m.query.anno[,col])
					initial.query <- initial.query[!is.na(initial.query)]
					compare.query <- as.character(m.query.anno[,compare])
					compare.query <- compare.query[!is.na(compare.query)]
					matches <- sum(initial.query %in% compare.query)
				}	
				similarity.matrix[col,compare] <- matches
			}
		}
		similarity.matrix[lower.tri(similarity.matrix)] <- 0
	# add row and columnnames as query names to access by those
		colnames(similarity.matrix) <- paste("query",queries,sep="")
		rownames(similarity.matrix) <- paste("query",queries,sep="")
		
	# plot 1: pairwise compare of queries
#	plot.new()
	# pairewise compare
	# layout: always two venn diagrams next to each other -> ncol=2 fixed
	# number of pairwise compares (((n-1)n)/2) correspond to the number of venn diagrams
	# due to the fixed column number of two, there are the have of all compares rows plus one for a title
	# area1 = all peaks
	# area2 = annotated peaks with query a = current.area
	# area3 = annotated peaks with query b = compare.area
	# n12 = area2 -> all peaks annotated with query a from all peaks
	# n13 = area3 -> all peaks annotated with query b from all peaks
	# n23 = peaks annotated with query a and query b
	# n123 = n23 peaks annotated with query 1 and b are part of all peaks = matches
	# get values and plot venn diagram
	# there is always a current query and a compare query
		for(query in 1:(num.queries-1)){
			current.query <- names(len.queries)[1]
			current.area <- len.queries[current.query]
			len.queries <- len.queries[names(len.queries) != current.query]
			for(compare in 1:length(len.queries)){
				compare.query <- names(len.queries)[compare]
				compare.area <- len.queries[compare.query]
				matches <- similarity.matrix[current.query,compare.query]
				plot.new()
				pushViewport(viewport(x=.5, y=0.5, width=.7, height=.7))
				draw.triple.venn(num.peaks, current.area, compare.area, current.area, matches, compare.area, matches, category =c("all",current.query,compare.query), 
					lwd = 2, lty ="solid", col = rep("black", 3), fill = c("gray", "red","blue"), cex=1, cat.pos = c(0,-20,-20), cat.dist = .025, 
					cat.cex =1.5, cat.default.pos= "outer", alpha =  c(0.2,0.5,0.5), euler=TRUE, scaled=TRUE)
				popViewport()
			}
		}

	}
	# plot 2: occurence per feature in best hits
	.plot.feature.distribution(df.uropa=df.uropa.best,header="Feature distribution across best hits")
	# plot 3: distance per query per feature in best hits
	.plot.distance.per.query.per.feature(df.uropa.best)
	# plot 4: genomic location per feature in best hits
	.plot.genomic.location.per.feature(df.uropa.best, "best")


	if(num.queries>1){
	## plots based on merged best hits
 		df.uropa.merged <- read.table(args[4], header=TRUE,  sep="\t",stringsAsFactors = FALSE)
 		df.uropa.merged[,"distance"] <- as.numeric(df.uropa.merged[,"distance"])
		df.uropa.merged <- df.uropa.merged[complete.cases(df.uropa.merged),]
	# plot 5: occurence per feature in merged best hits
		.plot.feature.distribution(df.uropa=df.uropa.merged,header="Feature distribution across merged best hits")
	# plot 6: distance per query per feature	
		y.lim <- round(median(df.uropa.merged[,"distance"]) + (max(df.uropa.merged[,"distance"])/20))
		if(y.lim>max(df.uropa.merged[,"distance"])){
			y.lim <- median(df.uropa.merged[,"distance"])
		}
		density <- subset(df.uropa.merged[,c("distance","feature")], (df.uropa.merged[,"distance"]<y.lim))
		dpq <- qplot(distance,data=density, geom="density", color=feature, xlab = "Distance to feature", ylab = "Relative count")
		print(dpq)
	# plot 7: genomic location per feature based on merged best hits
		merged.features <- unique(df.uropa.merged$feature)
		.plot.genomic.location.per.feature(df.uropa.merged, "merged best", feature=merged.features)
	}
	dev.off()
	
} else {
	cat("ERROR: use script like this:
		Rscript summary.R Besthits.txt summary.config.json summary.pdf
		or
		Rscript summary.R Besthits.txt summary.config.json summary.pdf Mergedbesthits.txt")
}