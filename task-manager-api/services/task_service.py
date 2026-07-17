from database import db
from models.task import Task
from models.user import User
from models.category import Category
from datetime import datetime, timezone

class TaskService:
    @staticmethod
    def get_all_tasks():
        tasks = Task.query.all()
        result = []
        for t in tasks:
            task_data = t.to_dict()
            task_data['overdue'] = t.is_overdue()
            task_data['user_name'] = User.query.get(t.user_id).name if t.user_id else None
            task_data['category_name'] = Category.query.get(t.category_id).name if t.category_id else None
            result.append(task_data)
        return result

    @staticmethod
    def get_task_by_id(task_id):
        task = Task.query.get(task_id)
        if not task:
            return None
        data = task.to_dict()
        data['overdue'] = task.is_overdue()
        return data

    @staticmethod
    def create_task(data):
        title = data.get('title')
        if not title or len(title) < 3 or len(title) > 200:
            raise ValueError("Título inválido")
        
        task = Task(
            title=title,
            description=data.get('description', ''),
            status=data.get('status', 'pending'),
            priority=data.get('priority', 3),
            user_id=data.get('user_id'),
            category_id=data.get('category_id')
        )
        if data.get('due_date'):
            task.due_date = datetime.strptime(data['due_date'], '%Y-%m-%d')
        if data.get('tags'):
            task.tags = ','.join(data['tags']) if isinstance(data['tags'], list) else data['tags']
            
        db.session.add(task)
        db.session.commit()
        return task

    @staticmethod
    def update_task(task_id, data):
        task = Task.query.get(task_id)
        if not task:
            return None
            
        if 'title' in data:
            task.title = data['title']
        if 'description' in data:
            task.description = data['description']
        if 'status' in data:
            task.status = data['status']
        if 'priority' in data:
            task.priority = data['priority']
        if 'due_date' in data:
            task.due_date = datetime.strptime(data['due_date'], '%Y-%m-%d') if data['due_date'] else None
        
        task.updated_at = datetime.utcnow()
        db.session.commit()
        return task

    @staticmethod
    def delete_task(task_id):
        task = Task.query.get(task_id)
        if not task:
            return False
        db.session.delete(task)
        db.session.commit()
        return True

    @staticmethod
    def search_tasks(query_params):
        tasks = Task.query
        if 'q' in query_params:
            tasks = tasks.filter(Task.title.like(f"%{query_params['q']}%") | Task.description.like(f"%{query_params['q']}%"))
        if 'status' in query_params:
            tasks = tasks.filter(Task.status == query_params['status'])
        
        return [t.to_dict() for t in tasks.all()]

    @staticmethod
    def get_stats():
        all_tasks = Task.query.all()
        total = len(all_tasks)
        done = len([t for t in all_tasks if t.status == 'done'])
        
        return {
            'total': total,
            'pending': len([t for t in all_tasks if t.status == 'pending']),
            'done': done,
            'overdue': len([t for t in all_tasks if t.is_overdue()]),
            'completion_rate': round((done / total) * 100, 2) if total > 0 else 0
        }
