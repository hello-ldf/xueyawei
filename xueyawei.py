# encoding:utf-8

import time, datetime, os, re, requests, io
import pprint, logging, sys
from selenium import webdriver
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')
logging.basicConfig(level=logging.INFO, format=' %(asctime)s - %(levelname)s - %(message)s')
logging.disable(logging.DEBUG)


# 这两个自己配置！！！！！！！！！！！！！！
username = ''
password = ''
# 这两个自己配置！！！！！！！！！！！！！！






homeURL = 'http://www.xueyawei.com/'
# 登录页面
loginURL = 'http://www.xueyawei.com/wp-login.php'
# 乐谱链接
musicScoreURL = 'http://www.xueyawei.com/?p=797'
# test = 'http://www.xueyawei.com/'
pathRegex = re.compile(r'/')

# 工具
def mkdir(path):
	exists = os.path.exists(path)
	if not exists:
		os.makedirs(path)

# 生成根目录【学押尾】 及目录文件
rootPath = u'【学押尾】'
mkdir(rootPath)

timeStruct = time.localtime(time.time()) 
now = time.strftime("%Y%m%d_%H%M%S", timeStruct)
newPath = os.path.join(rootPath, now+'.txt')
indexath = os.path.join(rootPath, 'index.txt')
# indexFile = open(imgPath, 'wb')
# indexFile.write(chunk)
# indexFile.close()


# 打开浏览器 跳到登录页面并登陆
browser = webdriver.Chrome()
browser.get(loginURL)

user_login = browser.find_element_by_id('user_login')
user_pass = browser.find_element_by_id('user_pass')
rememberme = browser.find_element_by_id('rememberme')
wp_submit = browser.find_element_by_id('wp-submit')

user_login.send_keys(username)
user_pass.send_keys(password)
rememberme.send_keys('forever')
wp_submit.click()

# 转到首页 获取专辑列表
browser.get(homeURL)
epEls = browser.find_elements_by_css_selector('#menu-item-38 .sub-menu a')
# 临时保存专辑列表
eps = []
for epEl in epEls:
	epName = pathRegex.sub('',epEl.get_attribute('innerHTML')) # 专辑名
	epURL = epEl.get_attribute('href')
	eps.append({'name': epName, 'url': epURL})
# 保存每张专辑
for ep in eps:
	epPath = os.path.join(rootPath, ep['name'])
	mkdir(epPath)

	browser.get(ep['url'])
	songELs = browser.find_elements_by_css_selector('.entry-title a')
	# 临时保存曲目列表
	songs = []
	for songEL in songELs:
		songName = pathRegex.sub('',songEL.get_attribute('innerHTML')) # 专辑名
		songURL = songEL.get_attribute('href')
		songs.append({'name': songName, 'url': songURL})
	# 保存每首歌
	for song in songs:
		songPath = os.path.join(epPath, song['name'])
		mkdir(songPath)

		browser.get(song['url'])

		# 先评论
		while True:
			easy2hide_notice = browser.find_element_by_css_selector('.easy2hide_notice')
			if easy2hide_notice:
				time.sleep(10)
				now_time = datetime.datetime.now()
				now_time_str = datetime.datetime.strftime(now_time,'%Y%m%d_%H%M%S')
				comment = browser.find_element_by_css_selector('#comment')
				comment.send_keys(now_time_str)
				comment.submit()
			else:
				break

		indexFile = io.open(indexPath, 'a', encoding='utf-8')
		indexFile.write('\n')
		indexFile.close()

		imgELs = browser.find_elements_by_css_selector('.wp-caption.aligncenter a')
		# 遍历图
		for imgEL in imgELs:
			# imgName = imgEL.get_attribute('title') # 图片名
			imgURL = imgEL.get_attribute('href')
			imgPath = os.path.join(songPath, os.path.basename(imgURL))

			indexFile = io.open(indexPath, 'a', encoding='utf-8')
			indexFile.write(imgPath+'\n')
			indexFile.close()

			# check file
			if os.path.exists(imgPath):
				continue

			# Download the image.
			logging.info('Downloading image %s...' % (imgURL))
			res = requests.get(imgURL)

			# Save the image
			logging.info('Save the image.path:%s' % (imgPath))
			imageFile = open(imgPath, 'wb')
			for chunk in res.iter_content(100000):
				imageFile.write(chunk)
			imageFile.close()

			# 更新内容
			indexFile = io.open(newPath, 'a', encoding='utf-8')
			indexFile.write(imgPath+'\n')
			indexFile.close()











# 跳到曲谱页面 评论 获取图片
# browser.get(musicScoreURL)

# easy2hide_notice = GetElementBySelector(browser, '.easy2hide_notice')
# if easy2hide_notice:
# 	time.sleep(10)
# 	now_time = datetime.datetime.now()
# 	now_time_str = datetime.datetime.strftime(now_time,'%Y%m%d_%H%M%S')
# 	comment = GetElementBySelector(browser, '#comment')
# 	comment.send_keys(now_time_str)
# 	comment.submit()

# easy2hide_notice = GetElementBySelector(browser, '.easy2hide_notice')
# if easy2hide_notice:
# 	print('还没好 o')