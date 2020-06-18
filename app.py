from flask import Flask, request, render_template, redirect, url_for, abort, session
import dbdb
import random

app = Flask(__name__)

app.secret_key = b'aaa!111/'

@app.route('/')
def main():
    return render_template('main.html')
    
# 로그인
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        id = request.form['id']
        pw = request.form['pw']
        ret = dbdb.select_user(id, pw)
        if ret != None:
            session['user'] = id
            return '''
                <script> alert('안녕하세요~ {}님');
                location.href="/"
                </script>
                '''.format(ret[2])
        else:
            return '''
                <script> alert('아이디 또는 패스워드를 확인 하세요');
                location.href="/login"
                </script>
                '''

# 로그아웃(session 제거)
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('main'))

# 회원 가입
@app.route('/join', methods=['GET', 'POST'])
def join():
    if request.method == 'GET':
        return render_template('join.html')
    else:
        id = request.form["id"]
        pw = request.form["pw"]
        name = request.form["name"]
        if id == "":
            return '''
                <script>
                alert('아이디를 입력 해주세요');
                location.href='/join';
                </script>
                '''
        elif pw == "":
            return '''
                <script>
                alert('비밀번호를 입력 해주세요');
                location.href='/join';
                </script>
                '''
        elif name == "":
            return '''
                <script>
                alert('이름을 입력 해주세요');
                location.href='/join';
                </script>
                '''
        ret = dbdb.check_id(id)
        if ret != None:
            return '''
                <script>
                alert('다른 아이디를 사용하세요');
                location.href='/join';
                </script>
                '''
        # id와 pw가 db 값이랑 비교 해서 맞으면 맞다 틀리면 틀리다
        dbdb.insert_user(id, pw, name)
        return redirect(url_for('login'))

#로그인 사용자만 이용 가능 (학생정보)
@app.route('/getinfo')
def getinfo():
    if 'user' in session:
        ret = dbdb.select_all()
        return render_template('getinfo.html', data=ret)
    return '''
        <script> alert('로그인 후에 이용 가능합니다');
        location.href="/login"
        </script>
        '''

# 게임 시작
@app.route('/game')
def game():
    return redirect(url_for('input_num', num=1))

monster = {}

# 게임 설정
@app.route('/input/<int:num>')
def input_num(num):
    if 'user' in session:
        ret = dbdb.check_id(session['user'])
        if ret != None:
            character = {'name':ret[2], 'hp':ret[3], 'mp':ret[4]}
            if num == 1: # 게임시작
                character['hp'] = 30
                character['mp'] = 10
                dbdb.set_status(character['hp'], character['mp'], ret[0])
                sendtext = '''
                {0}님 반갑습니다. (HP : {1}, MP : {2}, 스킬 : 마법의 수정화살) 으로 게임을 시작 합니다.
                '''.format(character['name'], character['hp'], character['mp'])
                return render_template('game.html', data=character, context=sendtext, index=1)
            elif num == 2: # 게임오버
                return render_template('game.html', data=character, index=2)
            elif num == 3: # 몬스터대치
                monster[session['user']] = {'name':"다리우스", 'hp':50, 'atk_min':1, 'atk_max':3}
                return render_template('game.html', data=character, monster=monster[session['user']], index=3)
            elif num == 4: # 전투개시
                return render_template('game.html', data=character, monster=monster[session['user']], index=4)
            elif num == 5: # 공격한다
                MonsterDamage = random.randint(monster[session['user']]['atk_min'], monster[session['user']]['atk_max'])
                character['hp'] -= MonsterDamage
                if character['hp'] < 1:
                    dbdb.set_status(0, character['mp'], ret[0])
                    return '''
                        <script> alert('HP가 0이 되어 당신은 사망 하였습니다');
                        location.href="/input/2"
                        </script>
                        '''
                dbdb.set_status(character['hp'], character['mp'], ret[0])
                MyDamage = random.randint(1, 5)
                monster[session['user']]['hp'] -= MyDamage
                if monster[session['user']]['hp'] < 1:
                    return render_template('game.html', data=character, index=5)
                sendtext = '''당신은 {0} 의 데미지를 입었습니다.\n{1} 에게 {2} 의 데미지를 입혔습니다.'''.format(MonsterDamage, monster[session['user']]['name'], MyDamage)
                return render_template('game.html', data=character, monster=monster[session['user']], context=sendtext, index=4)
            elif num == 6: # 스킬사용
                MonsterDamage = random.randint(monster[session['user']]['atk_min'], monster[session['user']]['atk_max'])
                if character['mp'] >= 3:
                    character['mp'] -= 3
                    character['hp'] -= MonsterDamage
                    if character['hp'] < 1:
                        dbdb.set_status(0, character['mp'], ret[0])
                        return '''
                            <script> alert('HP가 0이 되어 당신은 사망 하였습니다');
                            location.href="/input/2"
                            </script>
                            '''
                    dbdb.set_status(character['hp'], character['mp'], ret[0])
                    MyDamage = random.randint(5, 10)
                    monster[session['user']]['hp'] -= MyDamage
                    if monster[session['user']]['hp'] < 1:
                        return render_template('game.html', data=character, index=5)
                    sendtext = '''당신은 {0} 의 데미지를 입었습니다.\n{1} 을(를) 사용하여 {2} 에게 {3} 의 데미지를 입혔습니다.'''.format(MonsterDamage, "마법의 수정화살", monster[session['user']]['name'], MyDamage)
                    return render_template('game.html', data=character, monster=monster[session['user']], context=sendtext, index=4)
                else:
                    sendtext = '''MP가 부족하여 스킬을 사용 할 수 없습니다.'''
                    return render_template('game.html', data=character, monster=monster[session['user']], context=sendtext, index=4)   
                return "알 수 없는 오류" 
    return '''
        <script> alert('로그인 후에 이용 가능합니다');
        location.href="/login"
        </script>
        '''

if __name__ == '__main__':
    app.run(debug=True)
