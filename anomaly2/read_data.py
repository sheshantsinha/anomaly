from pymongo import MongoClient
import pandas as pd
from datetime import datetime
from sklearn.cluster import KMeans  
import matplotlib.pyplot as plt
import numpy as np
import pickle
from bson import ObjectId
import time
import requests
import json
import datetime as dt_after
from numpy.linalg import inv
import mse
plt.rcParams['figure.figsize'] = (5, 4)
def db_query():
	print('Execution Stared:-1st part')
	print(datetime.now())
	client=MongoClient('mongodb+srv://mongoAppUser:rp_JWzg.ZaE8B@msg91-prod-j98or.mongodb.net/admin')
	db=client['msg91_betatest']
	coll=db['ms_text_report_otp']
	coll2=db['ms_text_request_otp']
	jj=coll.count()
	print(jj)
	# to_date = datetime(2018, 6, 23, 10, 0, 0)
	# from_date = datetime(2018, 6, 9, 19, 48, 00)
	# print(from_date)
	# for ll in range(int(200)):
	# print(from_date)
	#{'sentTime':{"$gte": from_date, "$lt": to_date}}).sort([('_id',1)]
	d=coll.find().sort([('_id',-1)]).limit(3000)
	my_dict,limx,lim_dict={'deliveryTime':[],'sentTime':[],'route':[],'telNum':[],'status':[],'smsc':[],'requestID':[],'retryCount':[]},[],{}
	for r in d:
		#print(r['mobiles'])
		for ele in r:
			try:
				t=r[ele]
				my_dict[ele].append(t)

			except Exception as e:
				k=False
		if 'retryCount' not in r:
			my_dict['retryCount'].append(0)
		limx.append(ObjectId(my_dict['requestID'][-1]))
		lim_dict[ObjectId(my_dict['requestID'][-1])]=len(my_dict['requestID'])-1
		#my_dict['timeInterval'].append(int(my_dict['deliveryTime'][-1])-int(my_dict['sentTime'][-1]))
	# last_time=str(my_dict['sentTime'][-1])+'.0'
	# last_time=last_time.split(".")[0]
	# last_time=last_time.replace("-",",")
	# last_time=last_time.replace(" ",",")
	# last_time=last_time.replace(":",",")
	# last_time=last_time.split(",")
	# from_date = datetime(int(last_time[0]),int(last_time[1]),int(last_time[2]),int(last_time[3]),int(last_time[4]),int(last_time[5]))
	d2=coll2.find({'_id':{'$in':limx}})
	for dd in d2:
		my_dict['sentTime'][lim_dict[dd['_id']]]=dd['requestDateString']
	print('Execution Stared:-2nd part')
	df=pd.DataFrame(my_dict)
	df.to_csv('new_data.csv',index=False)
	time_integer()

def time_integer():
	df=pd.read_csv('new_data.csv')
	ds=df['sentTime']
	dt=df['deliveryTime']
	li=df.columns.tolist()
	timeDiff,sent_mili,req_arr,route,diff_arr=[],[],[],[],[]
	#print(my_dict)
	ref_dict={'requestID':[],'route':[],'timeDiff':[],'sent_in_ms':[],'smsc':[],'retryCount':[]}
	for i in range(df.shape[0]):
		try:
			tt=datetime.strptime(ds[i],'%Y-%m-%d %H:%M:%S')
		except:
			tt=datetime.strptime(ds[i],'%Y-%m-%d %H:%M:%S.%f')
		stms = tt.timestamp()
		dtt=datetime.strptime(dt[i],'%Y-%m-%d %H:%M:%S')
		dtms = dtt.timestamp()
		net_diff=(dtms-stms)

		if df['status'][i]==1:
			# print(millisec)
			ref_dict['timeDiff'].append(net_diff)
			ref_dict['sent_in_ms'].append(stms)
			ref_dict['requestID'].append(df['requestID'][i])
			ref_dict['route'].append(df['route'][i])
			ref_dict['smsc'].append(df['smsc'][i])
			ref_dict['retryCount'].append(df['retryCount'][i])
		#K
		diff_arr.append(net_diff)
	#print(my_dict['sentTime'])
	#print(len())
	df['timeDiff']=diff_arr
	#df['sent_in_ms']=ref_dict['sent_in_ms']
	df.to_csv('new_data.csv',index=False)
	df2=pd.DataFrame(ref_dict)
	#clustering(df2)
	makedict(df2,li)
