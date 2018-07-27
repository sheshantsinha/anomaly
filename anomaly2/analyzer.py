import pandas as pd 
import matplotlib.pyplot as plt
import pickle as pi 
import numpy as np
with open('coeff.pickle','rb') as f:
	data=pi.load(f)
with open('pi','rb') as f:
	data2=pi.load(f)
b0,b1,name,opr_dict=[],[],[],{}
for j in data2:
	opr_dict[j]=0
	tt=len(data2[j]['good'])+len(data2[j]['Best'])
	opr_dict[j]=tt
print(opr_dict)
print("**********")
for i in data:
	b1.append([i,data[i]['B1']])
	b0.append([i,data[i]['B0']])
b1=sorted(b1,key=lambda x:x[1])
barx,bary,barz=[],[],[]
cnames =['aliceblue','antiquewhite','aqua','aquamarine','azure','beige','bisque','black','blanchedalmond','blue','blueviolet','brown','burlywood','cadetblue','chartreuse','chocolate','coral']
for j in b1:
	print(j[0],j[1],opr_dict[j[0]],j[1]/opr_dict[j[0]])
	barx.append(j[0])
	barz.append(j[1])
	bary.append(opr_dict[j[0]])
k=plt.bar(barz,height=bary)
# for l in range(len(k)):
# 	print(k[0])
# 	k[l].set_color(cnames[l])
barz=np.array(barz)
plt.xticks(barz, barx);
plt.show()
