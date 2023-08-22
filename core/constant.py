import os
from core.scraper import Scraper

SLACK_TOKEN = os.getenv('SLACK_TOKEN')
CSE_URL_BASE = 'https://computer.cnu.ac.kr/computer/notice/'
CNU_URL_BASE = 'https://plus.cnu.ac.kr/_prog/_board'

BOARD_INFO_LIST = {
    'cse_bachelor':{
        'name' : '컴융-학사공지',
        'channel_id' : os.getenv('CHANNEL_BACHELOR'),
        'url' : CSE_URL_BASE + 'bachelor.do',
        'scraper': Scraper.crawl_cse,
    },
    'cse_notice':{
        'name' : '컴융-일반소식',
        'channel_id' : os.getenv('CHANNEL_NOTICE'),
        'url' : CSE_URL_BASE + 'notice.do',
        'scraper': Scraper.crawl_cse,
    },
    'cse_project':{
        'name' : '컴융-사업단소식',
        'channel_id' : os.getenv('CHANNEL_PROJECT'),
        'url' : CSE_URL_BASE + 'project.do',
        'scraper': Scraper.crawl_cse,
    },
    'cnu_notice': {
        'name' : '충남대-학사정보',
        'channel_id' : os.getenv('CHANNEL_CNU'),
        'url_base' : CNU_URL_BASE,
        'url' : CNU_URL_BASE + '/?code=sub07_0702&site_dvs_cd=kr&menu_dvs_cd=0702',
        'scraper': Scraper.crawl_cnu,
    }
}