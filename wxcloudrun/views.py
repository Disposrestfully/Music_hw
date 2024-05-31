from datetime import datetime
from flask import render_template, request, jsonify
from run import app
from wxcloudrun.dao import delete_counterbyid, query_counterbyid, insert_counter, update_counterbyid
from wxcloudrun.dao import query_ballbyname, insert_ball, update_ballbyname, get_allballs
from wxcloudrun.model import Counters, Balls
from wxcloudrun.response import make_succ_empty_response, make_succ_response, make_err_response


@app.route('/')
def index():
    """
    :return: 返回index页面
    """
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    params = request.get_json()
    name = params['name']
    ball = query_ballbyname(name)
    if ball is None:
        ball = Balls()
        ball.renew = 0
        ball.name = name
        insert_ball(ball)
    else:
        ball.renew = 1
        update_ballbyname(ball)
    return make_succ_empty_response()

@app.route('/read', methods=['GET'])
def read():
    return jsonify(get_allballs())

@app.route('/write', methods=['POST'])
def write():
    params = request.get_json()
    text_list = params['text']
    for input_text in text_list:
        ball = query_ballbyname(input_text)
        if ball != None:
            ball.renew = 0
            update_ballbyname(ball)
    return jsonify({'message': 'success'})


@app.route('/api/count', methods=['POST'])
def count():
    """
    :return:计数结果/清除结果
    """

    # 获取请求体参数
    params = request.get_json()

    # 检查action参数
    if 'action' not in params:
        return make_err_response('缺少action参数')

    # 按照不同的action的值，进行不同的操作
    action = params['action']

    # 执行自增操作
    if action == 'inc':
        counter = query_counterbyid(1)
        if counter is None:
            counter = Counters()
            counter.id = 1
            counter.count = 1
            counter.created_at = datetime.now()
            counter.updated_at = datetime.now()
            insert_counter(counter)
        else:
            counter.id = 1
            counter.count += 1
            counter.updated_at = datetime.now()
            update_counterbyid(counter)
        return make_succ_response(counter.count)

    # 执行清0操作
    elif action == 'clear':
        delete_counterbyid(1)
        return make_succ_empty_response()

    # action参数错误
    else:
        return make_err_response('action参数错误')


@app.route('/api/count', methods=['GET'])
def get_count():
    """
    :return: 计数的值
    """
    counter = Counters.query.filter(Counters.id == 1).first()
    return make_succ_response(0) if counter is None else make_succ_response(counter.count)
