import textblob as tb
import pandas as pd
import re
import collections
import urllib
from bs4 import BeautifulSoup
import sexmachine.detector as gender
import httplib
from urlparse import urlparse

#####Cleaning Functions#####
def delete_links(word):
    #Gets rid of hyperlinks and twitter link symbols.
    if "https:" in word: return ""
    elif "@" in word: return word.replace("@","")
    elif "#" in word: return word.replace("#","")
    elif "re:" in word: return word.replace('re:',"")
    else: return word

def split_words(word):
    #Splits word at uppercase letters, then returns the new words.
	#Ex. FeelsBadMan -> Feels Bad Man
    letters = list(word)
    pos = []
    new_words = []
    for i in range(len(letters)):
        if letters[i].isupper(): pos.append(i)
    if len(pos)==0: return word
    if len(pos)==1 and pos==[0]: return word
    if len(pos)==len(letters): return word

    if pos[0]!=0: pos = [0]+pos
    if pos[len(pos)-1]!=len(word)-1: pos= pos+[len(word)-1]
    for i in range(len(pos)-1):
        new_word = word[pos[i]:pos[i+1]]
        new_words.append(new_word)

    if word[len(word)-1].isupper() == False:
        new_words[len(new_words)-1] = new_words[len(new_words)-1] + word[len(word)-1]
    else:
        new_words.append(word[len(word)-1])
    return " ".join(new_words)

emoticons = {":-)": "happy", ":)":"happy", ":D":"happy", ":o)":"happy",
             ":]":"happy", ":3":"happy", ":c)":"happy", ":>":"happy",
             "=]":"happy", "8)":"happy", ":}":"happy", ":^)":"happy",
             ":-D":"happy", "8-D":"happy", "8D":"happy",
             "x-D":"happy", "xD":"happy", "X-D":"happy", "XD":"happy",
             "=-D":"happy", "=D":"happy", "=-3":"happy", "=3":"happy",
             "B^D":"happy", ":-))":"happy", ">:[":"sad", ":-(":"sad",
             ":(":"sad", ":-c":"sad", ":c":"sad", ":-<":"sad",
             ":<":"sad", ":-[":"sad", ":[":"sad",
             ":{":"sad", ";(":"sad", ":-||":"angry", ":@":"angry",
             ">:(":"angry", ":'-(":"sad", ":'(":"sad", ":'-)":"happy",
             ":')":"happy", "D:<":"disgust", "D:":"astonished", "D8":"astonished",
             "D;":"astonished", "D=":"astonished", "DX":"astonished", "D-':":"sad",
             ">:O":"angry", ":-O":"suprised", ":O":"suprised", ":-o":"suprised",
             ":o":"suprised", "8-O":"suprised", "O_O":"suprised", "o-o":"suprised",
             "O_o":"suprised", "o_O":"suprised", "o_o":"suprised", "O-O":"suprised",
             ">:P":"playful", ":-P":"playful", ":P":"playful", "X-P":"playful",
             "x-p":"playful", "xp":"playful", "XP":"playful", ":-p":"playful",
             "=p":"playful", ":-b":"playful", ":|":"neutral", ":-|":"neutral",
             ":$":"enbarrassed", ":-X":"quiet", ":X":"quiet", ":-#":"quiet",
             ":#":"quiet", ">:)":"pleased", ">:-)":"pleased", "o/\o":"congradulate",
             "%)":"drunk", "\o/":"cheer",
             "<3":"love", "</3":"hate", "(>_<)":"troubled", "(^_^:)":"nervous",
             "(-_-:)":"nervous", "(~_~:)":"nervous", "^_^:":"nervous",
             "(-_-)zzz":"boring", "^-^":"happy", "^_^":"happy",
             "(^_^)/":"happy", "(^O^)/":"happy", "(^o^)/":"happy", "T_T":"sad",
             "T-T":"sad", "(T_T)":"sad", "(T-T)":"sad", ":-:":"sad",
             ":_:":"sad", "(:-:)":"sad", "(:_:)":"sad", "QQ":"sad",
             "Q-Q":"sad", "Q_Q":"sad", "=^_^=":"happy", "(^-^)":"happy"}

def replace_emoticons(word):
    #Inputs a smiley, returns a word that (subjectivly) represents it best.
    emote = word.replace(";",":") 
    if emote in list(emoticons.keys()):
        return emoticons[emote]
    else:
        return word

