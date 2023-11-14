import scrapy
from scrapy_selenium import SeleniumRequest


class PluginthemeSpider(scrapy.Spider):
    name = "pluginTheme"

    def start_requests(self):
        start_urls = ["https://plugintheme.net/shop/"]
        yield SeleniumRequest(url=start_urls[0], callback=self.parse_urls)

    def parse_urls(self, response):
        rows = response.xpath('//div[contains(@class,"products row")]/div')
        for row in rows:
            url = row.xpath('.//div[@class="box-image"]//a/@href').get()
            yield SeleniumRequest(url=url, callback=self.parse_data)

        # Pagination
        next_page = response.xpath('//a[@class="next page-number"]/@href').get()
        yield SeleniumRequest(url=next_page, callback=self.parse_urls)

    def parse_data(self, response):
        global price, mrp, rsp, sh_description_html, description_html
        title = response.xpath('//h1[@class="product-title product_title entry-title"]/text()').get()
        if title: title = title.strip()

        mrp_pr = response.xpath('//del//bdi/text()').get()
        if mrp_pr:
            mrp_pr = mrp_pr.strip()
            mrp = f'${mrp_pr}'

        rsp_pr = response.xpath('//ins//bdi/text()').get()
        if rsp_pr:
            rsp_pr = rsp_pr.strip()
            rsp = f'${rsp_pr}'

        prod_version = response.xpath('//strong[text()="Product Version :"]/following::node()[1]').get()
        if prod_version: prod_version = prod_version.strip()

        prod_last_updt = response.xpath('//strong[text()="Product Last Updated :"]/following::node()[1]').get()
        if prod_last_updt: prod_last_updt = prod_last_updt.strip()

        license = response.xpath('//strong[text()="License :"]/following::a[1]/text()').get()
        if license: license = license.strip()

        sku = response.xpath('//span[@class="sku"]/text()').get()
        if sku: sku = sku.strip()

        category = response.xpath('//span[@class="posted_in"]/a/text()').getall()

        tag = response.xpath('//span[@class="tagged_as"]/a/text()').getall()

        img_url = response.xpath('//img[@class="wp-post-image skip-lazy"]/@src').get()

        sh_description = response.xpath('//div[@class="product-short-description"]/ul').get()
        if sh_description:
            sh_description_html = f'<html>{sh_description}</html>'

        description = response.xpath('//div[@id="tab-description"]').get()
        if description:
            description_html = f'<html>{description}</html>'

        demo_link = response.xpath('//a[text()="DEMO LINK"]/@href').get()

        yield {
            'Title': title,
            'Product Image': img_url,
            'MRP': mrp,
            'RSP': rsp,
            'Short Description': sh_description_html,
            'Demo Link': demo_link,
            # 'Download Link': download_link,
            'SKU': sku,
            'Category': category,
            'Tag': tag,
            'Description': description_html,
            'URL': response.url,

            # 'PLU': prod_last_updt,
            # 'License': license,
            # 'Product Version': prod_version,

        }