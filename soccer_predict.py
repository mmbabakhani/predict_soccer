#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import os #sistem amel
from scipy import spatial   #shabih sazi cosine     
import numpy as np
import matplotlib.pyplot as plt
import colorama
from colorama import Fore, Style
import pyautogui



os.system('clear')
teams=input("Please Enter teams name : " )
bz= float(input(Fore.LIGHTWHITE_EX + "Please Enter zarib--> as [mosavi] : " ))
cz= float(input("Please Enter zarib--> as [borde1] : " ))
az= float(input("Please Enter zarib--> as [borde2] :" +Fore.RESET))
zaribhadaf=np.array([bz,cz,az]) 

os.system('clear')




df=pd.DataFrame(pd.read_csv('ftb.csv')).to_numpy() #tabdil mishe be array
# print(type(df))
#print(df)




dfshape=df.shape #shape ye tuple hast ba andaze arrayemoon #shape ro mirize to ye tuple
dfshape=dfshape[0] #tedad satrhaye data===> index sefre shape>>>>meghdare nahayi dfshape,int hast




listt=[]
natije=[]
esm_teams=[]
nc=0
for m in range(dfshape):
    n1=np.delete(df[nc],[0,1,5,6,7], None)
    n2=np.delete(df[nc],[0,1,2,3,4], None) #natije 3 column akhar ke dar bala filter shode bood ro dar yek meghdar jadid mirize
    n3=np.delete(df[nc],[2,3,4,5,6,7], None) #esme tim ha
    listt.append(n1)
    natije.append(n2)
    esm_teams.append(n3)
    nc=nc+1
# print(listt)




zariblist=[]
for i in listt:
    zarib=spatial.distance.cosine(zaribhadaf,i)
#     print("\n",i,zarib)
    zariblist.append(zarib)
#     zariblist.append(i)




# print(type(zariblist))
#dataframe mikonim zarib listo
zariblistdf=pd.DataFrame(zariblist) 
listtdf=pd.DataFrame(listt)
natijedf=pd.DataFrame(natije)
esm_teamsdf=pd.DataFrame(esm_teams)
# zariblistdf
# listtdf



#rename column name
zariblistdf.columns = ['zarib']  #rename column name
natijedf.columns = ['Goals_team_1','Goals_team_2','True1false2mosavi3']  #rename column name
listtdf.columns = ['zarib_mosavi','zarib_team_1','zarib_team_2']  #rename column name
esm_teamsdf.columns = ['team_1','team_2']  #rename column name





#edghame 2 dataframe(zarib va list)
final= pd.concat([zariblistdf,listtdf,natijedf,esm_teamsdf],axis=1)  




#columne jadid va sharte>>zarayebe kamtar az 0.01(ke behine hastand baraye moghayese)
final.loc[final.zarib < 0.001, 'ok_for_compare'] = True 




#baraye automate maghadir True1false2mosavi3
#yadam mimoone geryamo daravordi>>>bekhosoos to bakhshe asigne series to dataframe           
for index,row in final.iterrows() : 
    
    if (row['Goals_team_1']==row['Goals_team_2']) :
        row['True1false2mosavi3']=3
        final.loc[index, 'True1false2mosavi3'] = row['True1false2mosavi3']
  
        
    elif ( row['zarib_team_1']<row['zarib_team_2']  )  :
        if (row['Goals_team_1']< row['Goals_team_2'] ):
            row['True1false2mosavi3']=2
            final.loc[index, 'True1false2mosavi3'] = row['True1false2mosavi3']
       
        elif (row['Goals_team_1']> row['Goals_team_2'] ):
            row['True1false2mosavi3']=1
            final.loc[index, 'True1false2mosavi3'] = row['True1false2mosavi3']  
            
        
        
        
    elif ( row['zarib_team_2']<row['zarib_team_1']  )  :
        if (row['Goals_team_1']< row['Goals_team_2'] ):
            row['True1false2mosavi3']=1
            final.loc[index, 'True1false2mosavi3'] = row['True1false2mosavi3']
       
        elif (row['Goals_team_1']> row['Goals_team_2'] ):
            row['True1false2mosavi3']=2
            final.loc[index, 'True1false2mosavi3'] = row['True1false2mosavi3']       
            
    
    
    elif ( row['zarib_team_1']==row['zarib_team_2']  )  :
        if (row['Goals_team_1']< row['Goals_team_2'] ):
            row['True1false2mosavi3']=0 # 0 is khonsa
            final.loc[index, 'True1false2mosavi3'] = row['True1false2mosavi3']
       
        elif (row['Goals_team_1']> row['Goals_team_2'] ):
            row['True1false2mosavi3']=0 # 0 is khonsa
            final.loc[index, 'True1false2mosavi3'] = row['True1false2mosavi3']





