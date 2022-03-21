from django.shortcuts import render
import models

# Create your views here.


# 用户登录
def UserLogin(request):
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
            paper = models.TestPaper.objects.filter(major=student.major)
            # 查询成绩信息
            grade = models.Record.objects.filter(sid=student.sid)

            # 渲染index模板
            return render(request, 'index.html', {'student': student, 'paper': paper, 'grade': grade})
        else:
            return render(request, 'login.html', {'message': '密码不正确'})
    elif request.method == 'GET':
        return render(request, 'login.html')
    else:
        return HttpResponse("请使用GET或POST请求数据")
