import requests;
from lxml import etree;
from datetime import datetime,timedelta;
import threading;
import os;

os.makedirs("./d");

count = 0 
hold = [];
dates = [];
threads = [];
sdate = datetime.strptime('10-11-2017','%d-%m-%Y');

while count < 2000:
	dates.append(sdate.strftime('%d-%m-%Y'));
	sdate = sdate - timedelta(1);
	count = count + 1;

def fetchUrl(url):
	global hold;
	r = requests.get(url);
	if r.status_code == 200:
		content = r.content;
		tree = etree.HTML(content);

		anchor = tree.xpath('//a/@href');
		text = tree.xpath('//a/text()');

		if len(anchor) > 0 and len(text) > 0:
			o = {}
			o['url'] = "https://www.nseindia.com" + anchor[0];
			o['txt'] = text[0];
			hold.append(o);

def fetchFile(url,name):
	headers = {
		'User-Agent': 'Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
		'referer': 'https://www.nseindia.com/products/content/equities/equities/archieve_eq.htm#'
	};
	r = requests.get(url,stream=True,headers=headers);

	with open("./d/"+name,'wb') as fd:
		for chunk in r.iter_content(2048):
			fd.write(chunk);

for adate in dates:
	url = "https://www.nseindia.com/ArchieveSearch?h_filetype=eqbhav&date={0}&section=EQ".format(adate);
	print "fetching {0}".format(url);
	t = threading.Thread(target=fetchUrl,args=(url,));
	t.start();
	threads.append(t);

for thread in threads:
	thread.join();

threads = [];
for aitem in hold:
	print "fetching {0}".format(aitem['url']);
	t = threading.Thread(target=fetchFile, args=(aitem['url'], aitem['txt']));
	t.start();
	threads.append(t);

for thread in threads:
	thread.join();