from django.contrib import admin
from .models import *
from import_export import resources
from import_export.formats.base_formats import XLSX
from import_export.admin import ImportExportModelAdmin
from django_admin_listfilter_dropdown.filters import DropdownFilter, RelatedDropdownFilter, ChoiceDropdownFilter, SimpleListFilter


# 修改名称
admin.site.site_header = '大数据资源招募考试系统平台'
admin.site.site_title = '大数据资源招募考试系统'

# Register your models here.

# admin.site.register(User, admin.ModelAdmin)
admin.site.register(UserInfo, admin.ModelAdmin)
admin.site.register(QuestionRadio, admin.ModelAdmin)
admin.site.register(QuestionCheckbox, admin.ModelAdmin)
admin.site.register(QuestionJudge, admin.ModelAdmin)
admin.site.register(QuestionText, admin.ModelAdmin)
admin.site.register(QuestionMedicine, admin.ModelAdmin)
admin.site.register(QuestionDiscuss, admin.ModelAdmin)
admin.site.register(QuestionAudio, admin.ModelAdmin)
# admin.site.register(TestPaper, admin.ModelAdmin)
# admin.site.register(QuestionBank, admin.ModelAdmin)
admin.site.register(Record, admin.ModelAdmin)
admin.site.register(UserExam, admin.ModelAdmin)
admin.site.register(ExamInfo, admin.ModelAdmin)

# admin.site.register([User, UserInfo, QuestionRadio, QuestionCheckbox, QuestionJudge, QuestionText, QuestionMedicine])
# admin.site.register([QuestionDiscuss, QuestionAudio, TestPaper, Record, UserExam, ExamInfo])


class UserResource(resources.ModelResource):
    # import 前进行的一些校验
    def before_import(self, dataset, using_transactions, dry_run, **kwargs):
        for row in dataset.dict:
            if len(str(row["pwd"])) < 6:
                raise Exception(f"密码不能少于8位,请检查 { str(row['pwd']) }")
        return dataset

    class Meta:
        model = User
        import_id_fields = ("username", "pwd", "email")
        fields = ("username", "pwd", "email")     # 导入的字段


class UserImportExportMixin(ImportExportModelAdmin):
    resource_class = UserResource

    def get_import_formats(self):
        return [XLSX]

    def get_export_formats(self):
        return [XLSX]


@admin.register(User)
class UserAdmin(UserImportExportMixin, admin.ModelAdmin, SimpleListFilter):
    template = 'django_admin_listfilter_dropdown/dropdown_filter.html'

    list_display = ["username", "pwd", "email"]

    # 右侧筛选列表
    # list_filter = ['username']
    list_filter = (
        ("username", DropdownFilter),
        ("email", ChoiceDropdownFilter),
    )
    # 模糊查询
    # search_fields = ["username", "email"]

    # def has_add_permission(self, request, obj=None):
    #     return False
    #
    # def has_delete_permission(self, request, obj=None):
    #     return False
    #
    # def has_change_permission(self, request, obj=None):
    #     return False


class CustomFilter(SimpleListFilter):
    template = 'django_admin_listfilter_dropdown/dropdown_filter.html'

    def lookups(self, request, model_admin):
        ...

    def queryset(self, request, queryset):
        ...

class TestPaperResource(resources.ModelResource):
    # import 前进行的一些校验
    def before_import(self, dataset, using_transactions, dry_run, **kwargs):
        for row in dataset.dict:
            if len(str(row["description"].replace(' ', ''))) < 1:
                raise Exception(f"简述不能为空,请检查 { str(row['description']) }")
            elif len(str(row["introduction"].replace(' ', ''))) < 1:
                raise Exception(f"简介不能为空,请检查 { str(row['introduction']) }")
            elif row["re_exam"] < 0 or type(row["re_exam"]) != int:
                raise Exception(f"重考次数不正确,需大于等于0且为整数,请检查 { str(row['re_exam']) }")
            elif row["is_active"] not in ['true', 'false']:
                raise Exception(f"是否启用不正确,只能为true或false,请检查 { str(row['is_active']) }")
            elif row["pass_score"] < 0:
                raise Exception(f"通过分数不正确,需大于等于0且为整数,请检查 { str(row['pass_score']) }")

        return dataset

    class Meta:
        model = TestPaper
        import_id_fields = ("description", "introduction", "re_exam", "extra_info", "is_active", "pass_score")
        fields = ("description", "introduction", "re_exam", "extra_info", "is_active", "pass_score")     # 导入的字段


class TestPaperImportExportMixin(ImportExportModelAdmin):
    resource_class = TestPaperResource

    def get_import_formats(self):
        return [XLSX]

    def get_export_formats(self):
        return [XLSX]


@admin.register(TestPaper)
class TestPaperAdmin(TestPaperImportExportMixin, admin.ModelAdmin):
    list_display = ["id", "description", "introduction", "re_exam", "extra_info", "is_active", "pass_score"]

    # 右侧筛选列表
    list_filter = ["re_exam", "is_active"]
    # 模糊查询
    search_fields = ["description", "introduction"]


class QuestionBankResource(resources.ModelResource):
    # import 前进行的一些校验
    def before_import(self, dataset, using_transactions, dry_run, **kwargs):
        for row in dataset.dict:
            if row["test_id"] < 1:
                raise Exception(f"试卷id不能小于1,请检查 { str(row['test_id']) }")
            elif row["question_id"] < 1:
                raise Exception(f"题目id不能小于1,请检查 { str(row['question_id']) }")
            elif row["order"] < 1:
                raise Exception(f"题目序号不能小于0,请检查 { str(row['order']) }")
            elif row["is_abandon"] not in ['true', 'false']:
                raise Exception(f"是否弃用只能为true或false,请检查 {str(row['is_abandon'])}")

        return dataset

    class Meta:
        model = QuestionBank
        import_id_fields = ("test_id", "question_id", "order", "is_abandon")
        fields = ("test_id", "question_id", "order", "is_abandon")     # 导入的字段


class QuestionBankImportExportMixin(ImportExportModelAdmin):
    resource_class = QuestionBankResource

    def get_import_formats(self):
        return [XLSX]

    def get_export_formats(self):
        return [XLSX]


@admin.register(QuestionBank)
class QuestionBankAdmin(TestPaperImportExportMixin, admin.ModelAdmin):
    list_display = ["id", "test_id", "question_id", "order", "is_abandon"]

    # 右侧筛选列表
    list_filter = ["id"]
    # list_filter = (
    #     # for ordinary fields
    #     ('id', DropdownFilter),
    #     # # for choice fields
    #     # ('question_id', ChoiceDropdownFilter),
    #     # # for related fields
    #     # ('is_abandon', RelatedDropdownFilter),
    # )

    # 模糊查询
    search_fields = ["test_id", "question_id"]
