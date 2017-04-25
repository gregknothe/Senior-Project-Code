install.packages("data.table",dependencies=T)
require(data.table)
require(twitteR)
require(xlsx)

#####BASE FUNCTIONS######
auth_twitter_api <- function() {
	#Authenticate with the twitter servers  
	consumer_key = "_______________________"
	consumer_secret = "____________________________________________________"
	access_token = "_________________________________________________"
	access_secret = "____________________________________________"

	setup_twitter_oauth(consumer_key, consumer_secret, access_token, access_secret)
}

add_day <- function(start_date) {
	#Adds a single day to the date. 
	split_day = substr(start_date, 9, 10)
	split_month = substr(start_date, 6, 7)
	split_year = substr(start_date, 3, 4)
		
	if(split_day > 31) {
		print("The format is MM-DD-YY, your DD was set above 31, which is impossible.")
		return(NULL)
	}
	if(split_month > 12) {
		print("The format is MM-DD-YY, your MM was set to above 12, which is impossible.")
		return(NULL)
	}
	
	final_month = "no change"
		
	final_day = as.numeric(split_day) + 1
		
	if(split_month=="1" || split_month=="3" || split_month=="5" || split_month=="7" ||
	split_month=="8" || split_month=="10") {
		if(final_day > 31) {
			final_day = "01"
			final_month = as.character(as.numeric(split_month) + 1)
			final_year = split_year
		}
	}
	if(split_month=="2") {
		if(final_day > 28) {
			final_day = "01"
			final_month = "03"
			final_year = split_year
		} 
	}
	if(split_month=="4" || split_month=="6" || split_month=="9" || split_month=="11") {
		if(final_day > 30) {
			final_day = "01"
			final_month = as.character(as.numeric(split_month) + 1)
			final_year = split_year
		}
	}
	if(split_month=="12") {
		if(final_day > 31) {
			final_day = "01"
			final_month = "01"
			final_year = as.character(as.numeric(split_year) + 1)
		}
	}
	if(final_month == "no change") {
		final_date = paste("20",paste(paste(split_year, split_month, sep="-"), final_day, sep="-"), sep="")
	}
	if(final_month != "no change") {
		final_date = paste("20",paste(paste(final_year, final_month, sep="-"), final_day, sep="-"), sep="")
	}
	
	return(final_date)
}

auth_twitter_api()
options(scipen = 999)

pull_reply <- function(topic, num_tweets=500, start_date){
	#Pulls tweets based on the parameters inputed. 
	end_date = add_day(start_date)
	reply = twListToDF(searchTwitter(topic, n=num_tweets, since=start_date, 
	until=end_date, lang="en"))
	reply = reply[!is.na(reply["replyToSID"]),]
	reply$statusSource = NULL
	reply$favorited = NULL
	reply$truncated = NULL
	reply$retweeted = NULL
	reply$longitude = NULL
	reply$latitude = NULL
	reply$replyToSN = NULL
	reply$replyToUID = NULL
	setnames(reply, old=c("text","replyToSID","favoriteCount","created","id","screenName","retweetCount", 
	"isRetweet"), new=c("reply_text","reply_replyToSID","reply_favoriteCount","reply_created","reply_id","reply_screenName",
	"reply_retweetCount", "reply_isRetweet"))
	return(reply)
}

pull_base <- function(id_list){
	#Pulls base tweets based on the list of tweet IDs inputed. 
	base = twListToDF(lookup_statuses(id_list))
	base = base[is.na(base["replyToSID"]),]
	base$statusSource = NULL
	base$favorited = NULL
	base$truncated = NULL
	base$retweeted = NULL
	base$longitude = NULL
	base$latitude = NULL
	base$replyToUID = NULL
	base$replyToSID = NULL
	base$replyToSN = NULL
	setnames(base, old=c("text","favoriteCount","created","id","screenName","retweetCount", 
	"isRetweet"), new=c("base_text","base_favoriteCount","base_created","base_id","base_screenName",
	"base_retweetCount", "base_isRetweet"))
	return(base)
}
 
pull_pairs <- function(topic, num_of_tweets, start_date){ 
	#Utilizes both above functions to pulls tweet pairs (the base tweet, and the reply tweet).
	reply = pull_reply(topic, num_of_tweets, start_date)
	base = pull_base(reply$reply_replyToSID)
	tweets = merge(reply, base, by.x="reply_replyToSID", by.y="base_id")
	return(tweets)
}

pull_tweets <- function(search_terms, num_of_tweets, start_date, file_path, iteration){
	#Pulls tweet pairs based on search terms and date. 
	for(i in search_terms){
		tweets = pull_pairs(i, num_of_tweets, start_date)
		file_name = paste(i,start_date,iteration,sep="_")
		write.xlsx(tweets, paste(paste(file_path,file_name,sep="/"),".xlsx", sep=""))
	}
}

pull_tweets_iterations <- function(search_terms, num_of_tweets, start_date, file_path, num_of_iterations){
	#Pulls tweet pairs over a set amount of time, so the machine can be unsupervised over an extended period of time. 
	for(iter in 1:num_of_iterations){
		start_time = Sys.time()
		pull_tweets(search_terms, num_of_tweets, start_date, file_path, iter)
		end_time = Sys.time()
		print(paste("Iteration #", iter," completed.", sep=""))
		if(iter != num_of_iterations){
			Sys.sleep(30*60 - (end_time - start_time))
		}
	}
}
	
pull_terms = c("he", "she", "it", "they", "we", "us", "our", "I", "my", "you", "your", "his", "her")




