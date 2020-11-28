
from flask import Flask, render_template, request, flash,  jsonify, redirect, url_for, session
from utils import query
import json
import time

# 创建flask对象
app = Flask(__name__)
app.config['SECRET_KEY'] = 'qweqwe'


@app.route('/index', methods=['GET', 'POST'])
def index():
    # uid = session.get('uid')
    sql_game = "select * from game"
    tup_game = query.query(sql_game)
    list_game = []
    list_games = []
    for game in tup_game:
        sql_score = "select floor(avg(score)) from purchase where gid = '%s';" % game[0]
        game_score = query.query(sql_score)
        aa = list(game_score[0])
        if aa[0] is None:
            aa[0]=0
        list_game = list(game)
        list_game.append(aa[0])
        
        #game like number
        sql_like = "select count(*) from likeGame where gid = '%s'" % game[0]
        game_like = query.query(sql_like)
        bb = list(game_like[0])
        # print(bb[0])
        if bb[0] is None:
            bb[0]=0
        list_game.append(bb[0])
        list_games.append(list_game)
    # print(list_games)
    list_games.sort(key=lambda a: a[9], reverse = True)
    tmp = list_games[0:5].copy()
    final_list = []
    final_list.append(tmp)
    list_games.sort(key=lambda a: a[5], reverse = True)
    tmp = list_games[0:5].copy()
    final_list.append(tmp)
    print(final_list)

    return render_template('index.html',result=final_list)



@app.route('/edit_personal', methods=['GET', 'POST'])
def edit_personal():
    uid = session.get('uid')
    if request.method == 'GET':
        return render_template('edit_personal.html')
    else:
        print(uid)
        name = request.form.get('name')
        password = request.form.get('password')
        gender = request.form.get('gender')
        age = request.form.get('age')
        region = request.form.get('region')

        sql="select * from user WHERE uid='%s'" % uid
        result=query.query(sql)
        if name=='':
            name=result[0][1]
        if password=='':
            password=result[0][5]
        if gender=='':
            gender=result[0][4]
        if age=='':
            age=result[0][2]
        if region=='':
            region=result[0][3]

        sql="UPDATE user SET uname='%s', age='%s', region='%s', gender='%s', passwd='%s' WHERE uid='%s'" % (name,age,region,gender,password,uid)
        print(result)
        query.update(sql)
        return redirect(url_for('personal_information'))

@app.route('/edit_company', methods=['GET', 'POST'])
def edit_company():
    cid = session.get('cid')
    if request.method == 'GET':
        return render_template('edit_company.html')
    else:
        name = request.form.get('name')
        password = request.form.get('password')
        flag = password
        sql="select * from company WHERE cid='%s'" % cid
        result=query.query(sql)
        if name=='':
            name=result[0][1]
        if password=='':
            password=result[0][2]

        sql="UPDATE company SET cname='%s' ,passwd='%s' WHERE cid='%s'" % (name,password,cid)
        print(result)
        query.update(sql)
        if flag!='':
            return redirect(url_for('company'))
        return redirect(url_for('company_index'))


@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method=='GET':
        return render_template('login.html')
    else:
        email = request.form.get('email')
        password = request.form.get('password')
        sql = "select * from user where uemail = '%s'" % email
        result = query.query(sql)
        
        if len(result) != 0:
            if result[0][5] == password:
                session['uid'] = result[0][0]
                session.permanent=True
        #         print(result)
        # print(result[0][4])
        # print(result[0])
                return redirect(url_for('index'))
            else:
                return u'wrong user or wrong password'
        else:
            return u'the user does not exist'
        

@app.route('/user_register', methods=['GET', 'POST'])
def user_register():
    if request.method=='GET':
        return render_template('user_register.html')
    else:
        user_email = request.form.get('user_email')
        user_name = request.form.get('user_name')
        password = request.form.get('password')
        age = int(request.form.get('age'))
        gender = request.form.get('gender')
        region = request.form.get('region')
        now = time.time()
        now = time.strftime('%Y/%m/%d')
        now = str(now)
        vify = "select * from user where uemail = '%s'" % user_email
        result = query.query(vify)
        if len(result) != 0:
            return u'user already exist'
        sql = "insert into user(uname,age,region,gender,passwd,reg_date,uemail) values( '%s','%d','%s','%s','%s','%s','%s' )" % (user_name,age,region,gender,password,now,user_email)
        query.update(sql)
        return redirect(url_for('login'))

