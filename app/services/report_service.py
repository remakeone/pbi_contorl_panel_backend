from app.models.report import Report
from app.models.tag import Tag  # 新增导入
from app import db
from flask_login import current_user
from sqlalchemy.orm import joinedload  # 新增导入


class ReportService:
    """
    报表服务类
    处理报表相关的业务逻辑
    """
    
    @staticmethod
    def get_all_reports():
        """
        获取当前用户有权限查看的所有报表

        Returns:
            list: 用户有权限查看的报表对象列表
        """
        all_reports = Report.query.all()
        # print(all_reports)
        result = []
        for report in all_reports:  # 遍历所有报表, 检查用户权限
            # logger.info(f"当前处理的报表: {report}")
            # logger.info(f"当前用户角色: {current_user.role if current_user.is_authenticated else '未认证'}")

            if current_user.is_authenticated and current_user.role == 'admin':
                pass

            elif current_user.is_authenticated and current_user.role == 'editor':
                pass

            else:
                if not report.is_active or report.is_hide_report:
                    continue
            report_dict = report.to_dict()
            report_dict['is_view'] = current_user.can_view_report(report)
            result.append(report_dict)

        return result

    @staticmethod
    def get_report_by_id(report_id):
        """
        根据ID获取报表
        
        Args:
            report_id: 报表ID
            
        Returns:
            Report: 报表对象
            
        Raises:
            404: 如果报表不存在
        """
        return Report.query.filter_by(id=report_id).first_or_404()
    
    @staticmethod
    def create_report(data):
        """
        创建新报表

        Args:
            data: 报表数据字典

        Returns:
            Report: 创建的报表对象
        """
        if 'powerbi_id' not in data:
            raise ValueError("powerbi_id为空")
        # 处理标签数据
        tags = data.pop('tags', [])
        report = Report(**data)

        # 添加标签关联（新增部分）
        if tags:
            existing_tags = Tag.query.filter(Tag.name.in_(tags)).all()
            new_tags = [Tag(name=name) for name in tags if name not in {t.name for t in existing_tags}]
            report.tags.extend(existing_tags + new_tags)

        db.session.add(report)
        db.session.commit()
        return report
    
    @staticmethod
    def update_report(report_id, data):
        """
        更新报表信息

        Args:
            report_id: 报表ID
            data: 报表数据字典

        Returns:
            Report: 更新后的报表对象

        Raises:
            404: 如果报表不存在
        """
        report = Report.query.get_or_404(report_id)
        tags = data.pop('tags', None)

        # 处理标签更新（新增代码）
        if tags is not None:
            # 获取当前标签集合
            current_tags = {tag.name for tag in report.tags}
            new_tags = set(tags)

            # 添加新增标签
            for tag_name in new_tags - current_tags:
                tag = Tag.query.filter_by(name=tag_name).first()
                if not tag:
                    tag = Tag(name=tag_name)
                    db.session.add(tag)
                report.tags.append(tag)

            # 移除不再存在的标签
            for tag in list(report.tags):
                if tag.name in current_tags - new_tags:
                    report.tags.remove(tag)

        # 原有字段更新逻辑保持不变
        for key, value in data.items():
            if key == 'powerbi_id' and not value:
                continue
            if hasattr(report, key):
                setattr(report, key, value)

        db.session.commit()
        return report
    
    @staticmethod
    def delete_report(report_id):
        """
        删除报表（软删除）
        
        Args:
            report_id: 报表ID
            
        Raises:
            404: 如果报表不存在
        """
        report = Report.query.get_or_404(report_id)
        # 软删除，只将is_active设为False
        report.is_active = False
        db.session.commit()
        
    @staticmethod
    def hard_delete_report(report_id):
        """
        硬删除报表（从数据库中删除）
        
        Args:
            report_id: 报表ID
            
        Raises:
            404: 如果报表不存在
        """
        report = Report.query.get_or_404(report_id)
        db.session.delete(report)
        db.session.commit()

    @staticmethod
    def get_all_tags():
        """
        获取系统所有标签
        Returns:
            list: 标签对象列表
        """
        return Tag.query.all()

    @staticmethod
    def add_tags_to_report(report_id, tag_names):
        """
        为报表添加标签
        Args:
            report_id: 报表ID
            tag_names: 标签名称列表
        """
        report = Report.query.get_or_404(report_id)
        existing_tags = Tag.query.filter(Tag.name.in_(tag_names)).all()

        # 创建不存在的标签
        existing_tag_names = {t.name for t in existing_tags}
        new_tags = [Tag(name=name) for name in tag_names if name not in existing_tag_names]

        # 批量添加关联
        report.tags.extend(existing_tags + new_tags)
        db.session.commit()

    @staticmethod
    def remove_tags_from_report(report_id, tag_names):
        """
        从报表移除标签
        Args:
            report_id: 报表ID
            tag_names: 要移除的标签名称列表
        """
        report = Report.query.options(joinedload(Report.tags)).get_or_404(report_id)
        tags_to_remove = [t for t in report.tags if t.name in tag_names]

        # 移除关联关系
        for tag in tags_to_remove:
            report.tags.remove(tag)
        db.session.commit()

    @staticmethod
    def get_reports_by_tag(tag_name):
        """
        根据标签名称获取报表
        Args:
            tag_name: 标签名称
        Returns:
            list: 报表对象列表
        """
        return Report.query.join(Report.tags).filter(Tag.name == tag_name).all()

