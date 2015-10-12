class Stack(object):
    def __init__(self):
        self.stack = []
    def __str__(self):
        return '%s' % self.stack
    def push(self,item):
        self.stack.append(item)
    def pop(self):
        return self.stack.pop()
    def isEmpty(self):
        if len(self.stack) ==0 :
            return True
        return False
    def peek(self):
        if not self.isEmpty():
            return self.stack[-1]
        return 'Stack Is Empty!'
    def size(self):
        return len(self.stack)



def checksyntax(string):
    s = Stack()
    mark = 0
    balance = True
    for word in string:
        if word in '[{(':
            mark = 1
            s.push(word)
        if word in '}])' :
            if s.isEmpty():
                return False
            else:
                s.pop()
    if mark == 1 and s.isEmpty() or mark == 0:
        return True
    else:
        return False



print checksyntax('{[str({sss)}dd}]')