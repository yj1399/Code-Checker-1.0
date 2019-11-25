import difflib
import re
import os
import time 
start = time.time()
path = '/home/yash/Downloads/'
first_file =  path + 'file_1.txt'
second_file = path + 'file_2.txt'
ff = open(first_file ,'r').readlines()
sf = open(second_file ,'r').readlines()
def chunk(l,n):
    for i in range(0,len(l),n):
        yield l[i:i+n]
if len(ff) or len(sf) > 100 :
    ff_len = len(ff)
    sf_len = len(sf)
    if ff_len != sf_len :
        if ff_len > sf_len :
            for x in range(ff_len-sf_len):
                sf.append('\n')
        else:
            for x in range(sf_len-ff_len):
                ff.append('\n') 
    ff_list = list(chunk(ff,100))
    sf_list = list(chunk(sf,100))
    dictionary = {'ff':ff_list , 'sf':sf_list}
    for key,value in dictionary.items():
        n=0
        for elem in value:
            with open(path+'file_tmp_'+str(key)+'_{}.txt'.format(n),'w') as f:
                for line in elem:
                    f.write(line)
            print('file_tmp_'+str(key)+'{}.txt is created....'.format(n))
            n+=1
    
    for i in range(len(ff_list)):
        first_chunk = path+'file_tmp_ff_{}.txt'.format(i)
        second_chunk = path+'file_tmp_ff_{}.txt'.format(i)
        if i==0:
            difference0 = difflib.HtmlDiff().make_file(ff_list[i],sf_list[i],first_chunk,second_chunk)
        else:
            difference = difflib.HtmlDiff().make_file(ff_list[i],sf_list[i],first_chunk,second_chunk)
            tbody = difference[difference.find('<tbody>')+len('<tbody>'):difference.find('</tbody>')]
            tbody_list = tbody.split('\n')
            n=1
            for line in tbody_list[1:-1]:
                no=re.search('id="from(\d*)_'+str(n)+'">'+str(n)+'<',line)
                line = line.replace('id="from'+str(no)+'_'+str(n)+'">'+str(n)+'<' ,'id="from'+str(no)+'_'+str(n+i*100)+'">'+str(n+i*100)+'<',1) 
                tbody_list[n] = line.replace('id="to'+str(no)+'_'+str(n)+'">'+str(n)+'<' ,'id="to'+str(no)+'_'+str(n+i*100)+'">'+str(n+i*100)+'<',1) 
                n+=1
            tbody='\n'.join(tbody_list)
            diff_split = difference0.split('</tbody>')
            difference0 = diff_split[0]+tbody+'</tbody>'+diff_split[1]
        print('Generating difference'+str(i))
    with open(path+'diff.html','w') as f :
        f.write(difference0)
for f in os.listdir(path):
    if re.search('file_tmp_[sf]f_(\d*).txt',f):
        os.remove(os.path.join(path,f))