@app.route('/company_register', methods=['GET', 'POST'])
def company_register():
    if request.method=='GET':
        return render_template('company_register.html')
    else:
        company_email = request.form.get('company_email')
        company_name = request.form.get('company_name')
        password = request.form.get('password')
        vify = "select * from company where cemail = '%s'" % company_email
        result = query.query(vify)
        if len(result) != 0:
            return u'company already exist'
        sql = "insert into company(cname,passwd,cemail) values( '%s','%s','%s')" % (company_name,password,company_email)
        query.update(sql)
        return redirect(url_for('company'))


@app.route('/company', methods=['GET', 'POST'])
def company():
    if request.method=='GET':
        return render_template('company.html')
    else:
        cemail = request.form.get('email')
        password = request.form.get('password')
        sql = "select * from company where cemail = '%s'" % cemail
        result = query.query(sql)
        print(result)
        if len(result) != 0:
            if result[0][2] == password:
                session['cid'] = result[0][0]
                session.permanent=True
                return redirect(url_for('company_index'))
            else:
                return u'wrong email or wrong password'
        else:
            return u'the user does not exist'



@app.route('/like', methods=['GET', 'POST'])
def like():
    likelist = []
    uid = session.get('uid')
    if request.method == 'GET':
        sql_like = "select gid from likeGame where uid = '%s'" % uid
        tup_gid = query.query(sql_like)
        # print(tup_gid)
        for gid_tup in tup_gid:
            gid = gid_tup[0]
            sql_game = "select * from game where gid = '%s'" % gid
            tup_game = query.query(sql_game)
            likelist.append(tup_game[0])
        return render_template('like.html', result = likelist)
    else:
        gidd = request.form.get("gid")
        # print(gidd)
        sql_uplike = "DELETE FROM likeGame WHERE gid ='%s' and uid ='%s'" % (gidd,uid)
        query.update(sql_uplike)
        sql_like = "select gid from likeGame where uid = '%s'" % uid
        tup_gid = query.query(sql_like)
        # print(tup_gid)
        for gid_tup in tup_gid:
            gid = gid_tup[0]
            sql_game = "select * from game where gid = '%s'" % gid
            tup_game = query.query(sql_game)
            likelist.append(tup_game[0])
        return render_template('like.html', result = likelist)


@app.route('/personal_information', methods=['GET', 'POST'])
def personal_information():
    uid = session.get('uid')
    sql = "SELECT * FROM user WHERE uid = '%s'" % uid
    result = query.query(sql)
    person_info = []
    person_info.append(result[0])
    sql_order = "select * from purchase where uid = '%s'" % uid
    order = query.query(sql_order)
    order_list=[]
    for single_order in order:
        sql_name = "select gname,picture from game where gid = '%s'" % single_order[2]
        name = query.query(sql_name)
        # print(name)
        dd = list(single_order)
        # print(dd)
        dd.append(name[0][0])
        dd.append(name[0][1])
        order_list.append(dd)
    person_info.append(order_list)
    # print(person_info)
    return render_template('personal_information.html', result=person_info)

@app.route('/company_index', methods=['GET', 'POST'])
def company_index():
    cid = session.get('cid')
    sql = "SELECT * FROM company WHERE cid = '%s'" % cid
    result = query.query(sql)
    return render_template('company_index.html', result=result)

@app.route('/company_gamelist', methods=['GET', 'POST'])
def company_gamelist():
    cid = session.get('cid')
    if request.method == 'GET':
        sql = "SELECT * FROM game WHERE cid = '%s'" % cid
        result1 = query.query(sql)
        list_result = []
        for game in result1:
            sql_score = "select floor(avg(score)) from purchase where gid = '%s';" % game[0]
            game_score = query.query(sql_score)
            aa = list(game_score[0])
            if aa[0] is None:
                aa[0]=0
            list_game = list(game)
            list_game.append(aa[0])
            
            sql_pcount = "select count(*) from purchase where gid = '%s'" % game[0]
            pur_count = query.query(sql_pcount)
            # print(pur_count)
            if pur_count[0][0] is None:
                pur_count[0][0] = 0
            list_game.append(pur_count[0][0])

            #game like number
            sql_like = "select count(*) from likeGame where gid = '%s'" % game[0]
            game_like = query.query(sql_like)
            bb = list(game_like[0])
            if bb[0] is None:
                bb[0]= 0
            # print(bb)
            list_game.append(bb[0])

            list_result.append(list_game)
        final_list = []
        list_result.sort(key=lambda a: a[9], reverse = True)
        tmp = list_result.copy()
        final_list.append(tmp)
        tmp = []
        for i in list_result:
            if i[9] == list_result[0][9] :
                tmp.append(i)
        # tmp = list_result[0].copy()
        final_list.append(tmp)
        list_result.sort(key=lambda a: a[10], reverse = True)
        tmp = list_result.copy()
        final_list.append(tmp)
        tmp=[]
        for i in list_result:
            if i[10] == list_result[0][10] :
                tmp.append(i)
        # print(tmp)
        final_list.append(tmp)
        # tmp = list_result[0].copy()
        # final_list.append(tmp)
        list_result.sort(key=lambda a: a[11], reverse = True)

        tmp = list_result.copy()
        final_list.append(tmp)
        tmp = []
        for i in list_result:
            if i[11] == list_result[0][11] :
                tmp.append(i)

        final_list.append(tmp)
        print(final_list)
        return render_template('company_gamelist.html', result=final_list)

