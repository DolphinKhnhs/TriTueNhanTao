import math
lst = [1, 1]

def giaithua(n):
     if n < len(lst):
          return lst[n]
     result = n*giaithua(n-1)
     lst.append(result)
     return result

cosx = 0
n = int(input("Nhap n: "))
x = float(input("Nhap x: "))
i=0
while(i<n):
     cosx += pow(-1,i)*(pow(x,i*2)/giaithua(2*i))
     i+=1
print(f"cos(x) = {cosx}")


