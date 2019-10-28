from tea_topic import app
from flask import Request
from flask import Flask, request, redirect, Response
from flask import render_template
import os
import json
import datetime


base_data_path = '/home/liangyunge/workspace/tea_topic/data'
tasklist_db = 'tasklist.json'
tea_x_task_db = 'tea_x_task.json'
ranklist_db = 'ranklist.json'

@app.route('/index')
def index():
    return render_template('index.html', title = '教室主页') 

@app.route('/list')
def list():
    if 'tid' not in request.args:
        return 'Pls input tid'
    tid = request.args['tid']
    tasklist_data_path = os.path.join(base_data_path, tasklist_db)
    tea_x_task_data_path = os.path.join(base_data_path, tea_x_task_db)

    with open(tasklist_data_path, 'r') as tdp:
        tasklist_datas = json.loads(tdp.read().strip())

    with open(tea_x_task_data_path, 'r') as ttdp:
        tea_x_task_datas = json.loads(ttdp.read().strip())

    with open(tasklist_data_path, 'r') as tdp:
        tasklist_datas = json.loads(tdp.read().strip())
    if tid not in tea_x_task_datas:
        return 'Pls input valid tid'
    tea_x_task = tea_x_task_datas[tid] 
    return render_template('list.html', title = '任务列表', tasklist_data = tasklist_datas, tea_x_task = tea_x_task, tid = tid) 


@app.route('/main')
def main():
    if 'tid' not in request.args:
        return 'Pls input tid'
    tid = request.args['tid']
    tasklist_data_path = os.path.join(base_data_path, tasklist_db)
    tea_x_task_data_path = os.path.join(base_data_path, tea_x_task_db)

    with open(tea_x_task_data_path, 'r') as ttdp:
        tea_x_task_datas = json.loads(ttdp.read().strip())

    with open(tasklist_data_path, 'r') as tdp:
        tasklist_datas = json.loads(tdp.read().strip())
    if tid not in tea_x_task_datas:
        return 'Pls input valid tid'

    tea_x_task = tea_x_task_datas[tid] 
    jdone = 0
    rewards = '0'
    tea_info = {}
    score = 0
    if 'status' in request.args and request.args['status'] == 'jd' and 'rewards' in request.args:
        jdone = 1
        rewards = request.args['rewards']

        ranklist_data_path = os.path.join(base_data_path, ranklist_db)
        ranklist = {}
        with open(ranklist_data_path, 'r') as rdp:
            ranklist = json.loads(rdp.read().strip())
        if tid in ranklist:
            tea_info = ranklist[tid]
        ranklist[tid]['score'] += int(rewards)
        score = ranklist[tid]['score']
        __update_db('ranklist', ranklist)
    return render_template('main.html', title = '主页', tasklist_data = tasklist_datas, tea_x_task = tea_x_task, tid = tid, jdone = jdone, rewards = rewards, score = score, tea_info = tea_info) 

@app.route('/submit')
def submit():
    if 'jobid' not in request.args or 'tid' not in request.args:
        return 'sss Pls input valid jobid and tid'
    jobid = request.args['jobid']
    tid = request.args['tid']

    tasklist_data_path = os.path.join(base_data_path, tasklist_db)
    tea_x_task_data_path = os.path.join(base_data_path, tea_x_task_db)

    with open(tasklist_data_path, 'r') as tdp:
        tasklist_datas = json.loads(tdp.read().strip())

    with open(tea_x_task_data_path, 'r') as ttdp:
        tea_x_task_datas = json.loads(ttdp.read().strip())
     
    if jobid not in tasklist_datas or tid not in tea_x_task_datas or jobid not in tea_x_task_datas[tid]:
        return 'Pls input valid jobid and tid'
    jobdetail = tasklist_datas[jobid]
    tea_x_task_detail = tea_x_task_datas[tid][jobid] 
    return render_template('submit.html', title = '任务确认', detail = jobdetail, tea_x_task = tea_x_task_detail, jobid = jobid, tid = tid) 


@app.route('/commit')
def commit():
    if 'jobid' not in request.args or 'tid' not in request.args:
        return 'Pls input valid jobid and tid'
    submit_type = '0'
    if 'submit_type' in request.args:
        submit_type = request.args['submit_type']
    jobid = request.args['jobid']
    tid = request.args['tid']

    tea_x_task_data_path = os.path.join(base_data_path, tea_x_task_db)
    with open(tea_x_task_data_path, 'r') as ttdp:
        tea_x_task_datas = json.loads(ttdp.read().strip())

    if tid not in tea_x_task_datas or jobid not in tea_x_task_datas[tid]:
        return 'ttt Pls input valid jobid and tid'
    if submit_type == '0': 
        tea_x_task_datas[tid][jobid]['status'] = '1'
        tea_x_task_datas[tid][jobid]['start_time'] = str(datetime.datetime.now())
    if submit_type == '1': 
        tea_x_task_datas[tid][jobid]['status'] = '2'
        tea_x_task_datas[tid][jobid]['finish_time'] = str(datetime.datetime.now())
    __update_db('tea_x_task', tea_x_task_datas)
    return json.dumps({'errno':0,'msg':'commit success'})

@app.route('/rankpage')
def rankpage():
    if 'tid' not in request.args:
        return 'Pls input tid'
    tid = request.args['tid']
    ranklist_data_path = os.path.join(base_data_path, ranklist_db)
    with open(ranklist_data_path, 'r') as rdp:
        ranklist = json.loads(rdp.read().strip())
    ordered_ranklist = []
    for _, info in ranklist.items():
        ordered_ranklist.append(info)
    def rank_node(node):
        return node['score']
    ordered_ranklist.sort(key = rank_node, reverse = True)
    return render_template('rankpage.html', title = '排行榜列表', tid = tid, ranklist = ordered_ranklist) 


@app.route('/addjob')
def addjob():
    if 'tid' not in request.args or 'jobid' not in request.args:
        return 'Pls input tid or jobid'
    tid = request.args['tid']
    jobid = request.args['jobid']

    tasklist_data_path = os.path.join(base_data_path, tasklist_db)
    with open(tasklist_data_path, 'r') as tdp:
        tasklist_datas = json.loads(tdp.read().strip())

    tea_x_task_data_path = os.path.join(base_data_path, tea_x_task_db)

    with open(tea_x_task_data_path, 'r') as ttdp:
        tea_x_task_datas = json.loads(ttdp.read().strip())
 
    add_status = 0
    if tid not in tea_x_task_datas:
        tea_x_task_datas[tid] = {}
    if jobid not in tea_x_task_datas[tid]:
        tea_x_task_datas[tid][jobid] = {"current_step":"1","status":"0","start_time":"-1","finish_time":"-1","mode":"active"} 
        __update_db('tea_x_task', tea_x_task_datas)
        add_status = 1
    return json.dumps({'errno':0,'errmsg':'insert ok','add_status':add_status, 'tips':tasklist_datas[jobid]['tip'][0]}) 

@app.route('/classroom')
def classroom():
    if 'tid' not in request.args or 'jobid' not in request.args:
        return 'Pls input valid tid and jobid'
    count = '0'
    tid = request.args['tid']
    jobid = request.args['jobid']

    if 'count' in request.args:
        count  = request.args['count']
    return render_template('classroom.html', title = '上课页面', count = count, tid = tid, jobid = jobid) 

@app.route('/lab')
def lab():
    return render_template('lab.html', title = '跑分页面') 


def __update_db(db_name, datas):
    with open(os.path.join(base_data_path, '%s.json'%(db_name)), 'w') as dn:
        dn.write(json.dumps(datas))