@app.route('/view_publishment/<cid>', methods=['GET', 'POST'])
def view_publishment(cid):
    # if request.method == 'GET':
    sql = "SELECT * FROM game WHERE cid = '%s'" % cid
    result1 = query.query(sql)
    list_result = []
    sql_cname = "select cname from company where cid = '%s'" % cid
    cname = query.query(sql_cname)
    # print(cname[0][0])
    for game in result1:
        sql_score = "select floor(avg(score)) from purchase where gid = '%s';" % game[0]
        game_score = query.query(sql_score)
        aa = list(game_score[0])
        list_game = list(game)
        list_game.append(aa[0])
        
        #game like number
        sql_like = "select count(*) from likeGame where gid = '%s'" % game[0]
        game_like = query.query(sql_like)
        bb = list(game_like[0])
        # print(bb[0])
        list_game.append(bb[0])
        list_game.append(cname[0][0])
        list_result.append(list_game)
    print(list_result)
    if request.method == 'POST':
        uid = session.get('uid')
        gid = request.form.get('gid')
        now = time.time()
        now = time.strftime('%Y/%m/%d', time.localtime(now))
        now = str(now)
        sql_ins_pur = "insert into purchase(uid,gid,pdate) values('%s','%s','%s')" % (uid,gid,now)
        query.update(sql_ins_pur)
        
    return render_template('view_publishment.html', result=list_result)


@app.route('/game_index/<gid>', methods=['GET', 'POST'])
def game_index(gid):
    uid = session.get('uid')
    if request.method == 'POST':
        now = time.time()
        now = time.strftime('%Y-%m-%d', time.localtime(now))
        now = str(now)
        com = 'None comment'
        sql_ins_pur = "insert into purchase(uid,gid,pdate,comment) values('%s','%s','%s','%s)" % (uid,gid,now,com)
        query.update(sql_ins_pur)
    sql_score = "select floor(avg(score)) from purchase where gid = '%s';" % gid
    game_score = query.query(sql_score)
    aa = list(game_score[0])
    if aa[0] is None:
        aa[0]=0
    sql = "select * from game where gid = '%s'" % gid
    # print(sql)
    game = query.query(sql)
    # print(game)
    result = []
    result.append(list(game[0]))
    # like number
    sql_like = "select count(*) from likeGame where gid = '%s'" % gid
    game_like = query.query(sql_like)
    bb = list(game_like[0])
    # print(bb[0])
    result.append(bb[0])
    # comment
    sql_comment =  "select * from purchase where gid = '%s'" % gid
    comment = query.query(sql_comment)
    cc = list(comment)
    list_comment = []
    lists_comment = []
    for comtable in cc:
        if comtable[3] is None:
            continue
        sql_name = "select uname from user where uid ='%s'" % comtable[1]
        name = query.query(sql_name)
        list_comment = list(comtable)
        list_comment.append(name[0][0])
        lists_comment.append(list_comment)
        # print(name[0][0])
        # username.append(name[0][0])
    result.append(lists_comment)
    sql_cname = "select cname from company where cid = '%s'" % result[0][3]
    cname = query.query(sql_cname)
    # print(cname[0][0])
    result.append(cname[0][0])
    result.append(aa[0])
    print(result)
    return render_template('game_index.html', result=result)
    

