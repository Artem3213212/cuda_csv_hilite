import os
from cudatext import *

fn_config = os.path.join(app_path(APP_DIR_SETTINGS), 'cuda_csv_hilite.ini')

option_int = 100
option_bool = True

def bool_to_str(v): return '1' if v else '0'
def str_to_bool(s): return s=='1'

def parse_csv_line(s,sep=',',quote='"'):
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
	if not(i==0 or s[i-1]==sep):
	    break
	i=s.find(quote,i+1)
	if not(i==len(s)-1 or s[i+1]==sep):
	    break
    return []

class Command:
    
    def __init__(self):

	global option_int
	global option_bool
	option_int = int(ini_read(fn_config, 'op', 'option_int', str(option_int)))
	option_bool = str_to_bool(ini_read(fn_config, 'op', 'option_bool', bool_to_str(option_bool)))

    def config(self):

	ini_write(fn_config, 'op', 'option_int', str(option_int))
	ini_write(fn_config, 'op', 'option_bool', bool_to_str(option_bool))
	file_open(fn_config)
	
    def run(self):
	s = '''
	file lines count: {cnt}
	option_int: {i}
	option_bool: {b}
	'''.format(
	     cnt = ed.get_line_count(),
	     i = option_int,
	     b = option_bool,
	     )
	msg_box(s, MB_OK)

    def on_open(self, ed_self):
	pass
    def on_scroll(self, ed_self):
	pass
