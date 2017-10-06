#!/usr/bin/python3
# -*- coding: utf-8 -*-

#important: index file cannot contain new line character

import urllib2;
import urllib;
import re;
import os;

url = 'http://manhua.fzdm.com/142/'
dir = '/Users/yandong/Documents/manga/konan/'
download = 0



# make new dir
def mkdir(path):
    isExists=os.path.exists(path)

    if not isExists:
        os.makedirs(path) 
 
        print ('success')
        return True
    #if not exist
    else:
        print ('already exist')
        return False


#update the new charpter
def update(charpter):
	fileObject = open(dir + 'index.txt', 'w')
	fileObject.write(charpter)
	fileObject.close()



def main():
	global download
	print 'name: konan' 
	#open the target page
	html = urllib2.urlopen(url).read();

	#find the pattern
	result = re.compile(r'<li class=(.+?)><a href=\"(.+?)\/\" title=(.+?)', re.DOTALL);

	#open the recent update charpter
	fileObject = open(dir + 'index.txt')
	index = fileObject.read()
	fileObject.close()

	print 'current read charpter ' + index

	#find out the charpter is not download yet
	for x in result.findall(html):
		#if the charpter already update
		if x[1] == index:
			break
		print 'start download charpter: ' + x[1]

		#make the new dir
		mkdir(dir + x[1])

		#else open the charpter
		page = 0
		charpterUrl = url + x[1] + '/'
		#print charpterUrl
		charpterHtml = urllib2.urlopen(charpterUrl).read()
		#print 'size is', len(charpterHtml);

		#if it is not the final page
		charpterResult = re.compile(r'<a href=\'index_(.+?)\' id=(.+?)>下一页')
		next = re.search(charpterResult, charpterHtml)
		#print 'next  = ' + next.group(1)
		while next:
			nextIndex = next.group(1)
			#print 'nextIndex = ' + nextIndex
			mhurl = re.compile(r'var mhurl = \"(.+?)\";')
			mhurlResult = re.search(mhurl, charpterHtml)
			imgsrc = re.compile(r'img\.src=\"(.+?)\"(.+?)')
			imgsrcResult = re.search(imgsrc, charpterHtml)
			imgurl = imgsrcResult.group(1) + mhurlResult.group(1)
			#print imgurl

			#check the url is correct or not 
			try:
				urllib2.urlopen(imgurl, timeout = 5)
				urllib.urlretrieve(imgurl, dir + x[1] + '/%s.jpg' % page)
				print 'download the page ' + str(page)
			except:
				print 'page ' + str(page) + ' cant be downloaded because of the wrong url'
		
			page = page + 1

			#read the next page
			charpterUrl = url + x[1] + '/index_' + str(page) + '.html'
			#print 'charpterUrl = ' + charpterUrl
			charpterHtml = urllib2.urlopen(charpterUrl).read()
			charpterResult = re.compile(r'<a href=\'index_(.+?)\' id=(.+?)>下一页')
			next = re.search(charpterResult, charpterHtml)

		print 'download the charpter ' + x[1] + ' success'
		if download == 0:
			update(x[1])
		download = download + 1

	print 'success download ' + str(download) + ' charpters'

main()



