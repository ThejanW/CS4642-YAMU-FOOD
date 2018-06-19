import scrapy


class RestaurantsSpider(scrapy.Spider):
    name = "cuisines"

    def start_requests(self):
        with open('cuisines_urls.txt') as f:
            urls = f.readlines()
        urls = [x.strip() for x in urls]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # cuisines page
        page_url = response.request.url
        cuisine_list = response.xpath('//div[@class="label-header"]/div[@class="pull-left"]//a/text()').extract()
        cuisine = cuisine_list[-1]

        parent_cuisine = ""
        if len(cuisine_list) == 3:
            parent_cuisine = cuisine_list[1]

        children_cuisines = response.xpath(
            '//div[@class="label-header"]/div[@class="label-filters pull-right hidden-xs"]//p/text()').extract()
        # remove word "More" from children
        try:
            children_cuisines.remove('More')
        except ValueError:
            pass

        yield {
            'page_url': page_url,
            'cuisine': cuisine,
            'parent_cuisine': parent_cuisine,
            'children_cuisines': children_cuisines
        }
