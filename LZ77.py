from CircularQueue import *

def find_start(q,searchstart,divider):
	if(searchstart==q.head):
		return(False,0)
	i=searchstart-1
	ctr=0
	if i==-1:
		i=SEARCH_SIZE+LOOK_SIZE
	flag=0
	while(True):
		if(i==q.head):
			flag=1
		if(ctr==non_null_count):
			break
		if(q.queue[i]==q.queue[divider]):
			print("found", q.queue[i], ' at ', i)
			return (True,i)
		i-=1
		if(i==-1):
			i=SEARCH_SIZE+LOOK_SIZE
		ctr+=1
		if(flag==1):
			break
	return (False,0)

def find_substring(q,startpos,divider):
	i=0
	a=startpos
	b=divider
	
	while(True):
		if(q.queue[a]!=q.queue[b]) or (i==LOOK_SIZE-1):
			break
		i+=1

		if((b+1)%(SEARCH_SIZE+LOOK_SIZE+1) in right_nulls):
			break
		a=(a+1)%(SEARCH_SIZE+LOOK_SIZE+1)
		b=(b+1)%(SEARCH_SIZE+LOOK_SIZE+1)
	return ((divider-startpos)%(SEARCH_SIZE+LOOK_SIZE+1),i,q.queue[b])

SEARCH_SIZE=4096
LOOK_SIZE=64

data="sir sid eastman easily teases sea sick seals"
#data="HHHHHH"
#data="\0\0\0\0\0\0"

q=CircularQueue(SEARCH_SIZE+LOOK_SIZE+1)
data_ptr=LOOK_SIZE
non_null_count=0
right_nulls=[]
divider=SEARCH_SIZE
window=[]
#Fill search buffer (Dictionary) with nulls
for i in range(SEARCH_SIZE):
	q.enqueue('\0')


#Fill lookahead buffer with data
i=0
while(i<LOOK_SIZE and i<len(data)):
	q.enqueue(data[i])
	i+=1

i=0
while(i<LOOK_SIZE-len(data)):
	right_nulls.append(q.enqueue('\0'))
	i+=1

while True:
	print('----------------------------')
	q.displaylinear(divider)

	
	(status,startpos)=find_start(q,divider,divider)
	if(status==True):
		(D,L,c)=find_substring(q,startpos,divider)
		
		while(True):
			temp_non_null_count=non_null_count
			non_null_count-=(divider-startpos)%(SEARCH_SIZE+LOOK_SIZE+1)

			(status_,startpos)=find_start(q,startpos,divider)
			non_null_count=temp_non_null_count

			if(status_==False):
				break
			(D_new,L_new,c_new)=find_substring(q,startpos,divider)
			if(L_new>=L):
				D=D_new
				L=L_new
				c=c_new

			if(startpos==q.head):
				break

		print (D,L,c)
		for i in range (L):
			q.dequeue()
			if(data_ptr<len(data)):
				q.enqueue(data[data_ptr])
			else:
				right_nulls.append(q.enqueue('\0'))

			data_ptr+=1
			divider+=1
			if divider==SEARCH_SIZE+LOOK_SIZE+1:
				divider=0
			if non_null_count<=SEARCH_SIZE:
				non_null_count+=1
			if(divider in right_nulls):
				break


	if(divider in right_nulls):
		break
	if(status==False):
		print(0,0,q.queue[divider])
	q.dequeue()
	if(data_ptr<len(data)):
		q.enqueue(data[data_ptr])
	else:
		right_nulls.append(q.enqueue('\0'))
	data_ptr+=1
	divider+=1
	if divider==SEARCH_SIZE+LOOK_SIZE+1:
		divider=0
	if non_null_count<=SEARCH_SIZE:
		non_null_count+=1

	
	
	
	





	

	