acro = {"2moro":"tomorrow", "2nite":"tonight", "brb":"be right back",
        "btw":"by the way", "bff":"best friend forever", "cya":"see you later",
        "ily":"i love you", "gr8":"great", "imho":"in my humble opinion",
        "irl":"in real life", "iso":"in search of", "jk":"just kidding",
        "j/k":"just kidding", "w/e":"whatever", "l8r":"later",
        "lmao":"laughing my ass off", "lol":"laugh out loud", "np":"no problem",
        "oic":"oh, i see", "omg":"oh my god", "pov":"point of view",
        "rbtl":"read between the lines", "rotflmao":"rolling on the floor laughing my ass off",
        "thx":"thank you", "tmi":"too much information", "tyvm":"thank you very much",
        "ttyl":"talk to you later", "wtf":"what the fuck", "xoxo":"hugs and kisses",
        "afaik":"as far as i know", "afk":"away from keyboard", "ama":"ask me anything",
        "b/c":"because", "cu":"see you later", "diy":"do it youself",
        "faq":"frequently asked questions", "fyi":"for your information", "ftw":"for the win",
        "hf":"have fun", "idk":"i dont know", "imo":"in my opinion",
        "n/a":"not available", "noob":"loser", "noyb":"none of your business",
        "op":"over powered", "rsvp":"please reply", "tba":"to be announced",
        "tbc":"to be continued", "tgif":"thank god, it is friday", "wfm":"works for me",
        "wth":"what the hell", "brt":"be right there", "cus":"because",
        "idc":"i dont care", "imu":"i miss you", "nsfw":"not safe for work",
        "nvm":"never mind", "qt":"cutie", "rn":"right now",
        "ur":"your", "w8":"wait", "wb":"welcome back",
        "gg":"good game", "dm":"direct message", "pm":"private message",
        "bae":"significant other", "tfti":"thanks for the invite", "gtg":"got to go",
        "lmk":"let me know", "omw":"on my way", "ppl":"people",
        "smh":"shake my head", "tbh":"to be honest", "til":"today i learned",
        "tl;dr":"too long, did not read", "yolo":"you only live once"}

def replace_acro(word):
    #Replaces acronyms with writen out words.
    acr = word.lower()
    if acr in list(acro.keys()):
        return acro[acr]
    else:
        return word

emojis = {"<U+1F601>":"happy", "<U+1F602>":"happy", "<U+1F603>":"happy",
          "<U+1F604>":"happy", "<U+1F605>":"nervous", "<U+1F606>":"happy",
          "<U+1F609>":"flirty", "<U+1F60A>":"happy", "<U+1F60B>":"happy",
          "<U+1F60C>":"tired", "<U+1F60D>":"love", "<U+1F60F>":"interested",
          "<U+1F612>":"annoyed", "<U+1F613>":"sad", "<U+1F614>":"sad",
          "<U+1F616>":"uneasy", "<U+1F618>":"flirty", "<U+1F61A>":"flirty",
          "<U+1F61C>":"energetic", "<U+1F61D>":"energetic", "<U+1F61E>":"disappointed",
          "<U+1F620>":"angry", "<U+1F621>":"angry", "<U+1F622>":"sad",
          "<U+1F623>":"uneasy", "<U+1F624>":"confident", "<U+1F625>":"sad",
          "<U+1F628>":"scared", "<U+1F629>":"weary", "<U+1F62A>":"sleepy",
          "<U+1F62B>":"tired", "<U+1F62D>":"sad", "<U+1F630>":"scared",
          "<U+1F631>":"scared", "<U+1F632>":"astonished", "<U+1F633>":"embarassed",
          "<U+1F635>":"sick", "<U+1F637>":"sick", "<U+1F638>":"happy",
          "<U+1F639>":"happy", "<U+1F63A>":"happy", "<U+1F63B>":"love",
          "<U+1F63C>":"confident", "<U+1F63D>":"love", "<U+1F63E>":"angry",
          "<U+1F63F>":"sad", "<U+1F640>":"scared", "<U+1F645>":"no",
          "<U+1F646>":"yes", "<U+1F647>":"sorry", "<U+1F64C>":"happy",
          "<U+1F64D>":"sad", "<U+1F64E>":"sad", "<U+1F64F>":"happy",
          "<U+274C>":"no", "<U+274E>":"no", "<U+2753>":"confused",
          "<U+2754>":"confused", "<U+2755>":"astonished", "<U+2757>":"astonished",
          "<U+2764>":"love", "<U+1F6AB>":"no", "<U+203C>":"astonished",
          "<U+2049>":"confused", "<U+263A>":"content", "<>":"",
          "<U+1F44D>":"yes", "<U+1F44E>":"no", "<U+1F44F>":"celebrate",
          "<U+1F44C>":"yes", "<U+1F493>":"love", "<U+1F494>":"hate",
          "<U+1F495>":"love", "<U+1F496>":"love", "<U+1F498>":"love",
          "<U+1F4A2>":"angry", "<U+1F4A4>":"sleepy", "<	U+1F4A6>":"worried",
          "<U+1F4A7>":"scared", "<U+1F4AF>":"yes", "<U+1F600>":"happy",
          "<U+1F607>":"divine", "<U+1F608>":"evil", "<U+1F60E>":"cool",
          "<U+1F615>":"confused", "<U+1F617>":"love", "<U+1F619>":"love",
          "<U+1F61B>":"excited", "<U+1F61F>":"sad", "<U+1F626>":"disappointed",
          "<U+1F627>":"sad", "<U+1F62C>":"angry", "<U+1F62E>":"suprised",
          "<U+1F634>":"sleepy", "<U+1F46C>":"love", "<U+1F46D>":"love"}

