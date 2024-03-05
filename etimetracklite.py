# Copyright (c) 2024, Wahni IT Solutions Pvt. Ltd. and contributors
# For license information, please see license.txt

import requests
from xml.etree import ElementTree as ET


class eTimeTrackLite():
	def __init__(self, domain):
		self.url = "http://{0}/iclock/WebAPIService.asmx".format(domain)
		self.headers = {
			'Content-Type': 'text/xml',
			'SOAPAction': "http://tempuri.org/GetTransactionsLog",
			'charset': 'utf-8'
		}
	
	def set_request_body(self, args):
		self.body = """<?xml version="1.0" encoding="utf-8"?>
			<soap:Envelope
				xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
				xmlns:xsd="http://www.w3.org/2001/XMLSchema"
				xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
			>
				<soap:Body>
					<GetTransactionsLog xmlns="http://tempuri.org/">
						<FromDateTime>{0}</FromDateTime>
						<ToDateTime>{1}</ToDateTime>
						<SerialNumber>{2}</SerialNumber>
						<UserName>{3}</UserName>
						<UserPassword>{4}</UserPassword>
						<strDataList></strDataList>
					</GetTransactionsLog>
				</soap:Body>
			</soap:Envelope>
		""".format(
			args.get("from_time"),
			args.get("to_time"),
			args.get("serial_no"),
			args.get("username"),
			args.get("password"),
		)
	
	def fetch_logs(self):
		self.logs = []
		response = requests.post(self.url, data=self.body, headers=self.headers)

		if response.status_code != 200:
			return

		root = ET.fromstring(response.content)
		str_data_list_element = root.find(".//{http://tempuri.org/}strDataList")

		if str_data_list_element is None:
			return

		str_data_list_content = str_data_list_element.text.split("\n")
		for log in str_data_list_content:
			self.logs.append(log.split('\t'))
