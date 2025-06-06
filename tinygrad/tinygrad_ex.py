from tinygrad import Tensor
 
 
a = Tensor.empty(4)
a.sum(0).realize()