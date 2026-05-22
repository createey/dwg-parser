# DXF Parser 使用说明

## 安装

1. 安装依赖：
```bash
pip install -r requirements.txt
pip install -e .
```

## 使用方法

### 命令行使用

```bash
# 基本用法
python dxf_parser.py input.dxf

# 指定输出文件
python dxf_parser.py input.dxf output.json
```

### Python API使用

```python
from dxf_parser import DXFReader, LayerExtractor, TextExtractor, JSONExporter

# 读取DXF文件
reader = DXFReader('input.dxf')
reader.read()

# 提取图层信息
layer_extractor = LayerExtractor(reader.doc)
layers = layer_extractor.extract_layers()

# 提取文本标注
text_extractor = TextExtractor(reader.doc)
texts = text_extractor.extract_text()

# 导出JSON
data = {'layers': layers, 'texts': texts}
exporter = JSONExporter('output.json')
exporter.export(data)
```

## 输出格式

输出的JSON文件包含以下结构：

```json
{
  "layers": [
    {
      "name": "图层名称",
      "color": 7,
      "linetype": "Continuous"
    }
  ],
  "texts": [
    {
      "type": "TEXT",
      "text": "文本内容",
      "layer": "图层名称",
      "insert": [x, y, z]
    }
  ]
}
```

## 注意事项

1. 需要先将DWG文件转换为DXF格式
2. 某些复杂的DXF实体可能需要额外的处理
3. 大文件可能需要较长时间处理
