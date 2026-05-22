# DXF Parser 设计文档

## 概述

创建一个独立的Python脚本，使用ezdxf库解析DXF文件，提取图层信息和文本标注，输出为JSON格式。

## 架构设计

脚本将包含以下主要功能：
1. 读取DXF文件
2. 提取图层信息
3. 提取文本标注
4. 输出为JSON格式

## 组件设计

脚本将包含以下主要组件：
1. DXFReader类：用于读取DXF文件
2. LayerExtractor类：用于提取图层信息
3. TextExtractor类：用于提取文本标注
4. JSONExporter类：用于输出JSON格式

## 数据流设计

DXF文件 -> DXFReader读取 -> LayerExtractor提取图层信息 -> TextExtractor提取文本标注 -> JSONExporter输出JSON

## 错误处理设计

1. 文件不存在时抛出异常
2. DXF文件格式错误时抛出异常
3. 提取数据失败时记录错误并继续
4. 输出JSON失败时抛出异常

## 测试设计

1. 单元测试各个类的功能
2. 集成测试整个脚本的工作流程
3. 使用示例DXF文件进行测试

## 实现细节

### DXFReader类

```python
import ezdxf

class DXFReader:
    def __init__(self, file_path):
        self.file_path = file_path
        self.doc = None
    
    def read(self):
        """读取DXF文件"""
        try:
            self.doc = ezdxf.readfile(self.file_path)
            return True
        except Exception as e:
            print(f"读取DXF文件失败: {e}")
            return False
    
    def get_modelspace(self):
        """获取模型空间"""
        if self.doc:
            return self.doc.modelspace()
        return None
```

### LayerExtractor类

```python
class LayerExtractor:
    def __init__(self, doc):
        self.doc = doc
    
    def extract_layers(self):
        """提取图层信息"""
        layers = []
        if self.doc:
            for layer in self.doc.layers:
                layer_info = {
                    'name': layer.dxf.name,
                    'color': layer.color,
                    'linetype': layer.dxf.linetype
                }
                layers.append(layer_info)
        return layers
```

### TextExtractor类

```python
class TextExtractor:
    def __init__(self, doc):
        self.doc = doc
    
    def extract_text(self):
        """提取文本标注"""
        texts = []
        if self.doc:
            msp = self.doc.modelspace()
            for entity in msp:
                if entity.dxftype() == 'TEXT':
                    text_info = {
                        'type': 'TEXT',
                        'text': entity.dxf.text,
                        'layer': entity.dxf.layer,
                        'insert': entity.dxf.insert.xyz
                    }
                    texts.append(text_info)
                elif entity.dxftype() == 'MTEXT':
                    text_info = {
                        'type': 'MTEXT',
                        'text': entity.text,
                        'layer': entity.dxf.layer,
                        'insert': entity.dxf.insert.xyz
                    }
                    texts.append(text_info)
        return texts
```

### JSONExporter类

```python
import json

class JSONExporter:
    def __init__(self, output_path):
        self.output_path = output_path
    
    def export(self, data):
        """导出为JSON格式"""
        try:
            with open(self.output_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"导出JSON失败: {e}")
            return False
```

### 主程序

```python
def main():
    # 读取DXF文件
    reader = DXFReader('input.dxf')
    if not reader.read():
        return
    
    # 提取图层信息
    layer_extractor = LayerExtractor(reader.doc)
    layers = layer_extractor.extract_layers()
    
    # 提取文本标注
    text_extractor = TextExtractor(reader.doc)
    texts = text_extractor.extract_text()
    
    # 组合数据
    data = {
        'layers': layers,
        'texts': texts
    }
    
    # 导出JSON
    exporter = JSONExporter('output.json')
    if exporter.export(data):
        print("数据提取成功！")

if __name__ == '__main__':
    main()
```

## 使用说明

1. 安装依赖：`pip install ezdxf`
2. 手动将DWG文件转换为DXF格式
3. 运行脚本：`python dxf_parser.py input.dxf`
4. 输出JSON文件：`output.json`

## 依赖项

- ezdxf：用于解析DXF文件
- Python 3.6+

## 注意事项

1. 需要先将DWG文件转换为DXF格式
2. 某些复杂的DXF实体可能需要额外的处理
3. 大文件可能需要较长时间处理