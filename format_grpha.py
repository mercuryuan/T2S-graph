database = "F:/train_bird/train_databases/books/books.sqlite"
import sqlite3
import plotly.graph_objects as go
import numpy as np

# 连接到数据库
conn = sqlite3.connect(database)
cursor = conn.cursor()

# 获取表和外键信息
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = [table[0] for table in cursor.fetchall()]

edges = []
for table in tables:
    cursor.execute(f"PRAGMA foreign_key_list({table});")
    foreign_keys = cursor.fetchall()
    for fk in foreign_keys:
        ref_table = fk[2]  # 外键引用的表名
        fk_field = fk[3]  # 外键字段
        ref_field = fk[4]  # 引用字段
        edges.append((table, ref_table, fk_field, ref_field))

# 使用环形布局生成节点的 3D 坐标
num_tables = len(tables)
theta = np.linspace(0, 2 * np.pi, num_tables, endpoint=False)  # 均匀分布角度
radius = 1  # 半径
z_values = np.linspace(-0.5, 0.5, num_tables)  # 添加 Z 坐标变化

nodes = {
    tables[i]: (
        radius * np.cos(theta[i]),  # x 坐标
        radius * np.sin(theta[i]),  # y 坐标
        z_values[i]  # z 坐标
    )
    for i in range(num_tables)
}

# 创建 3D 图形
fig = go.Figure()

# 添加节点（表）
for table, coord in nodes.items():
    fig.add_trace(go.Scatter3d(
        x=[coord[0]],
        y=[coord[1]],
        z=[coord[2]],
        mode='markers+text',
        marker=dict(size=10, color='skyblue'),
        text=table,
        textposition='top center',
        name=table
    ))

# 添加边（外键关系）
for edge in edges:
    start, end, fk_field, ref_field = edge
    fig.add_trace(go.Scatter3d(
        x=[nodes[start][0], nodes[end][0]],
        y=[nodes[start][1], nodes[end][1]],
        z=[nodes[start][2], nodes[end][2]],
        mode='lines+text',
        line=dict(color='gray', width=2),
        text=f"{start}.{fk_field} → {end}.{ref_field}",
        textposition="middle center",
        showlegend=False
    ))

# 更新图形布局
fig.update_layout(
    scene=dict(
        xaxis_title='X Axis',
        yaxis_title='Y Axis',
        zaxis_title='Z Axis',
    ),
    title='3D Database Schema Visualization with Foreign Key Details',
    showlegend=False
)

fig.show()
