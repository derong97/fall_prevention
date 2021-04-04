import numpy as np

# frames = np.load("/Users/glendawee/Desktop/sit_003.npy")
# print (frames)

# for i in frames: 
#     print (i)

arr1 = np.array([1,2,3,4])
arr2 = np.array([5,6,7,8])


arr3 = np.append(arr1, arr2) 
arr4 = np.vstack((arr1, arr2)) 

print (arr3) 

print (arr4) 

print(arr4[1])