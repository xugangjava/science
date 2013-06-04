#coding=utf-8
import re

if __name__=='__main__':
	word_string=''
	with open(u'项目申请书.xml') as f:
		while 1:
			buf=f.read(65536)
			if not buf:break
			word_string+=buf
	count=word_string.count('field')
	print count

#	i=0
#	while i<count:
#		word_string=word_string.replace('field','fid'+str(i),1)
#		i+=1
	print word_string.split('field')
