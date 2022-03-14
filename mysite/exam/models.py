from django.db import models


# Create your models here.


# 存储用户信息
# 用户名和email唯一+
class User(models.Model):
    username = models.CharField('用户名', max_length=20, unique=True)
    pwd = models.CharField('密码', max_length=15)
    email = models.EmailField('邮箱', unique=True)  # 默认为空 唯一值

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '用户信息表'

    def __str__(self):
        return self.email


GENDER_LIST = ["Male", "Female"]
AGE_LIST = ["0-18", "18-25", "26-30", "31-35", "36-40", "41-45", "46-50", "51-55", "56-60"]


class UserInfo(models.Model):
    gender = models.CharField('性别', choices=[(x, x) for x in GENDER_LIST], max_length=10)
    age = models.IntegerField('年龄', choices=[(x, x) for x in GENDER_LIST])
    work_time = models.CharField('可工作时间', max_length=20)
    lang = models.CharField('熟悉语种', null=True, max_length=20)
    subject = models.CharField('熟悉领域', null=True, max_length=20)

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '详细信息表'

    def __str__(self):
        return self.work_time


# 题目表 有：题目描述、题目id、题目答案、附带信息
class Question(models.Model):
    question = models.CharField('题目描述', max_length=150)
    answer = models.CharField('答案', max_length=50)
    score = models.IntegerField('分值')
    type = models.CharField('题目类型', choices=(('单选', '单选'), ('多选', '多选'), ('判断', '判断'), ('文本资源评测', '文本资源评测'),
                                             ('医学标注资源评测', '医学资源评测'), ('文本听写', '文本听写')), max_length=40)

    class Meta:
        abstract = True  # 抽象类，只用作继承用，不会生成表

    def __str__(self):
        return self.question


# 根据题目类型 一个题目类型就是一个class
# 单选题型
class QuestionRadio(Question):
    a = models.CharField('A选项', max_length=20)
    b = models.CharField('B选项', max_length=20)
    c = models.CharField('C选项', max_length=20)
    d = models.CharField('D选项', max_length=20)

    class Meta:
        verbose_name = '单选'
        verbose_name_plural = '单选题型'


# 多选题型
class QuestionCheckbox(Question):
    a = models.CharField('A选项', max_length=20)
    b = models.CharField('B选项', max_length=20)
    c = models.CharField('C选项', max_length=20)
    d = models.CharField('D选项', max_length=20)
    e = models.CharField('E选项', max_length=20)

    class Meta:
        verbose_name = '多选'
        verbose_name_plural = '多选题型'


# 判断题型
class QuestionJudge(Question):
    choice = models.CharField('T|F', choices=(('True', 'True'), ('False', 'False')), max_length=40)

    class Meta:
        verbose_name = '判断'
        verbose_name_plural = '判断题型'


# 文本资源评测
class QuestionText(Question):
    choice = models.CharField('T|F', choices=(('True', 'True'), ('False', 'False')), max_length=40)

    class Meta:
        verbose_name = '文本'
        verbose_name_plural = '文本资源评测'


# 判断题型
class QuestionJudge(Question):
    choice = models.CharField('T|F', choices=(('True', 'True'), ('False', 'False')), max_length=40)

    class Meta:
        verbose_name = '判断'
        verbose_name_plural = '判断题型'


# 判断题型
class QuestionJudge(Question):
    choice = models.CharField('T|F', choices=(('True', 'True'), ('False', 'False')), max_length=40)

    class Meta:
        verbose_name = '判断'
        verbose_name_plural = '判断题型'


# 试卷表 有：描述、简介、重考次数、附带信息
class TestPaper(models.Model):
    description = models.CharField('简述', max_length=30)
    introduction = models.CharField('简介', max_length=200)
    re_exam = models.IntegerField(default=0)
    extra_info = models.CharField(max_length=100, null=True, default=None)

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间", null=True, blank=True)

    class Meta:
        verbose_name = '试卷'
        verbose_name_plural = '试卷表'

    def __str__(self):
        return self.description


# 题库表 有：试卷id、题目id
class QestionBank(models.Model):
    test_id = models.IntegerField('试卷id')
    question_id = models.IntegerField('题目id')
    is_abandon = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间", null=True, blank=True)

    class Meta:
        verbose_name = '题库'
        verbose_name_plural = '题库表，存储试卷所有的题目'

    def __str__(self):
        return self.test_id
