import pandas as pd
import os
path= os.getcwd()
print(path)
def load_persona():
    df = pd.read_csv(path+"\source_file\persona.csv")
    return df
#Descriptive statistics are retrieved for the dataset
def check_df(df,head=5):
    print("##################### Shape #####################12321")
    print(df.shape)

    print("##################### Types #####################")
    print(df.dtypes)

    print("##################### Head #####################")
    print(df.head(head))

    print("##################### Tail #####################")
    print(df.tail())

    print("##################### Info #####################")
    print(df.info())


    print("##################### NA #####################")
    print(df.isnull().sum())

    print("##################### NA Sum #####################")
    print(df.isnull().sum().sum())

    print("##################### Quantiles #####################")
    print(df.quantile([0, 0.01,0.05, 0.10, 0.25, 0.50, 0.75, 0.95, 0.99, 1]).T)


#For categorical variables, explanatory statistics are taken
def cat_summary(df,col,value_count=False,nunique_count=False,unique_count=False):
    if value_count:
        print(pd.DataFrame({"Frequency": df[col].value_counts(),
                            "Ratio": (df[col].value_counts() / len(df)) * 100}))
    if nunique_count:
        print("Unique count : ", df[col].nunique(), "\n")
    if unique_count:
        print("Count : ", df[col].unique(), "\n")


def group(df,col1,agg_col1,mean=False,min=False,max=False,sum=False):
    if mean:
        print("Mean : ",df.groupby(col1).agg({agg_col1:"mean"}))
    if sum:
        print("Sum : ",df.groupby(col1).agg({agg_col1:"sum"}))
    if min:
        print("Min : ",df.groupby(col1).agg({agg_col1: "min"}))
    if max:
        print("Max :",df.groupby(col1).agg({agg_col1: "max"}))


print("################# TASK 1 #################","\n")
print("################# TASK 1.1 #################","\n")
df = load_persona() #file reading function
check_df(df) #general information

print("################# TASK 1.2 #################","\n")
cat_summary(df,"SOURCE",nunique_count=True)
cat_summary(df,"SOURCE",value_count=True)

print("################# TASK 1.3 #################","\n")
cat_summary(df,"PRICE",nunique_count=True)

print("################# TASK 1.4 #################","\n")
cat_summary(df,"PRICE",value_count=True)

print("################# TASK 1.5 #################","\n")
cat_summary(df,"COUNTRY",value_count=True)

print("################# TASK 1.6 #################","\n")
group(df,"COUNTRY","PRICE",sum=True)

print("################# TASK 1.7 #################","\n")
cat_summary(df,"SOURCE",value_count=True)

print("################# TASK 1.8 #################","\n")
group(df,"COUNTRY","PRICE",mean=True)

print("################# TASK 1.9 #################","\n")
group(df,"SOURCE","PRICE",mean=True)

print("################# TASK 1.10 #################","\n")
group(df,["SOURCE","COUNTRY"],"PRICE",mean=True)


print("################# TASK 2 #################","\n")
print(df.pivot_table(values="PRICE",index=["COUNTRY","SOURCE","SEX","AGE"]),"\n")

print("################# TASK 3#################","\n")
agg_df=df.pivot_table(values="PRICE",index=["COUNTRY","SOURCE","SEX","AGE"]).sort_values(by="PRICE",ascending=False)
print(agg_df,"\n")

print("################# TASK 4 #################","\n")
agg_df=agg_df.reset_index()
#print(agg_df.reset_index(),"\n")

print("################# TASK 5 #################","\n")
agg_df['AGE_CAT'] = pd.cut(agg_df['AGE'],[0,19,24,31,41,agg_df["AGE"].max()], labels=["0_18", "19_23", "24_30", "31_40", "41+"]).astype(object)
agg_df['AGE_CAT'].nunique()


print("################# TASK 6 #################","\n")
agg_df['customers_level_based']  = agg_df[[col for col in agg_df.columns if agg_df[col].dtypes =='O']].apply(lambda x:'_'.join(x), axis=1).str.upper()
agg_df.groupby(['customers_level_based']).agg({'PRICE' : 'mean'})


print("################# TASK 7.1 #################","\n")
agg_df["SEGMENT"]=pd.qcut(agg_df["PRICE"],4,labels=["D","C","B","A"])
agg_df
desc=["min","max","sum","mean"]
agg_df.groupby("SEGMENT").agg({"PRICE":desc})
#group(agg_df,"SEGMENT","PRICE",mean=True,min=True,max=True,sum=True)
agg_df[agg_df["SEGMENT"]=="C"]

#cat_summary(agg_df,["customers_level_based"],value_count=True)
#agg_df[agg_df["customers_level_based"]=="BRA_ANDROID_FEMALE_24_30"]


print("################# TASK 7.2 #################","\n")
country = input("Please, enter the first 3 letters of your country...").upper()
mobile = input("Please, enter mobile phone operating information (android or ios)").upper()
gender = input("Please enter gender information").upper()
age = int(input("Please enter age information"))
age_cat=""
if age <19:
    age_cat+="0_18"
elif age<24:
    age_cat += "19_23"
elif age<31:
    age_cat += "24_30"
elif age<41:
    age_cat += "31_40"
else:
    age_cat += "41+"

new_user= country+"_"+mobile+"_"+gender+"_"+age_cat
new_user

agg_df[agg_df["customers_level_based"] == new_user].loc[:,["customers_level_based","PRICE","SEGMENT"]]




