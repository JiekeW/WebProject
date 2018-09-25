n = 15
black = 1
white = 2
null = 0

def one_direction(l, p, s, d):
    i, j = p
    x, y = d
    if i+x<0 or i+x>=n or j+y<0 or j+y>=n:
        return -0.8
    if x<0 or (x==0 and y<0):
        if l[i+x][j+y] == s:
            return 'continue'
        elif l[i+x][j+y] == null:
            if 0<=i+2*x<n and 0<=j+2*y<n and l[i+2*x][j+2*y] == s:
                return 'continue'
    if l[i+x][j+y] == s:
        return 1 + one_direction(l,(i+x,j+y),s,d)
    elif l[i+x][j+y] == null:
        if i+2*x<0 or i+2*x>=n or j+2*y<0 or j+2*y>=n:
            return -0.2
        elif l[i+2*x][j+2*y] == s:
            return 0.7 + one_direction(l,(i+2*x,j+2*y),s,d)
        elif l[i+2*x][j+2*y] == null:
            return 0
        else:
            return -0.3 
    else:
        return -0.8

def get_onepoint(l,p=()):
    direction = [(-1,-1),(-1,0),(-1,1),(0,-1)]
    i, j = p
    score = 0
    for d in direction:
        if one_direction(l,p,l[i][j],d) == 'continue':
            continue
        else:
            count1 = one_direction(l,p,l[i][j],d)
            t = (-d[0],-d[1])
            count2 = one_direction(l,p,l[i][j],t)
            # if count2 >= 3:
            #     return 1000000
            # print(d,count1+count2+1)
        score += 10 ** (count1 + count2+1)
    return score

def get_allpoint(l):
    score = {'white':0, 'black':0}
    for i in range(n):
        for j in range(n):
            if l[i][j] == white:
                score['white'] += get_onepoint(l,(i,j))
            elif l[i][j] == black:
                score['black'] += get_onepoint(l,(i,j))    
    return score

def ai_answer(data):
    l = eval(data)
    op_max={}
    score = get_allpoint(l)
    if score['black'] > 15000:
        print('black win')
    next_op = {'black': score['black'], 
               'white': score['white'], 
               'rate': score['white']/score['black']}
    if score['black'] > score['white'] and score['black']>=1000:
        for i in range(n):
            for j in range(n):
                if l[i][j] == null:
                    l[i][j] = white
                    s = get_allpoint(l)
                    # print(s)
                    if s['black'] < next_op['black']:
                        next_op['black'] = s['black']
                        next_op['rate'] = s['white']/s['black']
                        next_op['position'] = (i,j)
                    elif s['black'] == next_op['black']:
                        if s['white']/s['black'] > next_op['rate']:
                            next_op['black'] = s['black']
                            next_op['rate'] = s['white']/s['black']
                            next_op['position'] = (i,j)
                    l[i][j] = null
    else:
        for i in range(n):
            for j in range(n):
                if l[i][j] == null:
                    l[i][j] = white
                    s = get_allpoint(l)
                    # print(s)
                    if s['white'] >= 1000:
                        if not op_max:
                            op_max['position'] = (i,j)
                            op_max['white'] = s['white']
                        elif s['white'] > op_max['white']:
                            op_max['position'] = (i,j)
                            op_max['white'] = s['white']
                    if s['white']/s['black'] > next_op['rate']:
                        next_op['black'] = s['black']
                        next_op['rate'] = s['white']/s['black']
                        next_op['position'] = (i,j)
                        next_op['white'] = s['white']
                    elif s['white']/s['black'] == next_op['rate']:
                        if s['black'] < next_op['black']:
                            next_op['black'] = s['black']
                            next_op['rate'] = s['white']/s['black']
                            next_op['position'] = (i,j)
                            next_op['white'] = s['white']
                    l[i][j] = null
    if op_max:
        score = op_max['white']
        position = op_max['position']
    else:
        score = next_op['white']
        position = next_op['position']
    if score > 15000:
        print('white win')
    return position