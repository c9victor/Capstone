class Node:
    def __init__(self, num=None):
        self.num = num
        self.next = None 
        self.prev = None 

    def __repr__(self) -> str: 
        return self.num


class LinkedList:
    def __init__(self):
        self.head = None
        self.last = None
    
    def print_nodes(self):
        node = self.head
        if node is None:
            return
        string = str(node.num)
        node = node.next
        while node is not self.head:
            string = string + " " + str(node.num)
            node = node.next
        print(string)

    def print_list(self):
        # list is empty
        if self.head is None:
            print("Empty")
            return
        node = self.head 
        # only one Node exists
        if node.next == node.prev == node:
            print("Prev:", node.prev.num, "\tVal: ", node.num, "\tNext:", node.next.num)
            return
        # two Nodes exists
        if node.next == node.prev:
            print("Prev:", node.prev.num, "\tVal: ", node.num, "\tNext:", node.next.num)
            print("Prev:", node.num, "\tVal: ", node.next.num, "\tNext:", node.num)
            return

        # general
        print("Prev:", node.prev.num, "\tVal: ", node.num, "\tNext:", node.next.num)
        node = node.next
        while node is not self.head:
            print("Prev:", node.prev.num, "\tVal: ", node.num, "\tNext:", node.next.num)
            node = node.next

    def add_first(self, node):
        # only one Node exists
        if self.head is None:
            self.head = node
            self.last = node
            self.head.next = self.head
            self.head.prev = self.head
            return
        # adding a second Node
        if self.head.next == self.head:
            self.head.next = node
            node.prev = self.head
        # general
        else:
            node.prev = self.last
            self.last.next = node
        if self.head is not None:
            self.head.prev = node   
        node.next = self.head   
        self.head = node   
    
    #NOT FINISHED YET
    def add_last(self, node):
        if self.last is None:
            self.last = node
            self.last.next = self.last
            self.last.prev = self.last
            return
        if self.last is not None:
            self.last.next = node
        node.prev = self.last
        self.last = node 

    def remove(self, num):
        travel = self.head
        while travel.num != num:
            travel = travel.next
        if travel == self.head:
            self.head = self.head.next
        if travel == self.last:
            self.last = self.last.prev
        travel.next.prev = travel.prev
        travel.prev.next = travel.next

    def restore(self, num):
        print('how do')

'''
Every row and col of the matrix consists of a circular doubly-linked list of nodes
'''
class DLX:
    def __init__(self):
        self.matrix = [[LinkedList() for x in range(9)] for y in range(9)]
        for r in self.matrix:
            for c in r:
                for i in range(9):
                    c.add_first(Node(0))
    
    def print_matrix(self):
        cnt = 1
        for r in self.matrix:
            for c in r:
                print(cnt)
                cnt += 1
                c.print_nodes()


# list1 = LinkedList()
# list1.add_first(Node(3))
# list1.add_first(Node(4))
# list1.add_first(Node(5))
# list1.print_nodes()
# list1.remove(5) 
# list1.print_list()
dlx = DLX()
dlx.print_matrix()