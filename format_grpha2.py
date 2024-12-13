import pyvista as pv
import sqlite3
import random
import networkx as nx
import math

# 数据库路径
database = "F:/train_bird/train_databases/books/books.sqlite"

# 连接到数据库
conn = sqlite3.connect(database)
cursor = conn.cursor()

# 获取表和外键信息
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = [table[0] for table in cursor.fetchall()]

edges = []
in_degree = {table: 0 for table in tables}  # 初始化每个表的入度
out_degree = {table: 0 for table in tables}  # 初始化每个表的出度

# 获取外键关系并计算度数
for table in tables:
    cursor.execute(f"PRAGMA foreign_key_list({table});")
    foreign_keys = cursor.fetchall()
    for fk in foreign_keys:
        ref_table = fk[2]  # 外键引用的表名
        fk_field = fk[3]  # 外键字段
        ref_field = fk[4]  # 引用字段
        edges.append((table, ref_table, fk_field, ref_field))
        out_degree[table] += 1  # 出度
        in_degree[ref_table] += 1  # 入度

# 使用 NetworkX 计算力导向布局
G = nx.DiGraph()  # 创建有向图
G.add_edges_from([(start, end) for start, end, _, _ in edges])  # 添加边到图中

# 使用 spring_layout 算法计算节点位置（力导向布局）
pos = nx.spring_layout(G, k=0.1, iterations=100)  # k 是弹簧常数，iterations 是迭代次数

# 检查缺失的表并提供默认坐标
nodes_coordinates = {}
for table in tables:
    if table in pos:
        nodes_coordinates[table] = (pos[table][0] * 10, pos[table][1] * 10, random.uniform(-5, 5))
    else:
        # 默认坐标
        nodes_coordinates[table] = (0, 0, random.uniform(-5, 5))

# 设置最短边的长度（单位：坐标轴尺度）
min_edge_length = 2.0  # 你可以根据需要调整这个值


# 计算并调整边的长度，确保最小边长
def adjust_edge_length(start_coord, end_coord, min_length):
    # 计算两点之间的欧氏距离
    dx = end_coord[0] - start_coord[0]
    dy = end_coord[1] - start_coord[1]
    dz = end_coord[2] - start_coord[2]
    distance = math.sqrt(dx ** 2 + dy ** 2 + dz ** 2)

    # 如果距离小于最小长度，按比例缩放两点之间的距离
    if distance < min_length:
        # 计算比例系数
        ratio = min_length / distance
        # 调整坐标
        new_end_coord = (
            start_coord[0] + dx * ratio,
            start_coord[1] + dy * ratio,
            start_coord[2] + dz * ratio
        )
        return start_coord, new_end_coord
    else:
        return start_coord, end_coord


# 创建 PyVista 的 3D 图
plotter = pv.Plotter()
plotter.add_axes()

# 添加节点（表）
for table, coord in nodes_coordinates.items():
    sphere = pv.Sphere(radius=0.3, center=coord)
    plotter.add_mesh(sphere, color="skyblue", label=table)
    plotter.add_point_labels(
        [coord],
        [table],
        point_size=20,
        font_size=14,  # 合适字体大小
        always_visible=True,
        text_color="black"
    )

# 添加边（外键关系）
for edge in edges:
    start, end, fk_field, ref_field = edge
    start_coord = nodes_coordinates[start]
    end_coord = nodes_coordinates[end]

    # 调整边的长度，确保最小边长
    start_coord, end_coord = adjust_edge_length(start_coord, end_coord, min_edge_length)

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
        point_size=10,
        font_size=14,
        text_color="white"
    )

# 显示图
plotter.show()
