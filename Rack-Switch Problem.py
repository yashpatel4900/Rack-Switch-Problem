# -- coding: utf-8 --
"""
Created on Thu Apr  2 20:51:03 2020

@author: india
"""

# Copyright (C) 2020  Yash Rajeshbhai Patel and Yash Ashokkumar Patel <yashpatel49000@gmail.com>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


import sys
import time
print('Rack Switch Problem \n')

print('Enter Dimensions of Rack: ')
R_x=int(input('Enter Length of rack: '))
R_y=int(input('Enter Height of rack: '))
R_z=int(input('Enter Width of rack: '))
R_v=R_x*R_y*R_z
print('Length of rack: ',R_x,'Height of rack: ',R_y,'Width of rack: ',R_z,'Volume of rack: ',R_v)

#Takes input of all switches
lt=['A','B','C','D','E']
switches={}
for x in lt:
    
    temp=list(map(int,(input("Enter Quantity, Weightage, Length, Heigth and Depth of each swithch (space seperated):").split())))
    vol=1
    for i in temp[2:]:
        vol=vol*i
    temp.append(vol)
    switches[x]=temp

start=time.time()
sys.stdout=open("Output.txt","w")
print('Rack Switch Problem\n\nRACK')
print('Length: ',R_x,'\nHeight: ',R_y,'\nWidth: ',R_z,'\nVolume: ',R_v)
print('\nThere are 5 Switches A,B,C,D,E')

for key,val in switches.items():
    print(key)
    for i in range(6):
        if i==0:
            print('Quantity: ',val[i])
        if i==1:
            print('Score: ',val[i])
        if i==2:
            print('Length: ',val[i])
        if i==3:
            print('Height: ',val[i])
        if i==4:
            print('Width: ',val[i])
        if i==5:
            print('Volume: ',val[i],'\n')
        

#Calculates sum of volume of all switches
sum_V_S=0
for key,val in switches.items():
    sum_V_S+=val[5]*val[0]
 
#Case 1 if Volume of Rack is Greater than sum of volume of switches no need to arrange
if R_v>sum_V_S:
    print('Volume of Rack is Greater than sum of volume of switches')
    print('Total Execution Time: ',time.time()-start,'Seconds\nProcessor: Intel Core i5-3210M CPU @ 2.50GHz\nRAM: 4GB')
    sys.exit(1)

#Seperate Dictionary for working on Quantity
Quantity={}
for key,val in switches.items():
            Quantity.update({key:val[0]})

guess=[]
height=set()

for val in switches.values():
    height.add(val[3])

#This part finds the minimum height of all switches so that in recursion program can terminate if remaining height of rack is less than height of any switch left
temp_val=R_y+1
temp_key=''

for key,val in switches.items():
    if val[3]<temp_val:
        temp_val=val[3]
        temp_key=key
        
min_height=temp_val
min_height_key=temp_key

#global_max_height is used as global for max_height which is used as local variable in knapsack function
#max_height represents height of any level according to the max height switch used in that level
global_max_height=0
def knapsack(x,y,z,Quantity):
    global switches
    
    #Iterating through the list of switches to find if they can fit or not

    flag=False
    result=[]
    for key,val in switches.items():

        if (val[2]<=x and val[3]<=y and val[4]<=z and Quantity[key]>0):
            flag=True
            copy_of_Quantity=Quantity.copy()
            copy_of_Quantity[key]-=1

            w_horizontal_left=knapsack(x,y,z-val[4],copy_of_Quantity)
            w_horizontal_right=knapsack(x-val[2],y,val[4],w_horizontal_left['quantity'])
            
            #Calculates score that can be obtained by solving problem when we divide remaining space horizontally
            w_horizontal=val[1]+w_horizontal_left['score']+w_horizontal_right['score']
           
            w_vertical_left=knapsack(val[2],y,z-val[4],copy_of_Quantity)
            w_vertical_right=knapsack(x-val[2],y,z,w_vertical_left['quantity'])
            
            #Calculates score that can be obtained by solving problem when we divide remaining space vertically
            w_vertical=val[1]+w_vertical_left['score']+w_vertical_right['score']
            
            #Chooses the best score from horizontal or vertical division
            if w_horizontal<w_vertical:
                ans= {'quantity':w_vertical_right['quantity'],'score':w_vertical}

            else:
                ans= {'quantity':w_horizontal_right['quantity'],'score':w_horizontal}

            result.append(ans)

    if not flag:
        return {'quantity':Quantity,'score':0}
    
    #This part finds the arrangement with maximum score in a level
    list_max=0
    max_index=0

    for i in range(0,len(result)):
        if result[i]['score']>list_max:
            list_max =result[i]['score']
            max_index=i

    return result[max_index]

