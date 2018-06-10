def parse_csv_line(s,sep=',',quote='"'):
    '''
    Parses one CSV line
    Gets fragments as list of 3-lists: [offset_start, offset_end, kind]
    kind: -1 for comma, 0+ for column
    '''
    if s=='' or s==None:
        return []
    res=[]
    col,x,b=0,0,True
    for i,c in enumerate(s):
        if c==sep and b:
            if x!=i:
                res.append([x,i,col])
                res.append([i,i+1,-1])
            else:
                if i!=0:
                    res[-1][1]+=1
                else:
                    res.append([0,1,-1])
            x=i+1
            col+=1
        elif c==quote:
            b=not b
    if x!=len(s):
        res.append([x,len(s),col])
    if not b:
        return []
    s=s.replace(quote*2,'')
    i=-1
    while True:
        i=s.find(quote,i+1)
        if i==-1:
            return res
        if not (i==0 or s[i-1]==sep):
            break
        i=s.find(quote,i+1)
        if not (i==len(s)-1 or s[i+1]==sep):
            break
    return []
