# This Python file uses the following encoding: utf-8
import re
import argparse
import sys

parser = argparse.ArgumentParser(description='Convert html of RB data to csv')
parser.add_argument('filename', metavar='workfile', type=str, nargs=1,
                  help='name of html file (including .html)')
args = parser.parse_args()

workfile=args.filename[0]
try:
   with open(workfile): pass
except IOError:
   print('Error! File '+workfile+' not found.')
   sys.exit()
   
f = open(workfile,'r')
end = 0
line_no = 0
while(end!=1):
    line = f.readline()
    if(line==""):
        end=1
    #if(re.search('P.Č.',line)):
    #skip beginning of file up to here
    if(re.search('P\.',line)):
        end=1
        print('1 ****');
        print(line);
end=0
lines=[]
while(end!=1):
    if(line==""):
        end=1
    #if(re.search('Poplatky za produkty a služby poskytované v rámci cenového programu eKonto',line)):
    #skip rest of the file after poplatky
    if(re.search('Poplatky za produkty a',line)):
        end=1
        print('2 ****');
        print(line);
        continue
    
    
    
    line=re.sub(r'&nbsp;','',line)
    line=re.sub(r'<tr>','\n',line)
    line=re.sub(r'<[td|TD|br].*?>','|',line)
    line=re.sub(r'<table.*?>','\nTABLE\n',line,flags=re.IGNORECASE)
    line=re.sub(r"<.*?>",'',line,flags=re.IGNORECASE)
    line=line.split('|')
    baf=15
    if(len(line)>baf):
        if line[5]=="Datum":
            line=line[2:]
        line[6]='"'+line[6]+'"'
        line[7]='"'+line[7]+'"'
        line[15]=re.sub(r"\.",',',line[15])
        line[16]=re.sub(r"\.",',',line[16])
    line_no+=1
    line=line[2:]
    print(line)
    line=str.join(";",line)
    lines.append(line)
    line = f.readline()
    
print('end of file')
f=open(workfile+".output.csv",'w')
for line in lines:
    f.write(line)
f.close()

print('\nSuccess! Ouptut written to '+workfile+'.output.csv');
