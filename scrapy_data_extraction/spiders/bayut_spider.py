import scrapy

from scrapy_data_extraction.items import BayutPropertyItem

class BayutSpider(scrapy.Spider):
    name = 'bayut_spider'
    allowed_domains = ['bayut.com']
    start_urls = ['https://www.bayut.com/to-rent/property/dubai/']

    def parse(self, response):
        # Your parsing logic here
        property_urls = response.xpath('//div[@class="title"]/a/@href').extract()
        for property_url in property_urls:
            yield scrapy.Request(url=property_url, callback=self.parse_property)

        # Pagination
        next_page = response.xpath('//li[@class="pagination__item pagination__item--next"]/a/@href').extract_first()
        if next_page:
            yield scrapy.Request(url=next_page, callback=self.parse)

    def parse_property(self, response):
        # Your property parsing logic here
        item = BayutPropertyItem()
        item['property_id'] = response.xpath('//div[@class="property-id"]/text()').extract_first().strip()
        item['purpose'] = response.xpath('//span[contains(text(), "Purpose")]/following-sibling::span/text()').extract_first().strip()
        item['type'] = response.xpath('//span[contains(text(), "Type")]/following-sibling::span/text()').extract_first().strip()
        item['added_on'] = response.xpath('//span[contains(text(), "Added on")]/following-sibling::span/text()').extract_first().strip()
        item['furnishing'] = response.xpath('//span[contains(text(), "Furnishing")]/following-sibling::span/text()').extract_first().strip()
        item['price'] = {
            'currency': response.xpath('//span[contains(text(), "Currency")]/following-sibling::span/text()').extract_first().strip(),
            'amount': response.xpath('//span[contains(text(), "Amount")]/following-sibling::span/text()').extract_first().strip()
        }
        item['location'] = response.xpath('//span[contains(text(), "Location")]/following-sibling::span/text()').extract_first().strip()
        item['bed_bath_size'] = {
            'bedrooms': int(response.xpath('//span[contains(text(), "Bedrooms")]/following-sibling::span/text()').extract_first().strip()),
            'bathrooms': int(response.xpath('//span[contains(text(), "Bathrooms")]/following-sibling::span/text()').extract_first().strip()),
            'size': response.xpath('//span[contains(text(), "Size")]/following-sibling::span/text()').extract_first().strip()
        }
        item['permit_number'] = response.xpath('//span[contains(text(), "Permit Number")]/following-sibling::span/text()').extract_first().strip()
        item['agent_name'] = response.xpath('//span[contains(text(), "Agent Name")]/following-sibling::span/text()').extract_first().strip()
        item['image_url'] = response.xpath('//div[@class="media-wrapper"]/img/@src').extract_first().strip()
        item['breadcrumbs'] = response.xpath('//div[@class="breadcrumbs"]/a/text()').extract()
        item['amenities'] = response.xpath('//span[contains(text(), "Amenities")]/following-sibling::div/span/text()').extract()

        yield item