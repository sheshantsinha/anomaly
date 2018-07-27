from pymongo import MongoClient
import pandas as pd
from datetime import datetime
from sklearn.cluster import KMeans  
import matplotlib.pyplot as plt
import numpy as np 
import pickle
from bson import ObjectId
plt.rcParams['figure.figsize'] = (5, 4)
def db_query():
	client=MongoClient('mongodb+srv://mongoAppUser:rp_JWzg.ZaE8B@msg91-prod-j98or.mongodb.net/admin')
	db=client['msg91_betatest']
	coll=db['ms_text_report_otp']
	coll2=db['ms_text_request_otp']
	jj=coll.count()
	print(jj)
	d=coll.find().sort([('_id',-1)]).limit(1000)
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
	d2=coll2.find({'_id':{'$in':limx}})
	for dd in d2:
		my_dict['sentTime'][lim_dict[dd['_id']]]=dd['requestDateString']
	for i in my_dict:
		print(i,len(my_dict[i]))
	df=pd.DataFrame(my_dict)
	df.to_csv('new_data.csv',index=False)
	time_integer(df)

def time_integer(df):
	ds=df['sentTime']
	dt=df['deliveryTime']
	li=df.columns.tolist()
	timeDiff,sent_mili,req_arr,route,diff_arr=[],[],[],[],[]
	#print(my_dict)
	ref_dict={'requestID':[],'route':[],'timeDiff':[],'sent_in_ms':[],'smsc':[],'retryCount':[]}
	for i in range(df.shape[0]):
		try:
			tt=datetime.strptime(str(ds[i]),'%Y-%m-%d %H:%M:%S')
		except:
			tt=datetime.strptime(str(ds[i]),'%Y-%m-%d %H:%M:%S.%f')
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
	counton,plotx=3,1
	for l in arr2:
		df=pd.DataFrame(route_dict[l])
		if(clustering(df,l,counton,plotx,li)==False):
			counton-=1
			#clustering(df,l,1,plotx,li)
		plotx+=1
	#plt.show()
	print('Array l',len(arr2))

def clustering(df,l0,clust,px,li):
	X=np.array(list(zip(df['sent_in_ms'],df['timeDiff'])))
	retry=df['retryCount']
	clusters=clust
	try:
		kmean=KMeans(n_clusters=clusters)
		train_data=X[0:int((len(X))*0.7)]
		test_data=X[int((len(X))*0.7):len(X)]
		kmean=kmean.fit(train_data)
		labels=kmean.predict(test_data)
		centroid=kmean.cluster_centers_
		cent=centroid.tolist()
		arrx,arry,arrperc=[],[],[]
		for p in range (clusters):
			arrx.append([])
			arry.append([])
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
			#print('Precentage around centroid '+str(cent[i][1])+'='+str(lenx)+'%')
			plt.scatter(arrx[i],arry[i])
			plt.scatter(cent[i][0],cent[i][1],color='red',label=str(cent[i][1])+'='+str(lenx)+'%')
		sorted_cent=sorted(arrperc,key=lambda l:l[1], reverse=True)
		print(l0)
		lab=['Worst :','Moderate :','Best :']
		with open('coeff.pickle','rb') as f:
			file=pickle.load(f)
		for m in range(len(sorted_cent)):
			print(lab[m]+' '+str(sorted_cent[m][2])+' '+str(sorted_cent[m][1])+' '+str(sorted_cent[m][0]))
			if l0 in file:
				b1=file[l0]['B1']
				b0=file[l0]['B0']
				y_pred=b0+b1*sorted_cent[m][2]
				print(l0,lab[m])
				print('Predicted',y_pred)
				print('Actual',sorted_cent[m][1])
				print('Deviation',(sorted_cent[m][1]-y_pred)*100/sorted_cent[m][1])			
		plt.title(l0)
		return True
	except Exception as e:
		print(e)
		return False

if __name__=='__main__':
	db_query()
	