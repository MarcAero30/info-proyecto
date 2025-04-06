from node import *
from segment import *
n1 = Node ('aaa', 0, 0)
n2 = Node ('bbb', 3, 4)
n3 = Node ("ccc",6,0)
s12 = Segment("s12",n1,n2)
s23 = Segment("s23",n2,n3)
ShowSegment(s12)
ShowSegment(s23)