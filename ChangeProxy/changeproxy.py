#scrapy������
#����IP�����������Ż����˶ι��ܷ���middlewares.py�У�����settings.py�п���DOWNLOADER_MIDDLEWARES���������ƻ�Ϊ�����ơ�
#11��20�ţ�learning 1.
import requests
import json
class ChangeProxy(object):         					# �������У�__init__  ��  process_request

	def __init__(self):								#��ʼ��
		self.ip_url = "http://ip.jiangxianli.com/api/proxy_ips"			   	#���ʴ���IP��ȡ��ַ���˴���õ���json��ʽ��m������IP
		self.temp_url = "http://ip.chinaz.com/"    #������ַ��IP��ѯ,������֤IP�Ƿ���Ч
		self.ip_list = []
		self.count = 0								#����ʹ��IP�ĸ������ڼ���ip��
		self.evecount = 0							#ÿ��IP�ķ��ʴ���

	def getIPData(self):                      		#�Ӵ���IP������Ǹ�����IP�������slef.ip_list,�ٴ���self.ip_list��IP��port�С�
		temp_data = requests.get(url=self.ip_url).text
		self.ip_list.clear()		#���IP�洢��
		for eve_ip in json.loads(temp_data)["data"]["data"]:	    #json.loads(temp_data)["result"]:����json�ļ�����ȡresult��������ݡ�
			self.ip_list.append({
				"ip":eve_ip["ip"],					#��ȡip��port ����ֵ��
				"port":eve_ip["port"] 
				})

	def changeProxy(self,request):      			#scrapy�޸Ĵ���IP
		request.meta["proxy"] = "http://" + str(self.ip_list[self.count - 1]["ip"]) + ":" + str(self.ip_list[self.count-  1]["port"])
	
	def yanzheng(self):								#��֤����IP�Ƿ���ã�Ĭ�ϳ�ʱ5s
		requests.get(url = self.temp_url,proxies = {"http":"http://"+str(self.ip_list[self.count-1]["ip"]) + ":" + str(self.ip_list[self.count-1]["port"])},timeout = 5)	

	def ifUsed(self,request):						#�л�����IP�����壬��������m��IP��������ÿһ��IP��ѭ��������ʼ�ĵط�

		try:
			self.changeProxy(request)
			self.yanzheng()
		except:
			if self.count == m:
				self.getIPData()
				self.count = 1
			self.count = self.count + 1
			self.ifUsed(request)

	def process_request(self,request,spider):    	#��Ҫִ�г��򣬴���IPʹ�ù��򣬴���ع���m��IP��һ������IPʹ���������n��,n��m����ֵ
		
		if self.count == 0 or self.count == m:     	#����ʼ������IP�������һ������
			self.getIPData()		               	#��ȡIP
			self.count = 1			               	#����=1�����¿�ʼ��

		if self.evecount == n: 
			self.count = self.count + 1
			self.evecount= 0
		else:
			self.evecount = self.evecount + 1

		self.ifUsed(request)			

