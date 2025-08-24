import math


def GiaiPT(arr):
     if len(arr) == 2:
          a = arr[0]
          b = arr[1]
          if a == 0:
               if b == 0:
                    return "Phương trình có vô số nghiệm"
               else:
                    return "Phương trình vô nghiệm"
          else:
               return f"Nghiệm của phương trình là: {-b/a}"
     if len(arr) == 3:
          c = arr[0]
          d = arr[1]
          e = arr[2]
          if c == 0:
               return GiaiPT([d,e])
          delta = pow(d,2) - 4*c*e
          if delta < 0:
               return "Phương trình vô nghiệm"
          elif delta == 0:
               return f"Phương trình có nghiệm kép: {-d/(2*c)}"
          else:
               x1 = (-d + math.sqrt(delta))/2*c
               x2 = (-d - math.sqrt(delta))/2*c
               return f"Nghiệm của phương trình là: x1 = {x1}, x2 = {x2}"
     else:
          return "Vui lòng nhập 2 hoặc 3 số"
          

print(GiaiPT([0,0]))
print(GiaiPT([0,1]))
print(GiaiPT([0,1,2]))
print(GiaiPT([1, -4, 3]))