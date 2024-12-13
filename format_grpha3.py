from random import random

import pyvista as pv
import sqlite3
import numpy as np

# 数据库路径
database = "F:/train_bird/train_databases/books/books.sqlite"

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

# 随机生成 3D 坐标
nodes = {table: (random.random(), random.random(), random.random()) for table in tables}

# 创建 PyVista 的 3D 图
plotter = pv.Plotter()
plotter.add_axes()

# 添加节点（表）
for table, coord in nodes.items():
    sphere = pv.Sphere(radius=0.03, center=coord)
    plotter.add_mesh(sphere, color="skyblue", label=table)
    plotter.add_point_labels(
        [coord],
        [table],
        point_size=30,
        font_size=16,  # 增大字体
        always_visible=True,
        text_color="black"
    )

# 添加边（外键关系）
for edge in edges:
    start, end, fk_field, ref_field = edge
    start_coord = nodes[start]
    end_coord = nodes[end]
    line = pv.Line(start_coord, end_coord)
    plotter.add_mesh(line, color="gray", line_width=2)

    # 计算边的中点
    mid_point = (
        (start_coord[0] + end_coord[0]) / 2,
        (start_coord[1] + end_coord[1]) / 2,
        (start_coord[2] + end_coord[2]) / 2,
    )

    # 添加外键依赖信息
    edge_label = f"{start}.{fk_field} -> {end}.{ref_field}"
    plotter.add_point_labels(
        [mid_point],
        [edge_label],
        point_size=20,
        font_size=10,
        text_color="red"
    )

# 显示图
plotter.show()