#sort
final=final.sort_values(by=final.columns[0]) 





jam_bord_true=0
jam_bakht_true=0
jam_mosavi_true=0
arrfinal=final.to_numpy()

for jj in arrfinal:
    
    if(jj[9] == True and jj[6]==1  ):
        jam_bord_true+=1
        
    if(jj[9] == True and jj[6]==2  ):
        jam_bakht_true+=1   
    if(jj[9] == True and jj[6]==3  ):
        jam_mosavi_true+=1   




#por kardane maghadir khali NaN in pandas ba 0
final=final.fillna(99999) 








print(Fore.LIGHTRED_EX+"-------------------------------------------")

print(teams)
print(zaribhadaf) 
print("-------------------------------------------"+Fore.RESET)
check_nan= (((final['True1false2mosavi3']==99999) ).sum()) #
print(check_nan)
# print(check_nan)
 
# if(check_nan== 0):
#     sumtrue=((final.ok_for_compare==True).sum())
# else:
#     pass
        
        #final.loc[final.zarib < 0.01, 'ok_for_compare'] = True 

#     sumtrue=((final.ok_for_compare==True).sum()) - check_sumtrue #meghdar nan az sumtrue kam mishe
# else:
#     sumtrue=((final.ok_for_compare==True).sum())
# if check_sumtrue==0 :
#     sumtrue=((final.ok_for_compare==True).sum())
# else:

sumtrue=(final['ok_for_compare']==True).sum()
sumtrue=sumtrue-check_nan
    
    
    
    
print("arrrrrrrrrr",jam_bord_true)
print("arrrrrrrrrr",jam_mosavi_true)
print("arrrrrrrrrr",jam_bakht_true)



# if ((jam_bord_darsad + jam_bakht_darsad+jam_mosavi_darsad)==100):  
jam_bord_darsad=(jam_bord_true*100)/sumtrue
jam_mosavi_darsad=(jam_mosavi_true*100)/sumtrue
jam_bakht_darsad=(jam_bakht_true*100)/sumtrue
failed_darsad=(check_nan*100)/sumtrue


print(Fore.LIGHTYELLOW_EX+"sum of True.Values for compare is",sumtrue)
print("jame bordhaye True va bedard bokhor",(jam_bord_darsad),"%")
print("jame mosavi haye True va bedard bokhor",(jam_mosavi_darsad),"%")
print("jame bakht haye True va bedard bokhor",(jam_bakht_darsad),"%")
print("failed data",failed_darsad,"%")
print("-------------------------------------------","\n")


    
    
if (jam_bord_darsad>=80 and sumtrue>20):
    print("pishnahad:----ehtemale bord kheili ziade ")
elif ((jam_bord_darsad>50 and sumtrue>20 and jam_mosavi_darsad>30)or(jam_mosavi_darsad>50 and sumtrue>20 and jam_bord_darsad>30)):
    print("pishnahad:----bord-mosavi ")
elif (jam_bord_darsad>40 and jam_bakht_darsad>40):
    print("pishnahad:bord-bord/ehtemale mosavi nist")
else:
    print("nazari mojood nist")










print("\n","-------------------------------------------","\n"+Fore.RESET)

print(final.iloc[:,[0,1,2,3,4,5,9]])

print("\n","-------------------------------------------","\n")





    
bordkol=((final.True1false2mosavi3==1).sum())
mosavikol=((final.True1false2mosavi3==3).sum())
bakhtkol=((final.True1false2mosavi3==2).sum())
print(Fore.LIGHTRED_EX+"amare_dar_majmoooe_kole_database(",bordkol+bakhtkol+mosavikol,")","\n")
print(bordkol,"bord---------bar hasbe zaribe kamtar!!!!!!",((bordkol*100)/(bordkol+mosavikol+bakhtkol)),"%")
print(mosavikol,"mosavi------------------------------------",((mosavikol*100)/(bordkol+mosavikol+bakhtkol)),"%")
print(bakhtkol,"bakht---------bar hasbe zaribe kamtar!!!!!!",((bakhtkol*100)/(bordkol+mosavikol+bakhtkol)),"%" +Fore.RESET)




