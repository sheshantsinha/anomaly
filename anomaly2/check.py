import matplotlib.pyplot as plt 
import pickle as pi 
import predict 
def main():
	with open('pi','rb') as f: 
		data=pi.load(f)
	lt,count=[],0
	print('Select any one of the following to visualize graph')
	for i in data:
		lt.append(i)
		print(count,i)
		count+=1
	print('Press any other key to visualize all graphs')
	try:
		r=int(input('Enter number:-'))
	except:
		print('Only integers are allowed.')
		exit()
	if r>=0 and r<count:
		predict.main(True,lt[r])
	else:
		predict.main(False,'No')
if __name__=='__main__':
	main()
	r=input('Would you like to visualize more graphs?(yes/no)')
	if r.lower()=='yes':
		main()
	else:
		exit()
