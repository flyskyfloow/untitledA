#!/usr/bin/env python
# -*- coding: utf-8 -*-
import scrapy

from ..items import GftsearchItem


class CftSpiderSsrn(scrapy.Spider):
    name = "ssrn"

    @staticmethod
    def extract_cookies(cookie):
        """从浏览器或者request headers中拿到cookie字符串，提取为字典格式的cookies"""
        cookies = dict([l.split("=", 1) for l in cookie.split("; ")])
        return cookies

    def start_requests(self):
        cookie = "__cfduid=d79dae932c5af4449eddf61d7d5e83c4c1510122393; optimizelyEndUserId=oeu1510122400585r0.6585689269566823; AMCVS_4D6368F454EC41940A4C98A6%40AdobeOrg=1; _pk_ref.7.2f73=%5B%22%22%2C%22%22%2C1510640013%2C%22https%3A%2F%2Fpapers.ssrn.com%2Fsol3%2FDisplayAbstractSearch.cfm%22%5D; AMCV_4D6368F454EC41940A4C98A6%40AdobeOrg=-1330315163%7CMCIDTS%7C17484%7CMCMID%7C24508037444471328661816005296240478782%7CMCAAMLH-1510727209%7C11%7CMCAAMB-1511244814%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1510647214s%7CNONE%7CMCAID%7CNONE; _ceg.s=ozeaii; _ceg.u=ozeaii; SITEID=en; CFCLIENT_SSRN=loginexpire%3D%7Bts%20%272017%2D11%2D14%2003%3A10%3A46%27%7D%23strgotourl%3D1%23blnlogedin%3DFalse%23; SSRN_LOGIN=154067121113103010006009069091082030022028105007049015094070071120008002096009067119; SSRN_PW=552119115003088021011109125016090005079007083115025106083097; CFID=Zy3rymi4mfx7eqn0ushsc14ki96nyf982a2rr2mow485b4v5rg-28377809; CFTOKEN=Zy3rymi4mfx7eqn0ushsc14ki96nyf982a2rr2mow485b4v5rg-81380848; CFGLOBALS=urltoken%3DCFID%23%3D28377809%26CFTOKEN%23%3D81380848%23lastvisit%3D%7Bts%20%272017%2D11%2D14%2003%3A10%3A57%27%7D%23hitcount%3D194%23timecreated%3D%7Bts%20%272017%2D11%2D08%2001%3A26%3A33%27%7D%23cftoken%3D74470335%23cfid%3D99323858%23; BNI_ssrn-lba=0000000000000000000000007604020a00005000; _pk_id.7.2f73=030c1946a00d4bfd.1510122791.8.1510647059.1510640013.; _pk_ses.7.2f73=*; optimizelySegments=%7B%226362251111%22%3A%22none%22%2C%226374050723%22%3A%22false%22%2C%226353661739%22%3A%22gc%22%2C%226339813413%22%3A%22referral%22%7D; optimizelyBuckets=%7B%7D; optimizelyPendingLogEvents=%5B%5D; s_pers=%20v8%3D1510647059112%7C1605255059112%3B%20v8_s%3DLess%2520than%25201%2520day%7C1510648859112%3B%20c19%3Dss%253Ahomepage%253Auser%7C1510648859116%3B%20v68%3D1510647057588%7C1510648859122%3B; s_sq=%5B%5BB%5D%5D; s_cc=true; _ceg.s=ozeeqb; _ceg.u=ozeeqb; s_sess=%20v31%3D1510308565888%3B%20s_cpc%3D0%3B%20e41%3D1%3B%20s_ppvl%3Dss%25253Arankings%25253Apapers%252C13%252C13%252C2182.3333740234375%252C1280%252C649%252C1920%252C1080%252C1.5%252CP%3B%20s_ppv%3Dss%25253Ahomepage%25253Auser%252C48%252C48%252C649%252C1280%252C649%252C1920%252C1080%252C1.5%252CP%3B"
        cookies = self.extract_cookies(cookie)
        return [scrapy.Request(url='https://hq.ssrn.com/rankings/Ranking_display.cfm?npage=1&RequestTimeout=5000&TMY_gID=2&TRN_gID=10&runid=70238', cookies=cookies)]

    # def parse(self, response):
    #     page = response.url.split("/")[-2]
    #     filename = 'quotes-%s.html' % page
    #     with open(filename, 'wb') as f:
    #         f.write(response.body)
    #     self.log('Saved file %s' % filename)

    def parse(self, response):
        item = GftsearchItem()
        for i in response.xpath('//*[@id="maincontent"]/div[6]/table/tbody/tr'):
            item['gid'] = i.xpath('./@id').extract_first()
            item['links'] = i.xpath('./td/a[@class="paper-title"]/@href').extract_first()
            item['title'] = i.xpath('./td/a/text()').extract_first()
            item['author'] = i.xpath('./td/span/a/text()').extract_first()
            item['downloads'] = i.xpath('./td[@class="shown-2 selected"]/a/text()').extract_first().strip()
            yield item


# #   递归爬虫到下一页
#         next_page = response.css('li.next a::attr(href)').extract_first()
#         if next_page is not None:
#             next_page = response.urljoin(next_page)
#             yield scrapy.Request(next_page, callback=self.parse)

        urlstart = "https://hq.ssrn.com/rankings/Ranking_display.cfm?npage="
        urlend = "&RequestTimeout=5000&TMY_gID=2&TRN_gID=10&runid=70198"

        for nextpage in range(1, 100):
            nexturl = urlstart + str(nextpage) + urlend
            yield scrapy.Request(nexturl, callback=self.parse)

