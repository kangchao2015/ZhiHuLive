def func_year(s):
 print 'func_year:', s
  
def func_month(s):
 print 'func_month:', s 
 
strs = ['year', 'month']
for s in strs:
 globals().get('func_%s' % s)(s)
