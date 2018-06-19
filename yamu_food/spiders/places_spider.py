import scrapy


class RestaurantsSpider(scrapy.Spider):
    name = "places"
    urls = None

    def start_requests(self):
        with open('places_urls.txt') as f:
            urls = f.readlines()
        urls = [x.strip() for x in urls]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # places listings
        page_url = response.request.url

        if "page" in page_url:
            links = response.xpath('//ul[@class="media-list search-results"]/div[@class="row"]/a/@href').extract()

            for link in links:
                yield scrapy.Request(link, callback=self.parse)
        else:
            # place page
            restaurant = response.xpath('//div[@class="place-title-box"]/h2/text()').extract_first()
            contact = response.xpath('//ul[@class="place-title-list list-inline"]/li/a/text()').extract_first()
            address = response.xpath('//div[@class="place-title-box"]/p/text()').extract_first()
            intro = response.xpath('//div[@class="place-title-box"]/p[@class="excerpt"]/text()').extract_first()
            reviewer = response.xpath(
                '//div[@class="author-byline"]/div[@class="media"]/div/div/a/span/text()').extract_first()
            cuisine = response.xpath('//p[text()="Cuisine"]/following::p[1]/a/text()').extract()
            price = response.xpath('//p[text()="Price Range"]/following::p[1]/a/text()').extract()
            food = response.xpath('//p[text()="Dish Types"]/following::p[1]/a/text()').extract()
            overall_rating = response.xpath(
                '//dt/a[text()="Overall Rating"]/following::dd[1]/span/text()').extract_first()
            quality_rating = response.xpath(
                '//dt/a[text()="Quality Rating"]/following::dd[1]/span/text()').extract_first()
            service_rating = response.xpath(
                '//dt/a[text()="Service Rating"]/following::dd[1]/span/text()').extract_first()
            ambience_rating = response.xpath(
                '//dt/a[text()="Ambience Rating"]/following::dd[1]/span/text()').extract_first()

            yield {
                'page_url': page_url,
                'restaurant': restaurant,
                'contact': contact,
                'address': address,
                'intro': intro,
                'reviewer': reviewer,
                'cuisine': cuisine,
                'price': price,
                'food': food,
                'overall_rating': overall_rating,
                'quality_rating': quality_rating,
                'service_rating': service_rating,
                'ambience_rating': ambience_rating
            }
