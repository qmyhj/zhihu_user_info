# -*- coding: utf-8 -*-
import scrapy
import json
from ..items import ZhihuItem

class UserinfoSpider(scrapy.Spider):
    name = 'userinfo'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['http://www.zhihu.com/']

    user_url = 'https://www.zhihu.com/api/v4/members/{user}?include=locations,employments,gender,educations,business,voteup_count,thanked_Count,follower_count,following_count,cover_url,following_topic_count,following_question_count,following_favlists_count,following_columns_count,avatar_hue,answer_count,articles_count,pins_count,question_count,columns_count,commercial_question_count,favorite_count,favorited_count,logs_count,included_answers_count,included_articles_count,included_text,message_thread_token,account_status,is_active,is_bind_phone,is_force_renamed,is_bind_sina,is_privacy_protected,sina_weibo_url,sina_weibo_name,show_sina_weibo,is_blocking,is_blocked,is_following,is_followed,is_org_createpin_white_user,mutual_followees_count,vote_to_count,vote_from_count,thank_to_count,thank_from_count,thanked_count,description,hosted_live_count,participated_live_count,allow_message,industry_category,org_name,org_homepage,badge[?(type=best_answerer)].topics'
    follower_url = 'https://www.zhihu.com/api/v4/members/excited-vczh/followers?include=data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&offset=20&limit=20'
    followee_url = 'https://www.zhihu.com/api/v4/members/excited-vczh/followees?include=data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&offset=20&limit=20'
    def start_requests(self):
        start_user = 'excited-vczh'
        yield scrapy.Request(self.user_url.format(user=start_user), callback=self.parse_user)
        yield scrapy.Request(self.follower_url, callback=self.parse_followers)
        yield scrapy.Request(self.followee_url, callback=self.parse_followees)

    def parse_user(self, response):
        html = json.loads(response.text)
        item = ZhihuItem()
        for field in item.fields:
            item[field] = html.get(field)
        yield item
        yield scrapy.Request(self.user_url.format(user=item['url_token']), callback=self.parse_followers)
        yield scrapy.Request(self.user_url.format(user=item['url_token']), callback=self.parse_followees)

    def parse_followers(self, response):
        html = json.loads(response.text)
        if 'data' in html.keys():
            for item in html.get('data'):
                url_token = item.get('url_token')
                yield scrapy.Request(self.user_url.format(user=url_token), callback=self.parse_user)

        if 'paging' in html.keys() and html.get('paging').get('is_end') == False:
            next = html.get('paging').get('next')
            yield scrapy.Request(next, callback=self.parse_followers)

    def parse_followees(self, response):
        html = json.loads(response.text)
        if 'data' in html.keys():
            for item in html.get('data'):
                url_token = item.get('url_token')
                yield scrapy.Request(self.user_url.format(user=url_token), callback=self.parse_user)

        if 'paging' in html.keys() and html.get('paging').get('is_end') == False:
            next = html.get('paging').get('next')
            yield scrapy.Request(next, callback=self.parse_followees)