def knapsack_height(R_x,R_y,R_z,Quantity,result={'score':0,'quantity':{}},levelwise=[]):
    global min_height,min_height_key,switches,height,guess
    
    #If Quantity of switch with minimum height goes 0 then min_height_key must be updated to terminate the code 
    if Quantity[min_height_key]==0:
        temp_val=R_y+1
        temp_key=''
        for key,val in switches.items():
            if val[3]<temp_val and val[3]>=min_height and Quantity[key]>0:
                temp_val=val[3]
                temp_key=key
                    
        if temp_val==R_y+1:
            temp_val=min_height
            temp_key=min_height_key

        min_height=temp_val
        min_height_key=temp_key

    #Base condition for all recursions 
    if R_y<min_height:
        guess.append({'result':result,'level':levelwise})
        return 0

    #Height is a set in which diffent height of switches are stored
    #This loop is used for selection of layers which can give maximum score and can occupy maximum volume of Rack
    for x in height:
        if x<=R_y:
            max_height=x
            
            copy_quantity=Quantity.copy()
            copy_result=result.copy()
            copy_levelwise=levelwise.copy()
            
            #This will return best arrangement of a level
            ans=knapsack(R_x,max_height,R_z,copy_quantity)
            
            #level_quantity is used to store how much switches is used in a particular level in the best case in which minimum volume of Rack is left and maximum score is obtained
            level_quantity={}
            for key,val in Quantity.items():
                level_quantity.update({key:val-ans['quantity'][key]})
            copy_result['quantity']=ans['quantity']
            copy_result['score']+=ans['score']
            copy_levelwise.append(level_quantity)
            
            #This is used to arrange the next level
            knapsack_height(R_x,R_y-max_height,R_z,ans['quantity'],copy_result,copy_levelwise)


knapsack_height(R_x,R_y,R_z,Quantity)

#This will select the best levels from different possibility to complete Rack
list_max=0
max_index=0

for i in range(0,len(guess)):
        if guess[i]['result']['score']>list_max:
            list_max =guess[i]['result']['score']
            max_index=i

#Finds how much quantity is left after filling Rack with Best case
Total_Quantity_diff={}
for key,val in Quantity.items():
    Total_Quantity_diff.update({key:val-guess[max_index]['result']['quantity'][key]})
    
#Finds how much volume is used of Rack and how much is left
Total_used_vol=0
for key,val in Total_Quantity_diff.items():
    for key1,val1 in switches.items():
        if key==key1:
            Total_used_vol+=val*val1[5]
            
#Displays which and how many switches are used in a particular level
counter=0
c_h=0
for i in guess[max_index]['level']:
    m_h=0
    counter+=1
    for key,val in i.items():
        for key1,val1 in switches.items():
            if key1==key and val>0:
                if val1[3]>m_h:
                    m_h=val1[3]
    c_h+=m_h
    print('LEVEL NUMBER: ',counter,'HEIGHT OF THIS LEVEL: ',m_h,'CURRENT HEIGHT: ',c_h,'SWITCHES USED IN THIS LEVEL: ',i)

print('\nTotal Volume of Rack Occupied by selected switches is: ',Total_used_vol,'and Volume which is not used is: ',R_v-Total_used_vol)
print('\nFINAL SCORED OBTAINED: ',guess[max_index]['result']['score'],'QUANTITY OF SWITCHES LEFT: ',guess[max_index]['result']['quantity'])
print('Total Execution Time: ',time.time()-start,'Seconds\nProcessor: Intel Core i5-3210M CPU @ 2.50GHz\nRAM: 4GB')
