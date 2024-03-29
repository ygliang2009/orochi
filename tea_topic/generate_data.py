import json

tasklist_dict = {'1':{
  'topic': '情绪任务',
  'tagid': '101',
  'jobtype': '短期任务',
  'tip': ['完成5次鼓励学生任务，使得学生上课情绪高涨!'],
  'count':5,
  'total_step': '1',
  'rewards': '10'},
 '2':{
  'topic': '开口时长任务',
  'tagid': '102,104,105',
  'jobtype': '中期任务',
  'tip': ['引导学生积极交流，5节课开口时长超过3分钟',
   '加强引导学生思维20次，使得学生更加专注',
   '引导学生积极交流，使得每节课开口时长超过3分钟超过5节课'],
  'count':3,
  'total_step': '3',
  'rewards': '50'}, 
 '3':{
  'topic': '互动任务',
  'tagid': '103',
  'jobtype': '短期任务',
  'tip': ['完成50次交互任务，使得学生得到更多的积极鼓励'
   ],
   'count':50,
  'total_step': '1',
  'rewards': '20'},
 '4':{
  'topic': '专注任务',
  'tagid': '104',
  'jobtype': '短期任务',
  'tip': ['完成5堂课专注超过10分钟,增加学生专注度'
   ],
  'total_step': '1',
  'count':10,
  'rewards': '20'},
 '5':{
  'topic': '情绪任务',
  'tagid': '104',
  'jobtype': '短期任务',
  'tip': ['情绪大挑战,完成1堂课学生高兴情绪5次以上'],
  'total_step': '1',
  'count':5,
  'rewards': '20'}
}

with open('data/tasklist.json', 'w')as tl:
    tl.write(json.dumps(tasklist_dict))

tea_x_task_dict = {'111':{ '3':{'current_step':'-1','status':'2','start_time':'2019-10-24 00:00:00','finish_time':'2019-10-24 23:00:02','mode':'active'},'5':{'current_step':'1','status':'0','start_time':'-1','finish_time':'-1','mode':'push'} }}
#tea_x_task_dict = {'111':{'1':{'current_step':'1','status':'0','start_time':'-1','finish_time':'-1','mode':'push'}, '3':{'current_step':'-1','status':'2','start_time':'2019-10-24 00:00:00','finish_time':'2019-10-24 23:00:02','mode':'active'},'5':{'current_step':'1','status':'0','start_time':'-1','finish_time':'-1','mode':'push'} }}

with open('data/tea_x_task.json', 'w') as tl:
    tl.write(json.dumps(tea_x_task_dict))


ranklist = {'111':{'name':'James', 'score':77.5, '101':30, '102':22.5, '103':15, '104':110},'144':{'name':'Tony', 'score':55.09, '101':30, '102':22.5, '103':45, '104':60},'196':{'name':'Linda','score':44.4, '101':30, '102':22.5, '103':15, '104':60},'160':{'name':'John','score':29.4, '101':10, '102':22.5, '103':15, '104':40},'111':{'name':'Juice','score':58.1, '101':30, '102':22.5, '103':15, '104':110}}

with open('data/ranklist.json', 'w') as rl:
    rl.write(json.dumps(ranklist))
