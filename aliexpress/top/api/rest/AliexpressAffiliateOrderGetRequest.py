'''
Created by auto_sdk on 2020.09.09
'''
from aliexpress.top.api.base import RestApi
class AliexpressAffiliateOrderGetRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.app_signature = None
		self.fields = None
		self.order_ids = None

	def getapiname(self):
		return 'aliexpress.affiliate.order.get'
