library(gplots)
library(ggplot2)
library(lubridate)
setwd("~/Documents/MPI/ClimateAndLanguage/LarryKing/analysis/")

colNamesX = c("v",'a','f','h','l','n','s','w','word_tokens','word_types','tokens_in_cmu','types_in_cmu')

files = list.files("../data/king_phon/","*.txt")

d = data.frame()

for(f in files){
  
  year = as.numeric(paste("20",substr(strsplit(f,"_")[[1]][3],1,2), sep=''))
  month = as.numeric(substr(strsplit(f,"_")[[1]][3],3,4))
  day = as.numeric(strsplit(f,"_")[[1]][4])
  
  dx = read.csv(paste("../data/king_phon/",f,sep=''), header = F, stringsAsFactors = F)
  rownames(dx) = dx$V1
  dx$V2 = as.numeric(dx$V2)
  v = dx[colNamesX,]$V2
  v = c(v,year,month,day)
  v[is.na(v)] = 0
  names(v) = c(colNamesX,'year','month','day')
  d = rbind(d,v)
}
names(d) = c(colNamesX,'year','month','day')

d$consonants = rowSums(d[,c('a','f','h','l','n','s','w')])
d$vowelRatio = d$v / d$consonants

d$tokenCoverage = d$tokens_in_cmu/d$word_tokens
d$typeCoverage = d$types_in_cmu/d$word_types

# TODO: some files have no words?
d = d[d$word_types>0 & d$word_tokens>0,]

mean(d$typeCoverage)
mean(d$tokenCoverage)

plotmeans(d$vowelRatio~d$month)

dt = as.Date(paste(d$year,d$month,d$day),format = '%Y %m %d')

d$dayOfYear =as.numeric(strftime(dt, format = "%j"))

d$date = substr(ISOdate(d$year,d$month,d$day),1,10)
# Humidity

# Los angeles = 34.1047979,-118.3903362
h = read.delim("../data/humidity/Humidity_LosAngeles.tsv", sep='\t', skip=1)

h$date = dmy("1/1/1948") + days(h$days.since.1948.01.01.12.00.00)
h$date = as.character(h$date)

# Join dates

d$humidity = h[match(d$date, h$date),]$unitless

# Write out
write.csv(d, file="../data/King_segmentsByDate.csv")


