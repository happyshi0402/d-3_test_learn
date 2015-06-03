#!/usr/bin/python 
import sys
import re
import kongdeju
import fisher
import operator
import json, datetime
import MySQLdb
import logging
import time
import threading
import os
#from bio_med_tools.Mysql_db import DB
kdjPath = "/home/kongdeju/"
###############The only input is annotated_vcf.out file ###################

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
def new_variant_filter1(filter_id, filter_info, account):
    try:
        db = DB()
        sel_variant_filter_run = "SELECT COUNT(*) FROM variant_filter_ruan_result WHERE filter_id = %d;" % (int(filter_id))
        con = db.execute(sel_variant_filter_run)
        if con != 1:
            return json.dumps({"status": 004, "message": "Error, return signal only."})
        else:
            results = db.fetchall()
            filter_run_result = str(filter_info).strip().replace('\'s',' s ')
            ins_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            for item in results:
                count = item[0]
            if count == 0:
                ins_var_filter_run_result = "INSERT INTO variant_filter_ruan_result(filter_id,account,filter_run_result,ins_date)" \
                               " VALUES (%d,'%s','%s','%s') "% (int(filter_id), account, filter_run_result, ins_date)
            else:
                ins_var_filter_run_result = "UPDATE variant_filter_ruan_result SET account = '%s',filter_run_result = '%s',ins_date = '%s' " \
                               "WHERE filter_id = %d;"% (account, filter_run_result, ins_date, int(filter_id))
            update_flag = db.execute(ins_var_filter_run_result)
            return json.dumps({"status": 002, "message": "Data has, return signal only."})
    except Exception, e:
        return json.dumps({"status": 703, "message": "Unexpected Error happened in internal. :%s "% e})
#############soft run start###############################################
ref = sys.argv[1]
refs = []
fp_ref = open(ref,'r')
fp_ref.readline()
for line in fp_ref:
    nl = line.strip("\n").split("\t")[25]
    refs.append(nl)
refs_uniq = list(set(refs))
os.remove(ref)
#############known2ref.txt###############################################
fp_know = open( kdjPath + 'kegg/knownToRefSeq.txt','r')#('/home/kongdeju/kegg/knownToRefSeq.txt','r')
ref1 = {}
know1 = {}
knows=[]
i=1
for line in fp_know:
	lines = line.strip().split("\t")
	ref1[i] = lines[1]
	know1[i] = lines[0]
	i = i+1
for x,r in ref1.items():
	if r in refs_uniq:
		knows.append(know1[x])
kg_uniq = list(set(knows))
#################################know2kegg.txt########################
fp_path = open(kdjPath + 'kegg/keggPathway.txt','r')#('/home/kongdeju/kegg/keggPathway.txt','r')
j=1
know2={}
path={}
for line in fp_path:
	lines= line.strip("\n").split("\t")
	know2[j] = lines[0]
	path[j] = lines[2]
	j = j+1
path_test =[]
path_sort = path.values()
for x,k in know2.items():
	if k in kg_uniq:
		path_test.append(path[x])
path_test.sort()
path_sort.sort()
test_path_dict = kongdeju.list2dict(path_test)
kegg_path_dict = kongdeju.list2dict(path_sort)
kegg_path_list = kegg_path_dict.keys()
kegg_path_list.sort()
outcome={}
outcome_short = {}
##########fisher exact test start##########
fisher_n = len(kg_uniq)
fisher_N = len(set(know2.values()))
for item in kegg_path_list:
	kegg_M = kegg_path_dict[item]
	if item in test_path_dict.keys():
		test_k = test_path_dict[item]
	else:
		test_k = 0
	p = fisher.pvalue(test_k,kegg_M,fisher_n-test_k,fisher_N-kegg_M).right_tail
	outcome[item]= [fisher_N,fisher_n,kegg_M,test_k,p]
	outcome_short[item] = p
sorted_outcome = sorted(outcome_short.items(),key=operator.itemgetter(1))
i=1
n= len(outcome)
for (x,y) in sorted_outcome:
	q = y*n/i
	i = i+1
	outcome[x].append(q)	
fp_name = open( kdjPath + 'kegg/keggMap.txt')
kegg_name = {}
new_outcome = {}
for line in fp_name:
	lines = line.strip("\n").split("\t")
	kegg_name[lines[0]] = lines[1]
for x,y in outcome.items():
	new_outcome[kegg_name[x]] = y
##################################################################################above is enough######################################
########fisher exact test end##################
fp3 = open(kdjPath+ 'kegg/ko00001.keg','r')
keggs = fp3.readlines()
kegg_dict = kongdeju.kegg2dict(keggs)
##########insert into sqldb###################
kegg_json = {"name":'kegg_pathways',"children":[]}
i=0
kegg_list_path=[]
for x,y in kegg_dict.items():
	kegg_json['children'].append({"name":x,"children":[]})
	j=0
	q=0
	for a,b in y.items():
		kegg_json['children'][i]['children'].append({"name":a,'children':[]})
		z=0
		for c,d in b.items():
			if c in new_outcome.keys() and new_outcome[c][3] >0 :
				tmp =[{'name':'Q_value: %g' % new_outcome[c][5]},{'name':'P_value: %g' % new_outcome[c][4]},{'name': 'num of mapped genes: %s' % new_outcome[c][3]},{'name': 'num of genes in this pathway: %s' % new_outcome[c][2]}]
				kegg_json['children'][i]['children'][j]['children'].append({'name':c,'children':tmp})
				kegg_dict[x][a][c] = new_outcome[c]
				kegg_list_path.append([c,new_outcome[c][2],new_outcome[c][3],new_outcome[c][4],new_outcome[c][5]])
				z= z +new_outcome[c][3]
				q=q+new_outcome[c][3]
		kegg_json['children'][i]['children'][j]['name'] = a + '(' + str(z) + ')'
		if z == 0 :
			del kegg_json['children'][i]['children'][j]['children']
		j=j+1
	kegg_json['children'][i]['name'] = x + '(' + str(q) + ')'
	i=i+1
out_file_name = sys.argv[2]
account = sys.argv[3]
new_variant_filter1(out_file_name, json.dumps(kegg_json), account)
# fp = open(out_file_name+'.json','w')
# xx =json.dumps(kegg_json)
# fp.write(xx)










