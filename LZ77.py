from CircularQueue import *
import sys
import os

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
			#print("found", q.queue[i], ' at ', i)
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
	does_end_match=False
	while(True):
		if(q.queue[a]!=q.queue[b]) or (i==LOOK_SIZE-1):
			break
		i+=1

		if((b+1)%(SEARCH_SIZE+LOOK_SIZE+1) in right_nulls):
			does_end_match=True
			break
		a=(a+1)%(SEARCH_SIZE+LOOK_SIZE+1)
		b=(b+1)%(SEARCH_SIZE+LOOK_SIZE+1)
	return ((divider-startpos)%(SEARCH_SIZE+LOOK_SIZE+1),i,q.queue[b],does_end_match)

SEARCH_SIZE=1024
LOOK_SIZE=32
non_null_count=0
right_nulls=[]

def encode(data, byte_list):
	#datastr="sir sid eastman easily teases sea sick seals"
	#data=bytearray()
	#data.extend(datastr.encode())

	#data="HHHHHH"
	#data="\0\0\0\0\0\0"
	global non_null_count
	global right_nulls
	non_null_count=0
	right_nulls=[]
	q=CircularQueue(SEARCH_SIZE+LOOK_SIZE+1)
	data_ptr=LOOK_SIZE
	non_null_count=0
	right_nulls=[]
	x=False
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
		#print('----------------------------')
		#q.displaylinear(divider)

		
		(status,startpos)=find_start(q,divider,divider)
		if(status==True):
			(D,L,c,x)=find_substring(q,startpos,divider)
			
			while(True):
				temp_non_null_count=non_null_count
				non_null_count-=(divider-startpos)%(SEARCH_SIZE+LOOK_SIZE+1)

				(status_,startpos)=find_start(q,startpos,divider)
				non_null_count=temp_non_null_count

				if(status_==False):
					break
				(D_new,L_new,c_new,x_new)=find_substring(q,startpos,divider)
				if(L_new>=L):
					D=D_new
					L=L_new
					c=c_new
					x=x_new

				if(startpos==q.head):
					break

			#print (D,L,chr(c))
			byte_list.append(D>>3)
			byte_list.append(((D & 7)<<5) + L)
			byte_list.append(c)

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
			if(x==True):
				byte_list.append(255)
			break
		if(status==False):
			#print(0,0,chr(q.queue[divider]))
			byte_list.append(0)
			byte_list.append(0)
			byte_list.append(q.queue[divider])

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

def extract(byte_list):
	extracted=[]
	i=0
	k=0
	does_end_match=False
	if(len(byte_list)%3 != 0):
		does_end_match=True
		

	while (i <len(byte_list)-1):
		D=(byte_list[i]<<3)+(byte_list[i+1]>>5)
		L=byte_list[i+1] & 31
		c=byte_list[i+2]

		#print(D,L,chr(c))
		
		if(L==0):
			extracted.append(c)
			k+=1
		else:
			j=k-D
			
			for count in range (L):
				extracted.append(extracted[j])
				k+=1
				j+=1
			extracted.append(c)
			k+=1

		i+=3
	
	if(does_end_match==True):
		extracted.pop()
	op_str=[]
	for w in range (len(extracted)):
		op_str.append(extracted[w])

	#print(op_str)
	return op_str


if(sys.argv[1]=="-c"):
	file=open(sys.argv[2],"rb")
	data=file.read()
	file.close()

	byte_list=[]
	encode(data,byte_list)

	file=open(sys.argv[2] + ".LZ77","wb")
	file.write(bytearray(byte_list))
	file.close()

elif(sys.argv[1]=="-e"):
	file=open(sys.argv[2],"rb")
	byte_list=file.read()
	file.close()

	op_str=extract(byte_list)

	file=open(os.path.splitext(os.path.splitext(sys.argv[2])[0])[0] + "_extracted" + os.path.splitext(os.path.splitext(sys.argv[2])[0])[1],"wb")
	file.write(bytearray(op_str))
	file.close()