def replace_emoji(word):
    #Replaces emoji's unicode with actual words.
    if "<U+" in word:
        if word in list(emojis.keys()):
            return emojis[word]
        else:
            return ""
    else:
        return word

def space_punc(tweet):
    #Places a space between punc and surrounding characters. 
    punc = ["!", "?", ".", ",", "(", ")", "[", "]", ";", ":"]
    for i in punc:
        tweet = tweet.replace(i, " "+i+" ")
    return tweet

def checkUrl(url):
	#Checks to see it the URL is valid to avoid errors later on. 
    p = urlparse(url)
    conn = httplib.HTTPConnection(p.netloc)
    conn.request('HEAD', p.path)
    resp = conn.getresponse()
    return resp.status < 400

def user_page_scrape(username):
	#Function to look up name and location of a twitter user.
    page_url = "https://twitter.com/"+username
    if checkUrl(page_url)==False:
        return ("","","")
    source = urllib.urlopen(page_url).read()
    soup = BeautifulSoup(source,"html.parser")
    name = soup.find_all("a", class_="ProfileNameTruncated-link u-textInheritColor js-nav js-action-profile-name")[0]
    name_text = name.text.rstrip().lstrip().strip("\n")
    location = soup.find_all("span", class_="ProfileHeaderCard-locationText u-dir")[0]
    location_text = location.text.rstrip().lstrip().strip("\n")
	assumed_first_name = name_text.split()[0]
    return (name_text, assumed_first_name, location_text)


def gender_guess(name):
#Takes first name and attempts to guess the gender.
    if name == "":
        return("unknown")
    gen = gender.Detector()
    return gen.get_gender(name)

#####MASTER CLEANING FUNCTION######
def clean_tweet(tweet):
    #Attempts to clean the tweets. 
    words = tweet.split()
    for i in range(len(words)):
        #Delete and replace unwanted words
        words[i]=delete_links(words[i])
        words[i]=replace_emoticons(words[i])
        words[i]=replace_emoji(words[i])
    tweet = space_punc(" ".join(words))

    words = tweet.split()
    for i in range(len(words)):
        #Split up clumped words and split acronyms
        words[i]=split_words(words[i])
        words[i]=replace_acro(words[i])
        words[i]=correct(words[i])
    return " ".join(words)

def get_sent(tweet):
	#Assigns sentiment value to cleaned tweets. 
    sent = tb.TextBlob(tweet).sentiment
    if sent[0]>0 and sent[1]<.80:
        status = "positive"
    elif sent[0]<0 and sent[1]<.80:
        status = "negative"
    else:
        status = "neutral"
    return (sent[0], sent[1], status)


#Reading in the raw data
#data = pd.read_csv("E:/TestDataSet.csv", encoding = 'iso-8859-1')
#data = data[0:10]

base_clean_tweet = []
reply_clean_tweet = []
base_sent = []
reply_sent = []
base_status = []
reply_status = []
base_subj = []
reply_subj = []
base_name = []
reply_name = []
base_first_name = []
reply_first_name = []
base_gender = []
reply_gender = []
base_location = []
reply_location = []

#Attempts to clean the tweets, assign sentiment value to the tweets, and gather available information 
#about the twitter user who tweeted the tweet. Then constructs a dataframe out off all of the data. 
for i in range(len(data.base_text)):
    base_clean_tweet.append(clean_tweet(data.base_text[i]))
    reply_clean_tweet.append(clean_tweet(data.reply_text[i]))
    b_sent = get_sent(base_clean_tweet[i])
    r_sent = get_sent(reply_clean_tweet[i])
    base_sent.append(b_sent[0])
    base_subj.append(b_sent[1])
    base_status.append(b_sent[2])
    reply_sent.append(r_sent[0])
    reply_subj.append(r_sent[1])
    reply_status.append(r_sent[2])
    b_user_info = user_page_scrape(data.base_screenName[i])
    r_user_info = user_page_scrape(data.reply_screenName[i])
    base_name.append(b_user_info[0])
    base_first_name.append(b_user_info[1])
    base_gender.append(gender_guess(b_user_info[1]))
    base_location.append(b_user_info[2])
    reply_name.append(b_user_info[0])
    reply_first_name.append(r_user_info[1])
    reply_gender.append(gender_guess(r_user_info[1]))
    reply_location.append(r_user_info[2])
    print("Ran code for "+data.reply_screenName[i] + " and " + data.base_screenName[i])

data["base_clean_tweet"] = base_clean_tweet
data["reply_clean_tweet"] = reply_clean_tweet
data["base_sent"] = base_sent
data["reply_sent"] = reply_sent
data["base_status"] = base_status
data["reply_status"] = reply_status
data["base_subj"] = base_subj
data["reply_subj"] = reply_subj
data["base_name"] = base_name
data["reply_name"] = reply_name
data["base_first_name"] = base_first_name
data["reply_first_name"] = reply_first_name
data["base_gender"] = base_gender
data["reply_gender"] = reply_gender
data["base_location"] = base_location
data["reply_location"] = reply_location

data.to_csv('E:/TestDataSet_Run.csv')
