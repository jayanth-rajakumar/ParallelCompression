class CircularQueue:

    #Constructor
    def __init__(self,max):
        self.queue = [None]*max
        self.head = 0
        self.tail = 0
        self.maxSize = max

    #Adding elements to the queue
    def enqueue(self,data):
        if self.size() == self.maxSize-1:
            print ("Queue Full!")
            return 1
        self.queue[self.tail]=data
        pos=self.tail
        self.tail = (self.tail + 1) % self.maxSize
        return pos

    #Removing elements from the queue
    def dequeue(self):
        if self.size()==0:
            print ("Queue Empty!") 
            return 1
        data = self.queue[self.head]
        self.head = (self.head + 1) % self.maxSize
        return data

    #Calculating the size of the queue
    def size(self):
        if self.tail>=self.head:
            return (self.tail-self.head)
        return (self.maxSize - (self.head-self.tail))

    def displaylinear(self,divider):
        
        i=self.head
        display_str=''
        while(i!=self.tail):
            
            if(i==divider):
                display_str+='|'
            display_str+=self.queue[i]
            i+=1
            if(i==self.maxSize):
                i=0
        print(display_str)
        

