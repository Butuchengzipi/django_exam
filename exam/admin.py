from django.contrib import admin
from .models import *
from import_export import resources
from import_export.formats.base_formats import XLSX
from import_export.admin import ImportExportModelAdmin

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


class TextInfoResource(resources.ModelResource):
    # import 前进行的一些校验
    def before_import(self, dataset, using_transactions, dry_run, **kwargs):
        for row in dataset.dict:
            if str(row["project_id"]) not in PROJECT_IDS:
                raise Exception(f"存在错误的project_id,请检查 { str(row['project_id']) }")
        return dataset

    class Meta:
        model = TextInfo
        import_id_fields = ("code", "corpus")
        fields = ("project_id", "code", "corpus")     # 导入的字段


class TextInfoImportExportMixin(ImportExportModelAdmin):

    resource_class = TextInfoResource

    def get_import_formats(self):
        return [XLSX]

    def get_export_formats(self):
        return [XLSX]


@admin.register(TextInfo)
class TextInfoAdmin(TextInfoImportExportMixin, admin.ModelAdmin):
    list_display = ["project_id", "code", "corpus", "created_at", "updated_at"]

    # 右侧筛选列表
    list_filter = ['project_id']
    # 模糊查询
    search_fields = ["code", "corpus"]

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False
