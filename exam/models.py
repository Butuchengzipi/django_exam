from django.db import models


# Create your models here.


# 存储用户信息
# 用户名和email唯一+
class User(models.Model):
    id = models.AutoField('序号', primary_key=True)
    username = models.CharField('用户名', max_length=20, unique=True)
    pwd = models.CharField('密码', max_length=15)
    email = models.EmailField('邮箱', unique=True)  # 默认为空 唯一值

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '用户信息表'

    def __str__(self):
        return self.email, self.username, self.id


GENDER_LIST = ["Male", "Female"]
AGE_LIST = ["0-18", "18-25", "26-30", "31-35", "36-40", "41-45", "46-50", "51-55", "56-60"]


class UserInfo(models.Model):
    id = models.AutoField('序号', primary_key=True)
    user_id = models.IntegerField('用户id')
    gender = models.CharField('性别', choices=[(x, x) for x in GENDER_LIST], max_length=10)
    age = models.IntegerField('年龄', choices=[(x, x) for x in GENDER_LIST])
    work_time = models.CharField('可工作时间', max_length=20)
    lang = models.CharField('熟悉语种', null=True, max_length=20)
    subject = models.CharField('熟悉领域', null=True, max_length=20)

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '详细信息表'

    def __str__(self):
        return self.user_id


# 题目表 有：题目描述、题目id、题目答案、附带信息
class Question(models.Model):
    id = models.AutoField('序号', primary_key=True)
    question = models.CharField('题目描述', max_length=100)
    answer = models.CharField('答案', max_length=50)
    score = models.IntegerField('分值')
    type = models.CharField('题目类型', choices=(('单选', '单选'), ('多选', '多选'), ('判断', '判断'), ('文本资源评测', '文本资源评测'),
                                             ('医学标注资源评测', '医学资源评测'), ('文本听写', '文本听写')), max_length=40)

    class Meta:
        abstract = True  # 抽象类，只用作继承用，不会生成表

    def __str__(self):
        return self.question, self.answer, self.score, self.type


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

    def __str__(self):
        return self.choice


# 文本资源评测（变形多选，按比例得分）
class QuestionText(Question):
    a = models.CharField('A选项', max_length=20)
    b = models.CharField('B选项', max_length=20)
    c = models.CharField('C选项', max_length=20)
    d = models.CharField('D选项', max_length=20)
    e = models.CharField('E选项', max_length=20)
    f = models.CharField('F选项', max_length=20)
    g = models.CharField('G选项', max_length=20)
    h = models.CharField('H选项', max_length=20)

    class Meta:
        verbose_name = '文本'
        verbose_name_plural = '文本资源评测'


# 医学资源评测（变形单选，下拉框实现）
class QuestionMedicine(Question):
    a = models.CharField('A选项', max_length=20)
    b = models.CharField('B选项', max_length=20)
    c = models.CharField('C选项', max_length=20)

    class Meta:
        verbose_name = '医学'
        verbose_name_plural = '医学资源评测'


# 论述题型
class QuestionDiscuss(Question):
    brief = models.CharField('简介', max_length=150)

    class Meta:
        verbose_name = '论述'
        verbose_name_plural = '论述题型'

    def __str__(self):
        return self.brief


# 文本听写  根据音频转写文本
class QuestionAudio(Question):
    audio_url = models.CharField('音频链接', max_length=150)

    class Meta:
        verbose_name = '音频'
        verbose_name_plural = '音频转写题型'

    def __str__(self):
        return self.audio_url


# 试卷表 有：描述、简介、重考次数、附带信息
class TestPaper(models.Model):
    id = models.AutoField('序号', primary_key=True)
    description = models.CharField('简述', max_length=30)
    introduction = models.CharField('简介', max_length=200)
    re_exam = models.IntegerField(default=0)
    extra_info = models.CharField(max_length=100, null=True, default=None)

    # 是否活跃
    is_active = models.BooleanField(null=False, default=False)
    pass_score = models.IntegerField('通过分数', default=0)

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间", null=True, blank=True)

    class Meta:
        verbose_name = '试卷'
        verbose_name_plural = '试卷表'

    def __str__(self):
        return self.description, self.introduction


# 题库表 有：试卷id、题目id
class QuestionBank(models.Model):
    id = models.AutoField('序号', primary_key=True)
    test_id = models.IntegerField('试卷id')
    question_id = models.IntegerField('题目id')
    order = models.IntegerField()
    is_abandon = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间", null=True, blank=True)

    class Meta:
        verbose_name = '题库'
        verbose_name_plural = '题库表'

    def __str__(self):
        return self.test_id, self.question_id, self.order


# 考试记录表
class Record(models.Model):
    id = models.AutoField('序号', primary_key=True)

    # 记录用户的每一次考试的每一道题
    user_id = models.IntegerField('用户id')
    test_id = models.IntegerField('试卷id')
    question_id = models.IntegerField('题目id')

    user_answer = models.TextField('用户答案')
    user_score = models.IntegerField('用户得分')

    exam_batch = models.IntegerField('考试批次')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间", null=True, blank=True)

    class Meta:
        verbose_name = '考试记录'
        verbose_name_plural = '考试记录表'

    def __str__(self):
        return self.test_id, self.question_id, self.user_id, self.user_score


# 用户考试表
class UserExam(models.Model):
    id = models.AutoField('序号', primary_key=True)

    user_id = models.IntegerField('用户id')
    test_id = models.IntegerField('试卷id')

    class Meta:
        verbose_name = '用户考试'
        verbose_name_plural = '用户考试表'
        unique_together = ('user_id', 'test_id')

    def __str__(self):
        return self.user_id, self.test_id, self.id


# 考试信息表
class ExamInfo(models.Model):
    id = models.AutoField('序号', primary_key=True)

    # 记录用户的每一次考试的每一道题
    userexam_id = models.IntegerField('用户考试id', unique=True)
    exam_score = models.IntegerField('用户总得分')
    total_score = models.IntegerField('试卷总分')
    remark = models.CharField('备注', max_length=100)
    exam_time = models.IntegerField('考试次数')
    is_pass = models.BooleanField('是否通过', default=False)

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间", null=True, blank=True)

    class Meta:
        verbose_name = '考试信息'
        verbose_name_plural = '考试信息表'

    def __str__(self):
        return self.userexam_id, self.exam_score, self.total_score, self.is_pass
