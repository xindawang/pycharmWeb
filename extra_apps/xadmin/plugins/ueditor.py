# # -*- coding:utf8 -*-
#
# import xadmin
# from xadmin.views import BaseAdminPlugin, CreateAdminView, DetailAdminView, UpdateAdminView
# from DjangoUeditor.models import UEditorField
# from DjangoUeditor.widgets import UEditorWidget
# from django.conf import settings
#
# class XadminUEditorWidget(UEditorWidget):
#     def __init__(self,**kwargs):
#         self.ueditor_options=kwargs
#         self.Media.js = None
#         super(XadminUEditorWidget,self).__init__(kwargs)
#
# class UeditorPlugin(BaseAdminPlugin):
#
#     def get_field_style(self, attrs, db_field, style, **kwargs):
#         if style == 'ueditor':
#             if isinstance(db_field, UEditorField):
#                 widget = db_field.formfield().widget
#                 param = {}
#                 param.update(widget.ueditor_settings)
#                 param.update(widget.attrs)
#                 return {'widget': XadminUEditorWidget(**param)}
#         return attrs
#
#     def block_extrahead(self, context, nodes):
#         js = '<script type="text/javascript" src="%s"></script>' % (settings.STATIC_URL + "ueditor/ueditor.config.js")
#         js += '<script type="text/javascript" src="%s"></script>' % (settings.STATIC_URL + "ueditor/ueditor.all.min.js")
#         nodes.append(js)
#
# xadmin.site.register_plugin(UeditorPlugin, UpdateAdminView)
# xadmin.site.register_plugin(UeditorPlugin, CreateAdminView)


# -*- coding:utf8 -*-

import xadmin
from xadmin.views import BaseAdminPlugin, CreateAdminView, DetailAdminView, UpdateAdminView
from WangEditor.models import WangEditorField
from WangEditor.widgets import WangEditorWidget
from django.conf import settings

class XadminWangEditorWidget(WangEditorWidget):
    def __init__(self,**kwargs):
        self.WangEditor_options=kwargs
        # self.Media.js = None
        super(XadminWangEditorWidget,self).__init__(kwargs)

class WangEditorPlugin(BaseAdminPlugin):

    def get_field_style(self, attrs, db_field, style, **kwargs):
        if style == 'WangEditor':
            if isinstance(db_field, WangEditorField):
                # widget = db_field.formfield().widget
                # param = {}
                # param.update(widget.WangEditor_settings)
                # param.update(widget.attrs)
                return {'widget': XadminWangEditorWidget()}
        return attrs

    # def block_extrahead(self, context, nodes):
    #     js = '<script type="text/javascript" src="%s"></script>' % (settings.STATIC_URL + "editor/js/wangEditor.js")
    #     js += '<script type="text/javascript" src="%s"></script>' % (settings.STATIC_URL + "editor/js/lib/jquery-1.10.2.min.js")
    #     nodes.append(js)

xadmin.site.register_plugin(WangEditorPlugin, UpdateAdminView)
xadmin.site.register_plugin(WangEditorPlugin, CreateAdminView)
