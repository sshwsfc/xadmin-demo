from django.conf import settings
import xadmin
from models import *
from xadmin.layout import *

from xadmin.plugins.inline import Inline
from xadmin.plugins.batch import BatchChangeAction

from django.contrib.comments.models import Comment

class MaintainInline(object):
    model = MaintainLog
    extra = 0
    style = 'accordion'

class IDCAdmin(object):
    list_display = ('name', 'description', 'create_time')
    list_display_links = ('name',)
    wizard_form_list = [
        ('Frist\'s Form', ('name', 'description')),
        ('Seocnd Form', ('contact', 'telphone', 'address')),
        ('Thread Form', ('customer_id',))
    ]

    search_fields = ['name']
    relfield_style = 'fk-ajax'
    reversion_enable = True

    actions = [BatchChangeAction,]
    batch_fields = ('contact', )
    
class CommentInline(object):
    generic_inline = True
    ct_fk_field = "object_pk"
    model = Comment
    extra = 1
    style = 'tab'

class HostAdmin(object):
    def open_web(self, instance):
        return "<a href='http://%s' target='_blank'>Open</a>" % instance.ip
    open_web.short_description = "Acts"
    open_web.allow_tags = True
    open_web.is_column = True

    def thumbnail_img(self, obj):
        return "<img src='http://js.wiyun.com/site_media/images/wallpaper/eac1bce7-90d5-40a7-a7e2-ae02acca2e86_jpg_152x102_crop_upscale_q85.jpg'/>"
    thumbnail_img.short_description = "TImg"
    thumbnail_img.allow_tags = True
    thumbnail_img.is_column = True
    thumbnail_img.thumbnail_img = True

    list_display = ('thumbnail_img', 'name', 'idc', 'guarantee_date', 'service_type', 'status', 'open_web', 'description')
    list_display_links = ('name',)
    grid_layouts = ['thumbnails', 'table']

    raw_id_fields = ('idc',)
    style_fields = {'system': "radio-inline"}

    search_fields = ['name', 'ip', 'description']
    list_filter = ['idc', 'guarantee_date', 'status', 'brand', 'model', 'cpu', 'core_num', 'hard_disk', 'memory', 'service_type']

    list_bookmarks = [{'title': "Need Guarantee", 'query': {'status__exact': 2}, 'order': ('-guarantee_date',), 'cols': ('brand', 'guarantee_date', 'service_type')}]

    show_detail_fields = ('idc',)
    list_editable = ('name', 'idc', 'guarantee_date', 'service_type', 'description')
    save_as = True
    
    #aggregate_fields = {"guarantee_date": "min"}
    
    actions = [BatchChangeAction,]
    batch_fields = ('name', 'idc', 'guarantee_date', 'service_type', 'status', 'description', 'system')

    form_layout = (
        Main(
            TabHolder(
                Tab('Comm Fiels',
                    Fieldset('Company data',
                        'name', 'idc',
                        description="some comm fields, required"
                    ),
                    Inline(MaintainLog),
                ),
                Tab('Extend Fiedls',
                    Fieldset('Contact details',
                        'service_type',
                        Row('brand', 'model'),
                        Row('cpu', 'core_num'),
                        Row(AppendedText('hard_disk', 'G'), AppendedText('memory', "G")),
                        'guarantee_date'
                    ),
                ),
                Tab('Comments',
                    Inline(Comment),
                ),
            ),
        ),
        Side(
            Fieldset('Status data',
                'status', 'ssh_port', 'ip'
            ),
        )
    )
    inlines = [MaintainInline, CommentInline]
    reversion_enable = True
    
class HostGroupAdmin(object):
    list_display = ('name', 'description')
    list_display_links = ('name',)

    search_fields = ['name']
    style_fields = {'hosts': 'checkbox-inline'}

class MaintainLogAdmin(object):
    list_display = ('host', 'maintain_type', 'hard_type', 'time', 'operator', 'note')
    list_display_links = ('host',)

    list_filter = ['host', 'maintain_type', 'hard_type', 'time', 'operator']
    search_fields = ['note']

    form_layout = (
        Col("col2", 
            Fieldset('Record data',
                'time', 'note',
                css_class='unsort short_label no_title'
            ),
            span=9, horizontal=True
        ),
        Col("col1",
            Fieldset('Comm data',
                'host', 'maintain_type'
            ),
            Fieldset('Maintain details',
                'hard_type', 'operator'
            ),
            span=3
        )
    )
    reversion_enable = True

class AccessRecordAdmin(object):
    def avg_count(self, instance):
        return int(instance.view_count/instance.user_count)
    avg_count.short_description = "Avg Count"
    avg_count.allow_tags = True
    avg_count.is_column = True

    list_display = ('date', 'user_count', 'view_count', 'avg_count')
    list_display_links = ('date',)

    list_filter = ['date', 'user_count', 'view_count']
    actions = None
    aggregate_fields = {"user_count": "sum", 'view_count': "sum"}

    refresh_times = (3, 5, 10)
    data_charts = {
        "user_count": {'title': u"User Report", "x-field": "date", "y-field": ("user_count", "view_count"), "order": ('date',)},
        "avg_count": {'title': u"Avg Report", "x-field": "date", "y-field": ('avg_count',), "order": ('date',)}
    }

xadmin.site.register(Host, HostAdmin)
xadmin.site.register(HostGroup, HostGroupAdmin)
xadmin.site.register(MaintainLog, MaintainLogAdmin)
xadmin.site.register(IDC, IDCAdmin)
xadmin.site.register(AccessRecord, AccessRecordAdmin)
