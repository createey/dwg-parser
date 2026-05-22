# dwg_parser/create_sample.py
import ezdxf
from ezdxf.enums import TextEntityAlignment

# 创建一个新的DXF文档
doc = ezdxf.new(dxfversion="R2010")
msp = doc.modelspace()

# 添加图层
doc.layers.add("WALLS", color=1)
doc.layers.add("TEXT", color=7)
doc.layers.add("DIMENSIONS", color=3)

# 添加线条（墙体）
msp.add_line((0, 0), (10, 0), dxfattribs={"layer": "WALLS"})
msp.add_line((10, 0), (10, 10), dxfattribs={"layer": "WALLS"})
msp.add_line((10, 10), (0, 10), dxfattribs={"layer": "WALLS"})
msp.add_line((0, 10), (0, 0), dxfattribs={"layer": "WALLS"})

# 添加文本
msp.add_text(
    "房间 A",
    dxfattribs={"layer": "TEXT"}
).set_placement((5, 5), align=TextEntityAlignment.CENTER)

msp.add_text(
    "10.0m x 10.0m",
    dxfattribs={"layer": "DIMENSIONS"}
).set_placement((5, 2), align=TextEntityAlignment.CENTER)

# 保存文件
doc.saveas("sample.dxf")
print("示例DXF文件创建成功：sample.dxf")
