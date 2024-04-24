from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import sqlalchemy

app = Flask(__name__)
CORS(app, origins=['http://localhost:5173', 'http://www.marcotang.online', 'http://marcotang.online'])

# 配置数据库连接字符串和连接池参数
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Marcool520@localhost/mydatabase'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_size': 10,
    'max_overflow': 5,
    'pool_timeout': 30,
    'pool_recycle': 3600
}

# 初始化 SQLAlchemy
db = SQLAlchemy(app)

# 定义数据模型
class VueTable(db.Model):
    __tablename__ = 'VueTable'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255))
    age = db.Column(db.Integer)

# 在应用上下文中检查并创建表
with app.app_context():
    inspector = sqlalchemy.inspect(db.engine)  # 获取数据库检查对象
    table_name = 'VueTable'
    if not inspector.has_table(table_name):  # 使用 inspect() 检查表是否存在
        db.create_all()  # 如果表不存在，则创建

# 获取所有数据接口
@app.route('/api/getData', methods=['GET'])
def get_data():
    results = VueTable.query.all()
    data = [{'id': item.id, 'name': item.name, 'age': item.age} for item in results]
    return jsonify({'success': True, 'data': data})

# 增加数据接口
@app.route('/api/addData', methods=['POST'])
def add_data():
    req_data = request.json
    name = req_data.get('name')
    age = req_data.get('age')
    if name is None or age is None:
        return jsonify({'success': False, 'error': 'Name and age are required'}), 400
    new_item = VueTable(name=name, age=age)
    db.session.add(new_item)
    db.session.commit()
    results = VueTable.query.all()
    data = [{'id': item.id, 'name': item.name, 'age': item.age} for item in results]
    return jsonify({'success': True, 'data': data,'addData':{'name':name,'age':age}})

# 删除数据接口
@app.route('/api/deleteData', methods=['GET'])
def delete_data():
    id = request.args.get('id')
    if id is None:
        return jsonify({'success': False, 'error': 'ID parameter is missing'}), 400
    item = VueTable.query.filter_by(id=int(id)).first()
    if item:
        db.session.delete(item)
        db.session.commit() 
        return jsonify({'success': True}), 200
    else:
        return jsonify({'success': False, 'error': 'Item not found'}), 404

# 更新数据接口
@app.route('/api/updateData', methods=['POST'])
def update_data():
    req_data = request.json
    id = req_data.get('id')
    name = req_data.get('name')
    age = req_data.get('age')
    if name is None or age is None:
        return jsonify({'success': False, 'error': 'Name and age are required'}), 400
    item = VueTable.query.filter_by(id=int(id)).first()
    if item:
        item.name = name
        item.age = age
        db.session.commit() 
        return get_data() 
    else:
        return jsonify({'success': False, 'error': 'Item not found'}), 404

# 启动 Flask 应用
if __name__ == '__main__':
    app.run(host="0.0.0.0",port="5001")
