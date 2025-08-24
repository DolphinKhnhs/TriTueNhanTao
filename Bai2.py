import numpy as np

lst = np.array([[1,2,3], [4,5,6], [7,8,9]])

print(lst.max())
#Giá trị lớn nhất của từng cột
print(lst.max(0))
#Giá trị lớn nhất của hàng
print(lst.max(1))