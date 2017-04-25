data = read.csv("C:/Users/Greg Knothe/Desktop/FinalData_1.csv")

###Looking at data
install.packages("plyr")
require(plyr)

count(data$base_gender)
count(data$reply_gender)

count(data$reply_status)
count(data$base_status)

###Normality (Awful) 
qqnorm(data$reply_sent)
qqline(data$reply_sent)

bartlett.test(reply_sent~base_gender, data=data)
bartlett.test(reply_sent~reply_gender, data=data)


###Ploting variables

boxplot(reply_sent~reply_gender, data=data2, xlab="reply gender",
	  ylab="reply sentiment")

###############################
require(car)
model = lm(data$reply_sent ~ data$base_status + data$base_gender + 
		data$reply_gender + data$base_word_count)
qqPlot(model, main="QQ Plot")


###############################
boxplot(reply_sent~base_gender, data=data2, xlab="base gender",
	  ylab="reply sentiment")


###Binary Logistic Regression
data2 = data[data$reply_status!="neutral",]
length(data2$base_text)

data2$reply_gender = factor(data2$reply_gender, c("unknown", "male", "female"))
data2$base_gender = factor(data2$base_gender, c("unknown", "male", "female"))
data2$base_status = factor(data2$base_status, c("neutral", "positive", "negative"))


bin_sent = NULL
for(i in 1:length(data2$base_text)){
	if(data2$reply_status[i]=="positive"){
		bin_sent = c(bin_sent, 1)
	}
	else{
		bin_sent = c(bin_sent, 0)
	}
}

bin_sent

model = glm(bin_sent ~ data2$base_status + data2$base_gender * 
		data2$reply_gender + data2$base_word_count + time_cat, family=binomial(link="logit"))

summary(model)
confint(model)
anova(model, test="Chisq")




###Plot of reply_word_count vs reply_sent (NOTHING MEANINFUL)
plot(data2$reply_word_count, data2$reply_sent)
abline(lm(data2$reply_sent~data2$reply_word_count), col="red")

plot(data2$base_word_count, data2$base_sent)
abline(lm(data2$base_sent~data2$base_word_count), col="red")


all_sent = c(data2$reply_sent, data2$base_sent)
all_wc = c(data2$reply_word_count, data2$base_word_count)
plot(all_wc, all_sent)
abline(lm(all_sent~all_wc), col="red")
#######################################################3

head(data2)

length(data$adj_reply_time)

time_cat = NULL
times = c("0:00", "6:00", "12:00", "18:00")
times = strptime(times, format="%H:%M")
for(i in 1:length(data2$base_text)){
	x = strptime(data2$adj_reply_time[i], format="%H:%M:%S")
	if(x<=times[2]){
		time_cat = c(time_cat, "Early Morning")
	}
	if(x>times[2] & x<=times[3]){
		time_cat = c(time_cat, "Morning")
	}
	if(x>times[3] & x<=times[4]){
		time_cat = c(time_cat, "Afternoon")
	}
	if(x>times[4]){
		time_cat = c(time_cat, "Evening")
	}
}

time_cat = factor(time_cat,c("Early Morning","Morning","Afternoon","Evening"))
count(time_cat)

boxplot(data2$reply_sent~time_cat, xlab="reply creation time",
	  ylab="reply sentiment")


plot(strptime(data2$adj_reply_time, format="%H:%M:%S"), data2$reply_sent)


###Dataset with only known genders for both reply and base###############################

data3 = data2[data2$reply_gender!="unknown",]
data4 = data3[data3$base_gender!="unknown",]

bin_sent1 = NULL
for(i in 1:length(data4$base_text)){
	if(data4$reply_status[i]=="positive"){
		bin_sent1 = c(bin_sent1, 1)
	}
	else{
		bin_sent1 = c(bin_sent1, 0)
	}
}

count(bin_sent1)

time_cat1 = NULL
times = c("0:00", "6:00", "12:00", "18:00")
times = strptime(times, format="%H:%M")
for(i in 1:length(data4$base_text)){
	x = strptime(data4$adj_reply_time[i], format="%H:%M:%S")
	if(x<=times[2]){
		time_cat1 = c(time_cat1, "Early Morning")
	}
	if(x>times[2] & x<=times[3]){
		time_cat1 = c(time_cat1, "Morning")
	}
	if(x>times[3] & x<=times[4]){
		time_cat1 = c(time_cat1, "Afternoon")
	}
	if(x>times[4]){
		time_cat1 = c(time_cat1, "Evening")
	}
}
time_cat1 = factor(time_cat1,c("Early Morning","Morning","Afternoon","Evening"))
count(time_cat1)

model1 = glm(bin_sent1 ~ data4$base_status + data4$base_gender + 
		data4$reply_gender + data4$base_word_count + time_cat1, family=binomial(link="logit"))

summary(model1)
confint(model1)
anova(model1, test="Chisq")


#########################################################
b_status_neut = 0
b_status_pos = 0
b_gender_male = 0
b_gender_uknown = 0 



#########################################################3



model2 = glm(bin_sent ~ data2$base_status + data2$base_gender * 
		data2$reply_gender + data2$base_word_count + time_cat, family=binomial(link="logit"))

summary(model2)
confint(model2)
anova(model2, test="Chisq")


data2$reply_gender = factor(data2$reply_gender, c("male", "female","unknown"))
data2$base_gender = factor(data2$base_gender, c("male", "female", "unknown" ))
data2$base_status = factor(data2$base_status, c("negative", "neutral", "positive"))

model = glm(bin_sent ~ data2$base_status + data2$base_gender + 
		data2$reply_gender + data2$base_word_count + time_cat, family=binomial(link="logit"))

summary(model)
confint(model)
anova(model, test="Chisq")
exp(cbind(OR = coef(model), confint(model)))

model1 = glm(bin_sent ~ data2$base_status + data2$base_word_count + time_cat, family=binomial(link="logit"))

summary(model1)
confint(model1)
anova(model1, test="Chisq")
exp(cbind(OR = coef(model), confint(model)))

######################################################3
data5 = data2[data2$base_status!="neutral",]
length(data5$base_text)

bin_sent5 = NULL
for(i in 1:length(data5$base_text)){
	if(data5$reply_status[i]=="positive"){
		bin_sent5 = c(bin_sent5, 1)
	}
	else{
		bin_sent5 = c(bin_sent5, 0)
	}
}

time_cat2 = NULL
times = c("0:00", "6:00", "12:00", "18:00")
times = strptime(times, format="%H:%M")
for(i in 1:length(data5$base_text)){
	x = strptime(data5$adj_reply_time[i], format="%H:%M:%S")
	if(x<=times[2]){
		time_cat2 = c(time_cat2, "Early Morning")
	}
	if(x>times[2] & x<=times[3]){
		time_cat2 = c(time_cat2, "Morning")
	}
	if(x>times[3] & x<=times[4]){
		time_cat2 = c(time_cat2, "Afternoon")
	}
	if(x>times[4]){
		time_cat2 = c(time_cat2, "Evening")
	}
}

model5 = glm(bin_sent5 ~ data5$base_status + data5$base_gender + 
		data5$reply_gender + data5$base_word_count + time_cat2, family=binomial(link="logit"))

summary(model5)
confint(model5)
anova(model5, test="Chisq")
step(model5)

#######################################################
require(ggplot2)
qplot(data2$base_sent, data2$reply_sent)

data2$reply_status = factor(data2$reply_status)
boxplot(data2$reply_word_count~data2$reply_status, xlab="reply sentiment", ylab="word count of tweet")

