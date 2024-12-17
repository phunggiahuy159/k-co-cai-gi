# def Try(k): 
#     global f
#     global load
#     global distance
#     global visited
#     global fs
#     for v in range(1,2*n+1):
#         if check(v):
#             cmin = 1
#             x[k] = v
#             f = f + distance[k-1][v]
#             visited[v] = True
#             if v<=n:
#                 load+=1
#             else:
#                 load-=1
#             if k == 2*n:
#                 updateBest()
#             else:
#                 if f + cmin*(2*n+1 - k) < fs:
#                     Try(k+1)
#             if v <= n:
#                 load-=1
#             else:
#                 load +=1
#             f = f - distance[k-1][v]
#             visited[v] = False