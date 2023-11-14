import scrapy
import json


class NtSchoolsSpider(scrapy.Spider):
    name = "nt_schools"
    start_urls = ['https://directory.ntschools.net/#/schools']
    headers = {
        'Accept': 'application/json',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Cookie': 'ab.storage.deviceId.a9882122-ac6c-486a-bc3b-fab39ef624c5=%7B%22g%22%3A%22db089d13-abcf-c574-7869-9611321e89c3%22%2C%22c%22%3A1685045349101%2C%22l%22%3A1685045349101%7D',
        'Host': 'directory.ntschools.net',
        'Pragma': 'no-cache',
        'Referer': 'https://directory.ntschools.net/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
        'X-Requested-With': 'Fetch',
        'sec-ch-ua': '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': "Windows",
    }

    def start_requests(self):
        url = 'https://directory.ntschools.net/api/System/GetAllSchools'
        yield scrapy.Request(url=url, callback=self.parse_urls, headers=self.headers)

    def parse_urls(self, response):
        base_url = 'https://directory.ntschools.net/api/System/GetSchool?itSchoolCode='
        raw_data = response.body
        schools_data = json.loads(raw_data)
        for school in schools_data:
            school_code = school['itSchoolCode']
            school_url = base_url + school_code
            yield scrapy.Request(url=school_url, callback=self.parse_data, headers=self.headers)

    def parse_data(self, response):
        raw_data = response.body
        data = json.loads(raw_data)
        yield {
            'Name': data['name'],
            'Physical_Address': data['physicalAddress']['displayAddress'],
            'Postal_Address': data['postalAddress']['displayAddress'],
            'Telephone_Number': data['telephoneNumber'],
            'Email': data['mail'],
        }
