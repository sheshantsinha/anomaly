import pickle as pi
import matplotlib.pyplot as plt
from sklearn import linear_model,datasets 
from sklearn.metrics import mean_squared_error,r2_score 
import numpy as np
from numpy.linalg import inv
import math
def writeinfile(coef,mse,opr):
	print(coef,mse,opr)
	with open('coeff.pickle','rb') as f:
		data=pi.load(f)
	print(data)
	if opr not in data:
		data[opr]={'B0':0,'B1':0,'mse':0}
		data[opr]['B0']=coef[0]
		data[opr]['B1']=coef[1]
		data[opr]['mse']=mse
	else:
		data[opr]['B0']=coef[0]
		data[opr]['B1']=coef[1]
		data[opr]['mse']=mse
	#print(data)
	with open('coeff.pickle','wb') as f:
		pi.dump(data,f)
def linear_reg(oprtx,oprty,opr,n):
	print('Note:-','This linear regression pattern is not accurate.\n','Error is very high')
	try:
		ones=np.ones((len(oprtx)))
		X=np.column_stack((ones,oprtx))
		trans=np.transpose(X)
		inv_r=inv(np.matmul(trans,X))
		mult1=np.matmul(inv_r,trans)
		mult2=(np.matmul(mult1,oprty)).tolist()
		print('Coe',mult2)
		y_pred=[]
		for i in oprtx:
			y_pred.append(mult2[0]+(mult2[1]*i))
		y_pred,oprty=np.array(y_pred),np.array(oprty)
		mse=math.sqrt(np.mean(np.square(y_pred-oprty)))
		print(mean_squared_error(y_pred,oprty))
		print('MSE',mse)
		writeinfile(mult2,mse,opr)
		plt.figure(n)
		plt.title(opr)
		plt.scatter(oprtx,oprty)
		plt.plot(oprtx,y_pred,'green')
	except Exception as e:
		print(e)
print('Note:-','This project is in Alpha Test.')
def main(oprtt,oprt_name):
	with open('pi','rb') as f:
		data=pi.load(f)
	if oprtt==False:
		n=1
		for i in data:
			plt.figure(n)
			oprtx,oprty=[],[]
			for j in data[i]:
				color,cl=['yellow','green','red'],'pink'
				if j=='good':
					cl=color[0]
				elif j=='Best':
					cl=color[1]
				else:
					cl=color[2]
				arrn=sorted(data[i][j],key=lambda x:x[2])
				arrx,arry,arrz=[],[],[]

				for x in range(len(data[i][j])):
					if arrn[x][1] >=0 and arrn[x][2] >=0:
						#if j != 'worst':
						arrx.append(arrn[x][2])   #time
						arry.append(arrn[x][1])	  #time difference
						arrz.append(arrn[x][0])	  #% of data lies
						oprtx.append(arrn[x][0])
						oprty.append(arrn[x][1])
					#plt.scatter(data[i][j][x][2],data[i][j][x][1],label=data[i][j][x][0])
						#print(i,j,str(len(data[i][j])))
			#linear_reg(oprtx,oprty,i,n)
		#		print(i,j,len(arrn))
				plt.plot(arrx,cl)
				plt.xlabel('Time')
				plt.ylabel('Mean time difference')
			plt.title(i)
			n+=1
	else:
		i=oprt_name
		oprtx,oprty=[],[]
		for j in data[i]:
			color,cl=['yellow','green','red'],'pink'
			if j=='good':
				cl=color[0]
			elif j=='Best':
				cl=color[1]
			else:
				cl=color[2]
			arrn=sorted(data[i][j],key=lambda x:x[2])
			arrx,arry,arrz=[],[],[]
			for x in range(len(data[i][j])):
				if arrn[x][1] >=0 and arrn[x][2] >=0:
					#if j != 'worst':
					arrx.append(arrn[x][2])   #time
					arry.append(arrn[x][1])	  #time difference
					arrz.append(arrn[x][0])	  #% of data lies
					oprtx.append(arrn[x][0])
					oprty.append(arrn[x][1])
				#plt.scatter(data[i][j][x][2],data[i][j][x][1],label=data[i][j][x][0])
					#print(i,j,str(len(data[i][j])))
		#linear_reg(oprtx,oprty,i,n)
	#		print(i,j,len(arrn))
			plt.plot(arrx,arry,cl)
			plt.xlabel('Time')
			plt.ylabel('Mean time difference')
		plt.title(oprt_name)
	plt.show()

if __name__=='__main__':
	main(False,'No')