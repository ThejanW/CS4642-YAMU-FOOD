#!/bin/bash
scrapy crawl places -o places.json &&
scrapy crawl cuisines -o cuisines.json