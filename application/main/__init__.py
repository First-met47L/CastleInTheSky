from flask import Blueprint
from ..models import Permission

main = Blueprint ('main', __name__)

from . import errors, forms, views


@main.app_context_processor
def inject_permissions():
    '''
    在模板中可能也需要检查权限,所以 Permission 类为所有位定义了常量以便于获取。为了
    避免每次调用 render_template() 时都多添加一个模板参数,可以使用上下文处理器。上
    下文处理器能让变量在所有模板中全局可访问
    :return: a dict object
    '''
    return dict (Permission=Permission)
