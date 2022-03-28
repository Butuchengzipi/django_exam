from django.contrib import admin
from .models import *

# 修改名称
admin.site.site_header = '大数据资源招募考试系统平台'
admin.site.site_title = '大数据资源招募考试系统'

# Register your models here.
admin.site.register(User, admin.ModelAdmin)
admin.site.register(UserInfo, admin.ModelAdmin)
admin.site.register(QuestionRadio, admin.ModelAdmin)
admin.site.register(QuestionCheckbox, admin.ModelAdmin)
admin.site.register(QuestionJudge, admin.ModelAdmin)
admin.site.register(QuestionText, admin.ModelAdmin)
admin.site.register(QuestionMedicine, admin.ModelAdmin)
admin.site.register(QuestionDiscuss, admin.ModelAdmin)
admin.site.register(QuestionAudio, admin.ModelAdmin)
admin.site.register(TestPaper, admin.ModelAdmin)
admin.site.register(QuestionBank, admin.ModelAdmin)
admin.site.register(Record, admin.ModelAdmin)
admin.site.register(UserExam, admin.ModelAdmin)
admin.site.register(ExamInfo, admin.ModelAdmin)

# admin.site.register([User, UserInfo, QuestionRadio, QuestionCheckbox, QuestionJudge, QuestionText, QuestionMedicine])
# admin.site.register([QuestionDiscuss, QuestionAudio, TestPaper, Record, UserExam, ExamInfo])
