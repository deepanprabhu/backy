from multiprocessing.pool import ThreadPool;
import requests;
from lxml import etree;
from datetime import datetime,timedelta;
import threading;
import os;
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import time;


def requests_retry_session(
    retries=3,
    backoff_factor=0.3,
    status_forcelist=(500, 502, 504),
    session=None,
):
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session

if not os.path.exists("./d"):
	os.makedirs("./d");

allurls = open("urls.txt","wt");

def fetchUrl(url):
	global hold;
	try:
		print "Fetching {0}".format(url);
		r = requests_retry_session().get(url,timeout=5);
		if r.status_code == 200:
			time.sleep(2);
			content = r.content;
			tree = etree.HTML(content);

			anchor = tree.xpath('//a/@href');
			text = tree.xpath('//a/text()');

			if len(anchor) > 0 and len(text) > 0:
				o = {}
				o['url'] = "https://www.nseindia.com" + anchor[0];
				o['txt'] = text[0];
				hold.append(o);
				allurls.write("{0}\n".format(o['url']));
	except Exception as e:
		print e;

def fetchFile(obj):
	url = obj['url'];
	name = obj['txt'];
	headers = {
		'User-Agent': 'Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
		'referer': 'https://www.nseindia.com/products/content/equities/equities/archieve_eq.htm#'
	};
	try:
		r = requests.get(url,stream=True,headers=headers);

		with open("./d/"+name,'wb') as fd:
			for chunk in r.iter_content(2048):
				fd.write(chunk);
	except Exception as e:
		print e;

count = 0 
hold = [];
dates = [];
urls = [];
sdate = datetime.strptime('10-11-2017','%d-%m-%Y');

while count < 3800:
	dates.append(sdate.strftime('%d-%m-%Y'));
	sdate = sdate - timedelta(1);
	count = count + 1;

for adate in dates:
	url = "https://www.nseindia.com/ArchieveSearch?h_filetype=eqbhav&date={0}&section=EQ".format(adate);
	urls.append(url);

pool = ThreadPool(processes=50);
pool.map(fetchUrl,urls);

npool = ThreadPool(processes=30);
npool.map(fetchFile,hold);
allurls.close();