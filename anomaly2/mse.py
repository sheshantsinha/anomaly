import pickle 
import numpy as np 
from numpy.linalg import inv
import math 
import requests
import secrets
import string
import random
def mean_error():
	arr=[]
	with open('pred.pickle','rb') as f:
		data=pickle.load(f)
	with open('oprt.pickle','rb') as f2:
		data2=pickle.load(f2)
	with open('requestid.pickle','rb') as f2:
		data3=pickle.load(f2)
	for opr in data2:
		ratio=data[opr]['ratio']
		time=data[opr]['time']
		best=data3[opr]['BestID']
		worst=data3[opr]['WorstID']
		kt=linear_module(ratio,time,opr,best,worst)
		if kt !=False:
			opt=kt[3]
			r_id=kt[2]
			kt.pop()
			kt.pop()
			arr.append(kt)
	arr,str1=sorted(arr,key=lambda x:x[1]),''
	if len(arr)>0:
	#	str1+='Unexpected behaviour:-'
		for j in range(len(arr)):
			if j==0:
				print(arr[j][0])
				if arr[j][0] in data2: 
					str1+='Unexpected behaviour:-'+str(arr[j][0])+'(RMSE:-'+str(round(arr[j][1],2))+')'
			else:
				if arr[j][0] in data2: 
					str1+=','+str(arr[j][0])+'(RMSE: '+str(round(arr[j][1],2))+')'
		print(str1)
		print('Exception:-\n\n')
#		print(opr,r_id)
		if len(str1)>0:
			send_data(str1)
	secure_token()
def linear_module(ratio,time,opr,best,worst):
	ones=np.ones((len(time)))
	X=np.column_stack((ones,time))
	trans=np.transpose(X)
	inv_r=inv(np.matmul(trans,X))
	mult1=np.matmul(inv_r,trans)
	mult2=(np.matmul(mult1,ratio)).tolist()
	b0,b1=mult2[0],mult2[1]
	print(opr,b0,b1)
	ratio,time=np.array(ratio),np.array(time)
	y_pred=[]
	for i in range (len(time)):
		y_pred.append(b0+(b1*time[i]))

	y_pred=np.array(y_pred)

	epsilon=math.sqrt(np.mean(np.square(y_pred-ratio)))

	dist=abs(ratio[-1]-(b1*time[-1])-b0)

	print(opr,epsilon,dist)

	if dist>epsilon:
		print('sdk')
		if ratio[-1]-(b1*time[-1])-b0 >0:
			return [opr,epsilon,best[-1],1]
		elif ratio[-1]-(b1*time[-1])-b0 <0:
			return[opr,epsilon,worst[-1],0]
	else:
		return False
def secure_token():
	n=random.randint(20,40)
	token=''.join(secrets.choice(string.ascii_uppercase+string.digits+string.ascii_lowercase) for _ in range(n))
	with open('secure_token.pickle','rb') as f:
		tok=pickle.load(f)
	if len(tok)<3:
		tok.append(token)
	else:
		tok=tok[1:3]
		tok.append(token)
	with open('secure_token.pickle','wb') as f:
		pickle.dump(tok,f)
	url='https://sokt.io/3zss8oHpKuiYuuuNZMMA/anomaly_det-prediction'
	value={"pred":'Secure Token to get requestID of requests:: '+token}
	r = requests.post(url, data =value)
def send_data(str1):
	url='https://sokt.io/3zss8oHpKuiYuuuNZMMA/anomaly_det-prediction'
	value={"pred":str1}
	r = requests.post(url, data =value)
# if __name__=='__main__':
# 	mean_error()
