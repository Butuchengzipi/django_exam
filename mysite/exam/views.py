from django.shortcuts import render
import models
from django.http import HttpResponse


# Create your views here.


# 用户登录
def user_login(request):
    if request.method == 'POST':
        # 获取表单信息
        email = request.POST.get('email')
        password = request.POST.get('password')
        print("email", email, "password", password)

        # 通过唯一的email获取该用户实体
        user = models.User.objects.get(email=email)
        print(user)
        if password == user.pwd:  # 登录成功
            request.session['username'] = user.username  # user的值发送给session里的username
            request.session['is_login'] = True  # 认证为真
            # 查询考试信息
            user_exam = models.UserExam.objects.filter(user_id=user.id)
            # paper = models.TestPaper.objects.filter(major=student.major)

            # 查询成绩信息
            exam_info = models.ExamInfo.objects.filter(userexam_id=user_exam.id)
            # grade = models.Record.objects.filter(sid=student.sid)

            # 渲染index模板
            return render(request, 'index.html', {'user': user, 'user_exam': user_exam, 'exam_info': exam_info})
        else:
            return render(request, 'login.html', {'message': '密码不正确'})
    elif request.method == 'GET':
        return render(request, 'login.html')
    else:
        return HttpResponse("请使用GET或POST请求数据")


# 首页
def index(request):
    # 若session认证为真
    if request.session.get('is_login', None):
        email = request.session.get('email', None)
        print(email)
        user = models.User.objects.filter(email=email)
        user_exam = models.UserExam.objects.filter(user_id=user.id)

        # 查询成绩信息
        exam_info = models.ExamInfo.objects.filter(userexam_id=user_exam.id)
        # grade = models.Record.objects.filter(sid=student.sid)

        # 渲染index模板
        return render(request, 'index.html', {'user': user, 'user_exam': user_exam, 'exam_info': exam_info})
    else:
        return render(request, 'index.html')


# 显示当前用户的个人信息
def user_file(request):
    # 若session认证为真
    if request.session.get('is_login', None):
        email = request.session.get('email', None)
        print(email)
        user = models.User.objects.filter(email=email)

        # 查询用户信息
        user_info = models.UserInfo.objects.filter(user_id=user.id)

        # 渲染index模板
        return render(request, 'index.html', {'user': user, 'user_info': user_info})


# 显示当前用户的考试信息
def user_exam(request):
    # 若session认证为真
    if request.session.get('is_login', None):
        email = request.session.get('email', None)
        print(email)
        user = models.User.objects.filter(email=email)

        # 查询试卷信息
        user_exam_result = models.UserExam.objects.filter(user_id=user.id)
        # 查询详细
        exam_info = models.TestPaper.objects.filter(id=user_exam.test_id)

        # 渲染index模板
        return render(request, 'index.html', {'user': user, 'user_exam': user_exam, 'exam_info': exam_info})


# 学生退出登录,清除Session信息
def user_logout(request):
    # logout(request)
    request.session.clear()

    # reverse() 反转函数
    url = reverse('exam:index')
    # url反转后重定向
    return redirect(url)


# 开始考试，跳转到考试页面
def start_exam(request):
    email = request.GET.get('email')
    tid = request.GET.get('tid')
    # 获取用户对象
    user = models.User.objects.filter(email=email)

    # 获取用户信息
    user_info = models.UserInfo.object.filter(user_id=user.id)

    # 试卷信息
    paper = models.TestPaper.objects.filter(id=tid)

    # 题目
    question = models.QestionBank.objects.filter(test_id=tid)

    context = {
        'username': user.username,
        'email': email,
        'gender': user_info.gender,
        'age': user_info.age,
        'description': paper.description,
        'introduction': paper.introduction,
        're_exam': paper.re_exam,
        'pass_score': paper.pass_score,
        'question': question,
        'count': question.count()  # 数据表中数据的条数
    }
    return render(request, 'exam.html', context=context)


# 显示考试成绩页面
def examinfo(request):
    # 若session认证为真
    if request.session.get('is_login', None):
        email = request.session.get('email', None)
        print(email)
        user = models.User.objects.filter(email=email)

        test_id = request.GET.get('test_id')
        user_exam_result = models.UserExam.objects.filter(test_id=test_id)
        # 查询考试结果
        exam_info = models.ExamInfo.objects.filter(userexam_id=user_exam_result.id)

        return render(request, 'examinfo.html', {'user': user, 'exam_info': exam_info})
    else:
        return render(request, 'examinfo.html')


# 交卷时自动计算考试成绩，并存入数据库
def calculate_grade(request):
    if request.method == 'POST':
        sid = request.POST.get('sid')
        subject1 = request.POST.get('subject')
        student = models.Student.objects.get(sid=sid)
        paper = models.TestPaper.objects.filter(major=student.major)
        grade = models.Record.objects.filter(sid=student.sid)
        course = models.Course.objects.filter(course_name=subject1).first()
        now = datetime.now()
        # 计算考试成绩
        questions = models.TestPaper.objects.filter(course__course_name=subject1). \
            values('pid').values('pid__id', 'pid__answer', 'pid__score')

        stu_grade = 0  # 初始化一个成绩
        for p in questions:
            qid = str(p['pid__id'])
        stu_ans = request.POST.get(qid)
        cor_ans = p['pid__answer']
        if stu_ans == cor_ans:
            stu_grade += p['pid__score']
        models.Record.objects.create(sid_id=sid, course_id=course.id, grade=stu_grade, rtime=now)
        context = {
            'student': student,
            'paper': paper,
            'grade': grade
        }
        return render(request, 'index.html', context=context)