def makedict(df,li):
	arr1,arr2,route_dict=df['smsc'],[],{}
	for i in range(df.shape[0]):
		try:
			arr2.index(arr1[i])
		except:
			arr2.append(arr1[i])
	for j in arr2:
		route_dict[j]={'requestID':[],'timeDiff':[],'sent_in_ms':[],'retryCount':[]}
	for k in range(df.shape[0]):
		route_dict[df['smsc'][k]]['requestID'].append(df['requestID'][k])
		route_dict[df['smsc'][k]]['timeDiff'].append(df['timeDiff'][k])
		route_dict[df['smsc'][k]]['sent_in_ms'].append(df['sent_in_ms'][k])
		route_dict[df['smsc'][k]]['retryCount'].append(df['retryCount'][k])
	counton,plotx,packet=3,1,{}
	for l in arr2:
		df=pd.DataFrame(route_dict[l])
		if l not in packet:
			packet[l]={'worst':{'Avg_mean_time':0,'Nearest_data_in_per':0},'moderate':{'Avg_mean_time':0,'Nearest_data_in_per':0},'Best':{'Avg_mean_time':0,'Nearest_data_in_per':0},'total':0}
		if(clustering(df,l,counton,plotx,li,packet)==False):
			counton-=1
			clustering(df,l,1,plotx,li,packet)
		plotx+=1
	send_packet(packet)
	#plt.show()
	print('Total Operator',len(arr2))
	print('*******************')

def clustering(df,l0,clust,px,li,packet):
	X=np.array(list(zip(df['sent_in_ms'],df['timeDiff'])))
	retry=df['retryCount']
	requestID=df['requestID']
	clusters=clust
	try:
		kmean=KMeans(n_clusters=clusters)
		train_data=X[0:int((len(X))*0.7)]
		test_data=X[int((len(X))*0.7):len(X)]
		kmean=kmean.fit(train_data)
		labels=kmean.predict(test_data)
		centroid=kmean.cluster_centers_
		cent=centroid.tolist()
		arrx,arry,arrperc,arrz=[],[],[],[]
		for p in range (clusters):
			arrx.append([])
			arry.append([])
			arrz.append([])
			arrperc.append([])
		for i in range (df.shape[0]):
			dist,index=0,-1
			for j in range(clusters):
				d=((df['timeDiff'][i]-cent[j][1])**2)+((df['sent_in_ms'][i]-cent[j][0])**2)
				if dist==0:
					index=j 
					dist=d
				elif d<dist:
					index=j
					dist=d
			arry[index].append(df['timeDiff'][i])
			arrx[index].append(df['sent_in_ms'][i])
			arrz[index].append(df['requestID'][i])
		plt.figure(px)
		leny=0
		try:
			for tu in range(len(arry)):
				leny+=len(arry[tu])
		except Exception as e:
			print(e)
		for i in range(len(arrx)):
			lenx=len(arry[i])*100/leny
			arrperc[i].append(lenx)
			arrperc[i].append(cent[i][1])
			arrperc[i].append(cent[i][0])
			arrperc[i].append(arrz[i])
			#print('Precentage around centroid '+str(cent[i][1])+'='+str(lenx)+'%')
			plt.scatter(arrx[i],arry[i])
			plt.scatter(cent[i][0],cent[i][1],color='red',label=str(cent[i][1])+'='+str(lenx)+'%')
		packet[l0]['total']=leny
		sorted_cent=sorted(arrperc,key=lambda l:l[1], reverse=True)
		print(l0)
		lab=['Worst :','Moderate :','Best :']
		#
			#print(lab[m]+' '+str(sorted_cent[m][2])+' '+str(sorted_cent[m][1])+' '+str(sorted_cent[m][0]))
			#try:
			# except:
			# 	try:
			# 		packet[l0]['moderate']['Avg_mean_time']=sorted_cent[1][1]
			# 		packet[l0]['moderate']['Nearest_data_per']=sorted_cent[1][0]
			# 		packet[l0]['best']['Avg_mean_time']=sorted_cent[2][1]
			# 		packet[l0]['best']['Nearest_data_per']=sorted_cent[2][0]
			# 	except:
			# 		packet[l0]['best']['Avg_mean_time']=sorted_cent[2][1]
			# 		packet[l0]['best']['Nearest_data_per']=sorted_cent[2][0]

		with open('pi','rb') as f:
			file=pickle.load(f)
		if l0 not in file:
			file[l0]={'worst':[],'good':[],'Best':[]}
		try:
			file[l0]['worst'].append(sorted_cent[0])
			file[l0]['good'].append(sorted_cent[1])
			file[l0]['Best'].append(sorted_cent[2])
			packet[l0]['worst']['Avg_mean_time']=sorted_cent[0][1]
			packet[l0]['worst']['Nearest_data_in_per']=sorted_cent[0][0]
			packet[l0]['worst']['requestID']=sorted_cent[0][3]
			packet[l0]['moderate']['Avg_mean_time']=sorted_cent[1][1]
			packet[l0]['moderate']['Nearest_data_in_per']=sorted_cent[1][0]
			packet[l0]['moderate']['requestID']=sorted_cent[1][3]
			packet[l0]['Best']['Avg_mean_time']=sorted_cent[2][1]
			packet[l0]['Best']['Nearest_data_in_per']=sorted_cent[2][0]
			packet[l0]['Best']['requestID']=sorted_cent[2][3]
		except:
			try:
				file[l0]['worst'].append(sorted_cent[0])
				file[l0]['good'].append(sorted_cent[1])
				file[l0]['Best'].append(sorted_cent[0])
				packet[l0]['worst']['Avg_mean_time']=sorted_cent[0][1]
				packet[l0]['worst']['Nearest_data_in_per']=sorted_cent[0][0]
				packet[l0]['worst']['requestID']=sorted_cent[0][3]
				packet[l0]['moderate']['Avg_mean_time']=sorted_cent[1][1]
				packet[l0]['moderate']['Nearest_data_in_per']=sorted_cent[1][0]
				packet[l0]['moderate']['requestID']=sorted_cent[1][3]
			except:
				file[l0]['worst'].append(sorted_cent[0])
				file[l0]['good'].append(sorted_cent[0])
				file[l0]['Best'].append(sorted_cent[0])
				packet[l0]['worst']['Avg_mean_time']=sorted_cent[0][1]
				packet[l0]['worst']['Nearest_data_in_per']=sorted_cent[0][0]
				packet[l0]['worst']['requestID']=sorted_cent[0][3]
		# with open('pi','wb') as f:
		# 	pickle.dump(file,f)
		plt.title(l0)
		for n in range(df.shape[0]):
			if retry[n]!=0:
				xy=(df['sent_in_ms'][n],df['timeDiff'][n])
				plt.annotate(retry[n],xy)
		return True
	except Exception as e:
		print(e)
		return False
