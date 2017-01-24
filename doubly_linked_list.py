class Node():
    def __init__(self, payload):
        self.payload = payload
        self.prev = None
        self.next = None
 
class DoubleList():
    def __init__(self):
        self.head = None
        self.tail = None

 
    def append(self, payload):
        new_node = Node(payload)
        new_node.prev = self.tail

        if self.tail is None:
            self.head = self.tail = new_node
        else:
            temp_node = self.tail
            self.tail.next = new_node
            self.tail = self.tail.next
            self.tail.prev = temp_node


    def reverse(self):
        current_node = self.head
        temp_node = None
        while current_node is not None:
            temp_node = current_node.prev;
            current_node.prev = current_node.next;
            current_node.next = temp_node;
            current_node = current_node.prev

        self.head = temp_node.prev


    def remove(self, node_value):
        current_node = self.head
 
        while current_node is not None:
            if current_node.payload == node_value:
                if current_node.prev is not None:
                    current_node.prev.next = current_node.next
                    current_node.next.prev = current_node.prev
                else:
                    self.head = current_node.next
                    current_node.next.prev = None
 
            current_node = current_node.next


    def show(self):
        current_node = self.head
        while current_node is not None:
            print( current_node.payload)
            current_node = current_node.next
 
 
d = DoubleList()
 
d.append(1)
d.append(2)
d.append(3)
d.append(4)

d.show()

d.reverse()

d.show()
 
# d.remove(50)
# d.remove(5)
 
# d.show()