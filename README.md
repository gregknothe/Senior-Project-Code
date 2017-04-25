# Senior-Project-Code
This code was created for my personal senior project. The abstract to the project may give more insight into  the decisions made in the code, so here it is. 

_____________________________________________________________________________________________________________________________________

With the increasing amount of time people spend on social media sites and online in general, the internet has become a thriving hub of person to person interaction. Twitter is one of the largest platforms for these interactions, clocking in at an estimated 1.3 billion registered users, which is estimated to be around 18% of the world's total population.

With such a large user base, Twitter can serve as a great source of public opinion and user communication. In particular, Tweets provide a source of interactions amongst many people, through the use of comment chains on Twitter. With the help of the R package twitteR, these interactions were captured, cleaned, and analyzed. 

In addition to the information held within these interactions, information on each user was collected, such as name and location, through the use of web scraping. These details were then used to attempt to correctly identify the user's gender and time zone with various Python and R packages. 

With all this information in hand, the data were explored in attempt to find established trends amongst a majority of the users. These trends were then used to answer lingering questions, such as are people moodier at night when compared to morning? 

Logistic regression was used to examine associations in the dataset, and a stepwise process was used to reduce the model to the best fit. The only remaining significant variable when predicting reply sentiment was base sentiment. This makes intuitive sense, for it is common knowledge that people often treat to others in the same way they are treated.
