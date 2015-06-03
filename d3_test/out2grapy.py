import kongdeju
import sys
import json, datetime
import dumper
import matplotlib
import MySQLdb
matplotlib.use('Agg')
from matplotlib import pylab as plot
import MySQLdb
import logging
import time
import threading

class DB(object):
    conn = None
    cursor = None

    def connect(self):
        logging.info(time.ctime() + " : connect to mysql server..")
        self.conn = MySQLdb.connect(host='112.124.13.146', port=3306, user='gpo',
                                    passwd='btlc123', db='clinic', charset='utf8')
        self.conn.autocommit(True)

    def thread(self):
        t = threading.Thread(target=self.conn.ping, args=())
        t.setDaemon(True)
        t.start()
        t.join(2)
        if t.isAlive():
            return 0
        else:
            return 1

    def execute(self, sql_query):
        try:
            logging.info(time.ctime() + " : " + sql_query)
            i = 0
            while i < 3 and self.thread() != 1:
                self.close()
                self.connect()
                self.cursor = self.conn.cursor()
                i += 1
            if i == 3:
                return logging.error(time.ctime() + "execute failed")
            handled_item = self.cursor.execute(sql_query)
        except Exception, e:
            logging.error(e.args)
            logging.info("Reconnecting..")
            self.connect()
            self.cursor = self.conn.cursor()
            logging.info(time.ctime() + " : " + sql_query)
            handled_item = self.cursor.execute(sql_query)
        return handled_item

    def fetchone(self):
        try:
            logging.info(time.ctime() + " : fetchone")
            one_item = self.cursor.fetchone()
        except Exception, e:
            logging.error(e.args)
            logging.info(time.ctime() + " : fetchone failed, return ()")
            one_item = ()
        return one_item

    def fetchall(self):
        try:
            logging.info(time.ctime() + " : fetchall")
            all_item = self.cursor.fetchall()
        except Exception, e:
            logging.error(e.args)
            logging.info(time.ctime() + " : fetchall failed, return ()")
            all_item = ()
        return all_item

    def close(self):
        logging.info(time.ctime() + " : close connect")
        if self.cursor:
            self.cursor.close()
        self.conn.close()
#################################
def new_variant_data_pic(sample_no, pic1_str, pic2_str):
    try:
        db = DB()
        sel_variant_filter_run = "SELECT COUNT(*) FROM variant_data_pic WHERE sample_no = %d;" % (int(sample_no))
        con = db.execute(sel_variant_filter_run)
        if con != 1:
            return json.dumps({"status": 004, "message": "Error, return signal only."})
        else:
            results = db.fetchall()
            for item in results:
                count = item[0]
            if count == 0:
                ins_var_filter_run_result = "INSERT INTO variant_data_pic(sample_no,pic1,pic2)" \
                               " VALUES (%d,'%s','%s') "% (int(sample_no),  pic1_str, pic1_str)
            else:
                ins_var_filter_run_result = "UPDATE variant_data_pic SET pic1 = '%s',pic2 = '%s' " \
                               "WHERE sample_no = %d;"% (pic1_str, pic2_str, int(sample_no))
            update_flag = db.execute(ins_var_filter_run_result)
            return json.dumps({"status": 002, "message": "Data has, return signal only."})
    except Exception, e:
        return json.dumps({"status": 703, "message": "Unexpected Error happened in internal. :%s "% e})
###########################################################################################################
def table2dict(lines):
	colnames = lines[0].strip("\n").split('\t')
	colnums = len(colnames)
	dict_out = {}
	for item in colnames:
		dict_out[item] =[]
	for line in lines[1:]:
		i = 0
		items = line.strip('\n').split('\t')
		for item in items:
			dict_out[colnames[i]].append(item)
			i = i + 1
	return dict_out
def Ti_Tv(type_list):
	Ti = ['AG','GA','CT','TC']
	Ti_num = 0
	Tv_num = 0
	for item in type_list:
		if item in Ti:
			Ti_num = Ti_num +1
		else:
			Tv_num = Tv_num +1
	ratio = '%.2f' % (float(Ti_num)/float(Tv_num))
	return ratio
fp = open(sys.argv[1],'r')
lines = fp.readlines()
dict_out = table2dict(lines)
#####This is for chrome picture#####
chrome_list =  dict_out['Chr']
chrome_dict = kongdeju.list2dict(chrome_list)
####This is for genomic Ti/Tv#######
refs = dict_out['Ref']
vars = dict_out['Alt']
exotic_type = dict_out['Func.refGene']
genome_type_list = []
exotic_type_list = []
for ref,var,exo in zip(refs,vars,exotic_type):
	type = ref + var
	if not '-' in type:
		genome_type_list.append(type)
		if exo == 'exonic':
			exotic_type_list.append(type)

genome_ti_tv = Ti_Tv(genome_type_list)
exotic_ti_tv = Ti_Tv(exotic_type_list)
#### This is for coverage ####
read1 = dict_out['read1']
read2 = dict_out['read2']
coverage = []
for r1,r2 in zip(read1,read2):
	if r1:
		r1 = int(r1)
	else:
		r1 = 0
	if r2:
		r2 = int(r2)
	else:
		r2 = 0
	cov = r1 + r2
	coverage.append(cov)

cov_mean = kongdeju.mean(coverage)
cov_mean = '%.2f' % cov_mean
#####This is for quality ######
qual = dict_out['quality']
qnums = len(qual)
qn = 0
for item in qual:
	item = float(item)
	if item >= 40:
		qn = qn + 1
q40 = (float(qn)/float(qnums)) * 100
q40 = '%.2f' % q40
sample_no = sys.argv[2]
pic1=[genome_ti_tv,exotic_ti_tv,cov_mean,q40]
y,x,z = plot.hist(coverage,50,normed=1,histtype='bar',cumulative=-1,color='Burlywood')
'''
plot.xlabel('SNP depth')
plot.ylabel('Fraction of total SNP')
plot.title('Coverage')
out_fig = sample_no + '_pic2.svg'
plot.savefig(out_fig,format='svg')
'''
def addslashes(s):
    d = {'"':'\\"', "'":"\\'", "\0":"\\\0", "\\":"\\\\"}
    return ''.join(d.get(c, c) for c in s)
zft = {}
vals = []
for x1,y1 in zip(x,y):
	x1 = '%.2f' %x1
	y1 = '%.2f' %y1
	vals.append([x1,y1])
zft['data'] = vals
zft['x-label'] = 'SNP depth'
zft['y-label'] = 'fraction of all SNP'
pic2_str= json.dumps(zft)
pic1_str= json.dumps(pic1)
new_variant_data_pic(sample_no,pic1_str,pic2_str)
#####This is end ##########