def send_packet(packet):
	arr,new_pack=[],{}
	#print(packet)
	for l in packet:
		#print(l,packet[l]['worst']['Nearest_data_in_per'])
		try:
			if packet[l]['Best']['Nearest_data_in_per']!=0:
				ratio=packet[l]['Best']['Nearest_data_in_per']/packet[l]['worst']['Nearest_data_in_per']
				arr.append([l,ratio,packet[l]['Best']['Nearest_data_in_per'],packet[l]['worst']['Nearest_data_in_per']])
			else:
				print('It is a two faced case with Best % 0 and worst % 100')
				print(l,'Best',packet[l]['Best']['Avg_mean_time'])
				print(l,'Worst',packet[l]['worst']['Avg_mean_time'])
				#new_pack.append([l,['Best',packet[l]['Best']['Avg_mean_time']],['Worst',packet[l]['worst']['Avg_mean_time']]])
				new_pack[l]['Best']=packet[l]['Best']['Avg_mean_time']
				new_pack[l]['worst']=packet[l]['worst']['Avg_mean_time']
		except Exception as e:
			print(str(e))
	arr,str1,dface=sorted(arr, key=lambda x:x[1]),'',''
	for t in range(len(arr)):
		if arr[t][1]!=0: 
			if t==0:
				str1+='Actual:-'+str(arr[t][0])+'('+str(round(arr[t][1],2))+', Best:- '+str(round(arr[t][2],2))+'%,Worst:- '+str(round(arr[t][3],2))+'%)'
			else:
				str1+='<'+str(arr[t][0])+'('+str(round(arr[t][1],2))+', Best:- '+str(round(arr[t][2],2))+'%,Worst:- '+str(round(arr[t][3],2))+'%)'
	packet['performance']=str1
	data = {'Note':'This project is under alpha test','key':packet,'performance':str1,'ratio':arr,'zero_case':new_pack}
	#print(data)
	print(datetime.now())
	
	url='https://sokt.io/nch8356EzKi6xZsQZcyk/personal-anomaly1'
	r = requests.post(url, data =data)
	print(arr)
	prediction(arr,packet)
	#return r
