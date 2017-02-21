class Node():
    def __init__(self, payload):
        self.payload = payload
        self.next = None
 
class DoubleList():
    def __init__(self):
        self.head = None
        self.tail = None

    def append(self, payload):
        new_node = Node(payload)
        new_node.next = None

        if (self.tail is not None):
            self.tail.next = new_node
            self.tail = self.tail.next
        else:
            self.head = new_node
            self.tail = self.head

    def reverse(self):
        current_node = self.head
        last_node = None
        while (current_node is not None):
            temp_node = current_node.next
            current_node.next, last_node = last_node, current_node
            current_node = temp_node

        return last_node

    def reverse_r(self, current_node):
        if (current_node is None):
            return None

        temp_node = current_node.next;
        if (temp_node is None):
            return None

        self.reverse_r(temp_node);
        temp_node.next = current_node;
        current_node.next = None;
        current_node = temp_node;
        return self.tail

    def print_payload(self):
        current_node = self.head
        while current_node is not None:
            print( current_node.payload)
            current_node = current_node.next
 
 
d = DoubleList()
 
d.append(1)
d.append(2)
d.append(3)
d.append(4)

d.print_payload()

d.head = d.reverse_r(d.head)

d.print_payload()
 
# d.remove(50)
# d.remove(5)
 
# d.show()