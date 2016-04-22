#coding: utf8
# ss = lambda f, arr: arr if len(arr) < 2 else [max(arr)] + f(ss, arr[0: arr.index(max(arr))] + arr[arr.index(max(arr))+1 :])
# print ss(ss, [4,3,6,7,9,2,8])

ssort = lambda arr: arr if len(arr) < 2 else [max(arr)] + ssort(arr[0: arr.index(max(arr))] + arr[arr.index(max(arr))+1 :])
print ssort([4,3,6,7,9,2,8])