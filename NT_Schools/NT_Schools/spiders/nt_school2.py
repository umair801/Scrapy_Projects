import scrapy
import json


class NtSchoolSpider(scrapy.Spider):
    name = "nt_school"
    headers = {
        'Accept': 'application/json',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Host': 'directory.ntschools.net',
        'Pragma': 'no-cache',
        'Referer': 'https://directory.ntschools.net/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 OPR/104.0.0.0',
        'X-Requested-With': 'Fetch',
        'sec-ch-ua': '"Chromium";v="118", "Opera";v="104", "Not=A?Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': "Windows"
    }

    def start_requests(self):
        start_url = 'https://directory.ntschools.net/api/System/GetAllSchools'
        yield scrapy.Request(
            url=start_url,
            callback=self.parse_codes,
            headers=self.headers,
        )

    def parse_codes(self, response):
        resp_list = json.loads(response.body)
        for row in resp_list:
            school_code = row['itSchoolCode']
            yield scrapy.Request(
                url=f'https://directory.ntschools.net/api/System/GetSchool?itSchoolCode={school_code}',
                callback=self.parse_data,
                headers=self.headers,
            )

    def parse_data(self, response):
        global management_name, management_position, management_email, management_phone
        resp2 = json.loads(response.body)
        school_name = resp2['name']
        primary_school = resp2['primarySchool']
        physical_address = resp2['physicalAddress']['displayAddress']  # physicalAddress > {}
        postal_address = resp2['postalAddress']['displayAddress']
        phone = resp2['telephoneNumber']
        email = resp2['mail']
        website = resp2['uri']
        school_management = resp2['schoolManagement']
        for item in school_management:  # school_management > []
            f_name = item['firstName']
            l_name = item['lastName']
            management_name = f'{f_name} {l_name}'
            management_position = item['position']
            management_email = item['email']
            management_phone = item['phone']

        yield {
            'School Name': school_name,
            'Primary School': primary_school,
            'Physical Address': physical_address,
            'Postal Address': postal_address,
            'Email': email,
            'Phone': phone,
            'Website': website,
            'Management Name': management_name,
            'Management Position': management_position,
            'Management Email': management_email,
            'Management Phone': management_phone,
        }