def prediction(arr,packet):
	arr2,oprt_dict=[],{}
	with open('pred.pickle','rb') as f:
		data=pickle.load(f)
	with open('requestid.pickle','rb') as f:
		requestdata=pickle.load(f)
	for i in range(len(arr)):
		oprt_dict[arr[i][0]]=arr[i][1]
		ti=datetime.now().timestamp()
		l1=0
		try:
			l1=len((data[arr[i][0]]['ratio']))
		except Exception as e:
			print(str(e))
		if arr[i][0] not in data:
			data[arr[i][0]]={'ratio':[],'time':[],'BestID':[],'WorstID':[]}
		(data[arr[i][0]]['ratio']).append(arr[i][1])
		(data[arr[i][0]]['time']).append(ti/1e+8)

		if arr[i][0] not in requestdata:
			requestdata[arr[i][0]]={'index':[],'BestID':[],'WorstID':[],'ModerateID':[]}
			(requestdata[arr[i][0]]['index']).append(l1-1)
			(requestdata[arr[i][0]]['BestID']).append(packet[arr[i][0]]['Best']['requestID'])
			(requestdata[arr[i][0]]['WorstID']).append(packet[arr[i][0]]['worst']['requestID'])
			(requestdata[arr[i][0]]['ModerateID']).append(packet[arr[i][0]]['moderate']['requestID'])
		else:
			(requestdata[arr[i][0]]['index']).append(l1-1)
			(requestdata[arr[i][0]]['BestID']).append(packet[arr[i][0]]['Best']['requestID'])
			(requestdata[arr[i][0]]['WorstID']).append(packet[arr[i][0]]['worst']['requestID'])
			(requestdata[arr[i][0]]['ModerateID']).append(packet[arr[i][0]]['moderate']['requestID'])
	with open('pred.pickle','wb') as f:
		pickle.dump(data,f)
	with open('oprt.pickle','wb') as f1:
		pickle.dump(oprt_dict,f1)
	with open('requestid.pickle','wb') as f:
		pickle.dump(requestdata,f)
	future_sequence()
def future_sequence():
	arr2,str4=[],''
	with open('pred.pickle','rb') as f:
		data=pickle.load(f)
	with open('oprt.pickle','rb') as f2:
		data2=pickle.load(f2)
	for i in data:
		k=next_ratio(data[i]['ratio'],data[i]['time'],i)
		arr2.append(k)
	arr2=sorted(arr2,key=lambda x:x[1])
	print('Sorted Arr',arr2)
	print('Operators',data2)
	for t in range(len(arr2)):
		if arr2[t][1]>=0:
			if arr2[t][0] in data2: 
				if t==0:
					str4+='Predicted statitics of next 5 min:-'+str(arr2[t][0])+'('+str(round(arr2[t][1],2))+')'
				else:
					str4+='<'+str(arr2[t][0])+'('+str(round(arr2[t][1],2))+')'
	print('Sorted ',str4)
	url='https://sokt.io/3zss8oHpKuiYuuuNZMMA/anomaly_det-prediction'
	value={"pred": "Predicted statitics of next 5 min:-"+str4}
	r = requests.post(url, data =value)
def next_ratio(a,b,c):
	tj=datetime.now()
	try:
		ones=np.ones((len(b)))
		X=np.column_stack((ones,b))
		trans=np.transpose(X)
		inv_r=inv(np.matmul(trans,X))
		mult1=np.matmul(inv_r,trans)
		mult2=(np.matmul(mult1,a)).tolist()
		new_time=tj+dt_after.timedelta(minutes=5)
		timest=new_time.timestamp()/1e+8
		fut_ratio=mult2[0]+(mult2[1]*timest)
		return [c,fut_ratio]
	except Exception as e:
		print(str(e))
if __name__=='__main__':
	print('Note:-','This project is in Alpha Test.')
	db_query()
	mse.mean_error()
