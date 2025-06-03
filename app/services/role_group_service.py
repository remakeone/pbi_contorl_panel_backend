from app.models.role_group import RoleGroup
from app.models.user import User
from app.models.report import Report
from app import db

class RoleGroupService:
    """
    角色组服务类
    处理角色组相关的业务逻辑
    """
    
    @staticmethod
    def get_all_role_groups():
        """
        获取所有角色组
        
        Returns:
            list: 角色组对象列表
        """
        return RoleGroup.query.all()
    
    @staticmethod
    def get_role_group_by_id(group_id):
        """
        根据ID获取角色组
        
        Args:
            group_id: 角色组ID
            
        Returns:
            RoleGroup: 角色组对象
            
        Raises:
            404: 如果角色组不存在
        """
        return RoleGroup.query.get_or_404(group_id)
    
    @staticmethod
    def create_role_group(data):
        """
        创建新角色组
        
        Args:
            data: 角色组数据字典
            
        Returns:
            RoleGroup: 创建的角色组对象
            
        Raises:
            ValueError: 如果角色组名称已存在
        """
        if RoleGroup.query.filter_by(name=data['name']).first():
            raise ValueError("角色组名称已存在")
            
        role_group = RoleGroup(
            name=data['name'],
            description=data.get('description', '')
        )
        db.session.add(role_group)
        db.session.commit()
        return role_group
    
    @staticmethod
    def update_role_group(group_id, data):
        """
        更新角色组信息
        
        Args:
            group_id: 角色组ID
            data: 角色组数据字典
            
        Returns:
            RoleGroup: 更新后的角色组对象
            
        Raises:
            404: 如果角色组不存在
            ValueError: 如果角色组名称已存在
        """
        role_group = RoleGroup.query.get_or_404(group_id)
        
        if 'name' in data and data['name'] != role_group.name:
            if RoleGroup.query.filter_by(name=data['name']).first():
                raise ValueError("角色组名称已存在")
            role_group.name = data['name']
            
        if 'description' in data:
            role_group.description = data['description']
            
        db.session.commit()
        return role_group
    
    @staticmethod
    def delete_role_group(group_id):
        """
        删除角色组
        
        Args:
            group_id: 角色组ID
            
        Raises:
            404: 如果角色组不存在
        """
        role_group = RoleGroup.query.get_or_404(group_id)
        db.session.delete(role_group)
        db.session.commit()
    
    @staticmethod
    def get_group_users(group_id):
        """
        获取角色组下的所有用户
        
        Args:
            group_id: 角色组ID
            
        Returns:
            list: 用户对象列表
            
        Raises:
            404: 如果角色组不存在
        """
        role_group = RoleGroup.query.get_or_404(group_id)
        return role_group.users
    
    @staticmethod
    def add_users_to_group(group_id, user_ids):
        """
        添加用户到角色组
        
        Args:
            group_id: 角色组ID
            user_ids: 用户ID列表
            
        Raises:
            404: 如果角色组不存在
        """
        role_group = RoleGroup.query.get_or_404(group_id)
        users = User.query.filter(User.id.in_(user_ids)).all()
        
        for user in users:
            if user not in role_group.users:
                role_group.users.append(user)
                
        db.session.commit()
    
    @staticmethod
    def remove_user_from_group(group_id, user_id):
        """
        从角色组中移除用户
        
        Args:
            group_id: 角色组ID
            user_id: 用户ID
            
        Raises:
            404: 如果角色组或用户不存在
        """
        role_group = RoleGroup.query.get_or_404(group_id)
        user = User.query.get_or_404(user_id)
        
        if user in role_group.users:
            role_group.users.remove(user)
            db.session.commit()
    
    @staticmethod
    def get_group_visible_reports(group_id):
        """
        获取角色组可见的所有报表
        
        Args:
            group_id: 角色组ID
            
        Returns:
            list: 报表对象列表
            
        Raises:
            404: 如果角色组不存在
        """
        role_group = RoleGroup.query.get_or_404(group_id)
        return role_group.visible_reports
    
    @staticmethod
    def add_reports_to_group(group_id, report_ids):
        """
        添加报表到角色组可见列表
        
        Args:
            group_id: 角色组ID
            report_ids: 报表ID列表
            
        Raises:
            404: 如果角色组不存在
        """
        role_group = RoleGroup.query.get_or_404(group_id)
        reports = Report.query.filter(Report.id.in_(report_ids)).all()
        
        for report in reports:
            if report not in role_group.visible_reports:
                role_group.visible_reports.append(report)
                
        db.session.commit()
    
    @staticmethod
    def remove_report_from_group(group_id, report_id):
        """
        从角色组可见列表中移除报表
        
        Args:
            group_id: 角色组ID
            report_id: 报表ID
            
        Raises:
            404: 如果角色组或报表不存在
        """
        role_group = RoleGroup.query.get_or_404(group_id)
        report = Report.query.get_or_404(report_id)
        
        if report in role_group.visible_reports:
            role_group.visible_reports.remove(report)
            db.session.commit()
    
    @staticmethod
    def get_reports_not_in_group(group_id):
        """
        获取不在角色组可见列表中的所有报表
        
        Args:
            group_id: 角色组ID
            
        Returns:
            list: 报表对象列表
            
        Raises:
            404: 如果角色组不存在
        """
        role_group = RoleGroup.query.get_or_404(group_id)
        visible_report_ids = [report.id for report in role_group.visible_reports]
        
        if visible_report_ids:
            return Report.query.filter(Report.id.notin_(visible_report_ids)).all()
        else:
            return Report.query.all()
    
    @staticmethod
    def set_group_visible_reports(group_id, report_ids):
        """
        设置角色组可见的报表列表（替换当前所有可见报表）
        
        Args:
            group_id: 角色组ID
            report_ids: 报表ID列表
            
        Raises:
            404: 如果角色组不存在
        """
        role_group = RoleGroup.query.get_or_404(group_id)
        reports = Report.query.filter(Report.id.in_(report_ids)).all()
        
        # 清空当前可见报表列表
        role_group.visible_reports = []
        
        # 添加新的可见报表
        for report in reports:
            role_group.visible_reports.append(report)
            
        db.session.commit()
        
        return role_group.visible_reports 