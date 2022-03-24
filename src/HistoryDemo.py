import sqlite3
from tkinter.messagebox import YES
import xlwt

con = sqlite3.connect('History') 
cur = con.cursor()  

cur.execute('SELECT * FROM urls')
con.text_factory = str   

header = ['id', 'url', 'title', 'visit_count',
          'typed_count', 'last_visit_time', 'hidden']
wbk = xlwt.Workbook()
sheet = wbk.add_sheet('Sheet1', cell_overwrite_ok=True)

for index, hkey in enumerate(header):
        sheet.write(0, index, hkey)

t = cur.fetchone()
row=1
while t is not None:
    t_s={}
    for i, d in enumerate(t):
        t_s[header[i]]=d
        sheet.write(row, i, d)
        if i==2:
            if('d3'in d or 'd3.js' in d or 'transition' in d ):
                sheet.write(row, i, d)
        elif(i>2):
            if('d3'in t_s['title'] or 'd3.js' in t_s['title'] or 'transition' in t_s['title'] ):
                sheet.write(row, i, d)
                if(i==6):
                    row=row+1

    t = cur.fetchone()
wbk.save('history_d3.xls')



cur.close()
con.close()
