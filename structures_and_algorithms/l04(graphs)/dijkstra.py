class dijkstra_struct:
    def __init__(self, limit=100):
        # self.lst - heap
        # self.lst[i][0] - distance to vertex, self.lst[i][1] - vertex number
        self.lst = [None] * (limit + 1)
        # i - i-th vertex in self.vert
        # self.vert[i][0] - dist, self.vert[i][1] - previous vertex, 
        # self.vert[i][2] - visited or not,  self.vert[i][3] - index in self.lst
        self.vert = [None] * (limit + 1)
        self.size = 0
    
    
    def swap(self, i, j):
        #swap elements in heap
        self.lst[i], self.lst[j] = self.lst[j], self.lst[i]
        i = self.lst[i][1]
        j = self.lst[j][1]
        #swap position in heap for two vertex
        self.vert[i][3], self.vert[j][3] = self.vert[j][3], self.vert[i][3]
    
    
    def push_up(self, ind):
        par = ind // 2
        while (ind > 1 and self.lst[ind][0] < self.lst[par][0]):
            self.swap(ind, par)
            ind = par
            par //= 2
    
    
    def push_down(self, ind):
        child_1 = ind * 2
        while (child_1 <= self.size):
            min_child = child_1
            if (child_1 + 1 <= self.size):
                # if right child > left child: min_child += 1
                a = self.lst[child_1][0] > self.lst[child_1 + 1][0]
                min_child += a
            # if current elem < min_child: swap them
            if self.lst[min_child][0] < self.lst[ind][0]:
                self.swap(ind, min_child)
                ind = min_child
                child_1 = ind * 2
            else:
                return

                
    def add_elem(self, dist, vert):
        self.size += 1
        # if lst over, double it`s size
        if (self.size > len(self.lst) - 1):
            self.lst += [None] * self.size
        
        ind = self.size
        # record elem in heap
        self.lst[ind] = [dist, vert]
        # record vertex heap position
        self.vert[vert][3] = ind
        # change heap position
        self.push_up(ind)
    
    
    # change information about vert in heap
    def alter(self, vert):
        # find index in heap
        lst_ind = self.vert[vert][3]
        # record new distance in heap
        self.lst[lst_ind][0] = self.vert[vert][0]
        # change heap position
        self.push_up(lst_ind)
    
    
    def pop(self):
        if (self.size == 0):
            return (-1)
        # find vertex with min distance, swap with last elem
        min_ind = self.lst[1][1]
        self.swap(1, self.size)
        self.size -= 1
        # if there are more than 1 elem, push down new first elem
        if (self.size > 1):
            self.push_down(1)
        self.vert[min_ind][3] = None
        return(min_ind)
    
    
def input_graph(n, m):
    lst = [None] * (n + 1)
    for _ in range(m):        
        a, b, w = map(int, input().split())
        if lst[a] == None:
            lst[a] = [[b, w]]
        else:
            lst[a].append([b, w])
        if lst[b] == None:
            lst[b] = [[a, w]]
        else:
            lst[b].append([a, w])
    return lst


def dijkstra_alg(lst, data):
    data.vert[1] = [0, 0, 1, None]
    data.add_elem(0, 1)
    if (lst[1] == None):
        return
    while (data.size > 0):
        # take vertex with min distance
        cur_vert = data.pop()
        # for each related vertex change distance if it`s necessary
        for elem in lst[cur_vert]:
            next_vert = elem[0]
            # count general distance through cur_vert
            dist = data.vert[cur_vert][0] + elem[1]
            
            # if it`s new vertex, record data
            if data.vert[next_vert] == None:
                data.vert[next_vert] = [dist, cur_vert, 0, None]
                data.add_elem(dist, next_vert)

            # if new way was found, change data
            elif data.vert[next_vert][0] > dist:
                data.vert[next_vert][0] = dist
                data.vert[next_vert][1] = cur_vert
                data.alter(next_vert)

def main(n, m, lst=None):
    if (lst == None):
        lst = input_graph(n, m)
    data = dijkstra_struct(n)
    dijkstra_alg(lst, data)
    elem = data.vert[n]
    if (elem == None):
        print(-1)
        return
    tmp_lst = [None] * n
    i = n
    vert = n
    while (data.vert[vert] != None):
        i -= 1
        tmp_lst[i] = vert
        vert = data.vert[vert][1]
    while (i < n):
        print(tmp_lst[i], end=' ')
        i += 1
    return

n, m = map(int, input().split())
main(n, m)