@app.route('/company_gamepage/<gid>', methods=['GET', 'POST'])
def company_gamepage(gid):
    uid = session.get('uid')
    if request.method == 'GET':
        sql = "select * from game where gid = '%s'" % gid
        # print(sql)
        game = query.query(sql)
        # print(game)
        result = []
        result.append(list(game[0]))
        # like number
        sql_like = "select count(*) from likeGame where gid = '%s'" % gid
        game_like = query.query(sql_like)
        bb = list(game_like[0])
        # print(bb[0])
        result.append(bb[0])
        # comment
        sql_comment =  "select * from purchase where gid = '%s'" % gid
        comment = query.query(sql_comment)
        cc = list(comment)
        list_comment = []
        lists_comment = []
        for comtable in cc:
            sql_name = "select uname from user where uid ='%s'" % comtable[1]
            name = query.query(sql_name)
            list_comment = list(comtable)
            list_comment.append(name[0][0])
            lists_comment.append(list_comment)
            # print(name[0][0])
            # username.append(name[0][0])
        result.append(lists_comment)
        print(result)
        return render_template('company_gamepage.html', result=result)

@app.route('/game_comment/<gid>', methods=['GET', 'POST'])
def game_comment(gid):
    uid = int(session.get('uid') )
    result = []
    if request.method =='GET':
        sql_game = "select * from game where gid = '%s'" % gid
        game = query.query(sql_game)
        result.append(game[0])
        sql_like = "select count(*) from likeGame where gid = '%s'" % gid
        like = query.query(sql_like)
        result.append(like[0][0])
        print(result)
        return render_template('game_comment.html',result = result)
    else:
        score = request.form.get('score')
        comment = request.form.get('comment')
        print(score)
        print(comment)
        sql_upd = "update purchase set score = '%s', comment = '%s' where uid = '%s' and gid ='%s' " % (score,comment,uid,gid)
        print(sql_upd)
        query.update(sql_upd)
        return redirect(url_for('personal_information'))

@app.route('/publish', methods=['GET', 'POST'])
def publish():
    cid = int(session.get('cid') )
    if request.method =='GET':
        return render_template('publish.html')
    else:
        gname = request.form.get('gname')
        typee = request.form.get('type')
        price = int(request.form.get('price'))
        print(typee)
        gsystem = request.form.getlist('gsystem')
        strr= ";".join(gsystem)
        print(strr)
        sizeG = int(request.form.get('size'))
        now = time.time()
        now = time.strftime('%Y/%m/%d', time.localtime(now))
        now = str(now)
        picture = 'icon.png'
        sql_ins = "insert into game(gname,type,cid,price,release_date,gsystem,sizeG,picture) values('%s','%s','%d','%d','%s','%s','%d','%s')" % (gname,typee,cid,price,now,strr,sizeG,picture)
        print(sql_ins)
        query.update(sql_ins)
        return redirect(url_for('company_gamelist'))

@app.route('/game_store', methods=['GET', 'POST'])
@app.route('/game_store/<classs>', methods=['GET', 'POST'])
def game_store(classs):
    uid = session.get('uid')
    list_games = []
    if request.method == 'POST':
        gid = request.form.get("gid")
        print(gid)
        sql_ins_like = "insert into likeGame(uid,gid) values('%s','%s')" % (uid,gid)
        query.update(sql_ins_like)
    if classs == 'ALL':
        sql_game = "select * from game"
        tup_game = query.query(sql_game)
    else:
        sql_game = "select * from game where type = '%s'" % classs
        tup_game = query.query(sql_game)
    for game in tup_game:
        sql_score = "select floor(avg(score)) from purchase where gid = '%s';" % game[0]
        game_score = query.query(sql_score)
        aa = list(game_score[0])
        if aa[0] is None:
            aa[0]=0
        list_game = list(game)
        list_game.append(aa[0])
        
        #game like number
        sql_like = "select count(*) from likeGame where gid = '%s'" % game[0]
        game_like = query.query(sql_like)
        bb = list(game_like[0])
        # print(bb[0])
        if bb[0] is None:
            bb[0]=0
        list_game.append(bb[0])
        list_games.append(list_game)
    # print(list_games)
    list_games.sort(key=lambda a: a[9], reverse = True)
    tmp = list_games.copy()
    final_list = []
    final_list.append(tmp)
    list_games.sort(key=lambda a: a[10], reverse = True)
    tmp = list_games.copy()
    final_list.append(tmp)
    # print(final_list)

    # return redirect(url_for('game_store/all.html'),result)
    return render_template('game_store.html',result=final_list)
    
        



if __name__ == '__main__':
    app.run("0.0.0.0", debug=True)

