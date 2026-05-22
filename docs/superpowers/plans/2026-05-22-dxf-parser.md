# DXF Parser Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 创建一个独立的Python脚本，使用ezdxf库解析DXF文件，提取图层信息和文本标注，输出为JSON格式。

**Architecture:** 使用四个主要组件：DXFReader、LayerExtractor、TextExtractor和JSONExporter，每个组件负责特定功能。采用TDD方法，先编写测试再实现功能。

**Tech Stack:** Python 3.6+, ezdxf库, pytest测试框架

---

## File Structure

- `dxf_parser.py` - 主脚本，包含所有类和功能
- `tests/test_dxf_parser.py` - 测试文件
- `requirements.txt` - 更新依赖项
- `setup.py` - 更新安装配置

## Task 1: Setup Project and Dependencies

**Files:**
- Modify: `requirements.txt`
- Modify: `setup.py`

- [ ] **Step 1: Update requirements.txt**

```txt
# dwg_parser/requirements.txt
ctypes>=1.1.0
cffi>=1.15.0
pytest>=7.0.0
ezdxf>=0.18.0
```

- [ ] **Step 2: Update setup.py**

```python
# dwg_parser/setup.py
from setuptools import setup, find_packages

setup(
    name="dxf_parser",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "ezdxf>=0.18.0",
    ],
    entry_points={
        'console_scripts': [
            'dxf-parser=dxf_parser.main:main',
        ],
    },
)
```

- [ ] **Step 3: Install dependencies**

Run: `pip install -e .`

- [ ] **Step 4: Commit**

```bash
git add requirements.txt setup.py
git commit -m "chore: add ezdxf dependency and update setup.py"
```

## Task 2: Create Test File Structure

**Files:**
- Create: `tests/test_dxf_parser.py`

- [ ] **Step 1: Create test file structure**

```python
# dwg_parser/tests/test_dxf_parser.py
import pytest
import json
import tempfile
import os
from dxf_parser import DXFReader, LayerExtractor, TextExtractor, JSONExporter

class TestDXFReader:
    def test_read_nonexistent_file(self):
        """测试读取不存在的文件"""
        reader = DXFReader("nonexistent.dxf")
        assert reader.read() == False
    
    def test_read_valid_file(self):
        """测试读取有效的DXF文件"""
        # 创建临时DXF文件用于测试
        import ezdxf
        doc = ezdxf.new(dxfversion="R2010")
        msp = doc.modelspace()
        msp.add_line((0, 0), (10, 0))
        with tempfile.NamedTemporaryFile(suffix='.dxf', delete=False) as f:
            temp_path = f.name
            doc.saveas(temp_path)
        
        try:
            reader = DXFReader(temp_path)
            assert reader.read() == True
        finally:
            os.unlink(temp_path)

class TestLayerExtractor:
    def test_extract_layers_from_empty_document(self):
        """测试从空文档提取图层"""
        import ezdxf
        doc = ezdxf.new(dxfversion="R2010")
        extractor = LayerExtractor(doc)
        layers = extractor.extract_layers()
        assert isinstance(layers, list)
        assert len(layers) >= 1  # 至少有一个默认图层

class TestTextExtractor:
    def test_extract_text_from_empty_document(self):
        """测试从空文档提取文本"""
        import ezdxf
        doc = ezdxf.new(dxfversion="R2010")
        extractor = TextExtractor(doc)
        texts = extractor.extract_text()
        assert isinstance(texts, list)
        assert len(texts) == 0

class TestJSONExporter:
    def test_export_to_json(self):
        """测试导出到JSON文件"""
        data = {"test": "value"}
        with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as f:
            temp_path = f.name
        
        try:
            exporter = JSONExporter(temp_path)
            assert exporter.export(data) == True
            
            # 验证文件内容
            with open(temp_path, 'r', encoding='utf-8') as f:
                loaded_data = json.load(f)
                assert loaded_data == data
        finally:
            os.unlink(temp_path)

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest dwg_parser/tests/test_dxf_parser.py -v`
Expected: FAIL with "ModuleNotFoundError: No module named 'dxf_parser'"

- [ ] **Step 3: Commit**

```bash
git add dwg_parser/tests/test_dxf_parser.py
git commit -m "test: add test structure for DXF parser"
```

## Task 3: Implement DXFReader Class

**Files:**
- Create: `dxf_parser.py`

- [ ] **Step 1: Write the failing test for DXFReader**

```python
# 已在Task 2中包含在tests/test_dxf_parser.py中
```

- [ ] **Step 2: Implement DXFReader class**

```python
# dwg_parser/dxf_parser.py
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

# 主程序函数
def main():
    print("DXF Parser - 主程序")

if __name__ == '__main__':
    main()
```

- [ ] **Step 3: Run tests to verify they pass**

Run: `pytest dwg_parser/tests/test_dxf_parser.py::TestDXFReader -v`
Expected: PASS

- [ ] **Step 4: Commit**

```bash
git add dwg_parser/dxf_parser.py
git commit -m "feat: implement DXFReader class"
```

## Task 4: Implement LayerExtractor Class

**Files:**
- Modify: `dxf_parser.py`

- [ ] **Step 1: Write the failing test for LayerExtractor**

```python
# 已在Task 2中包含在tests/test_dxf_parser.py中
```

- [ ] **Step 2: Implement LayerExtractor class**

```python
# dwg_parser/dxf_parser.py (追加到文件)
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

- [ ] **Step 3: Run tests to verify they pass**

Run: `pytest dwg_parser/tests/test_dxf_parser.py::TestLayerExtractor -v`
Expected: PASS

- [ ] **Step 4: Commit**

```bash
git add dwg_parser/dxf_parser.py
git commit -m "feat: implement LayerExtractor class"
```

## Task 5: Implement TextExtractor Class

**Files:**
- Modify: `dxf_parser.py`

- [ ] **Step 1: Write the failing test for TextExtractor**

```python
# 已在Task 2中包含在tests/test_dxf_parser.py中
```

- [ ] **Step 2: Implement TextExtractor class**

```python
# dwg_parser/dxf_parser.py (追加到文件)
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

- [ ] **Step 3: Run tests to verify they pass**

Run: `pytest dwg_parser/tests/test_dxf_parser.py::TestTextExtractor -v`
Expected: PASS

- [ ] **Step 4: Commit**

```bash
git add dwg_parser/dxf_parser.py
git commit -m "feat: implement TextExtractor class"
```

## Task 6: Implement JSONExporter Class

**Files:**
- Modify: `dxf_parser.py`

- [ ] **Step 1: Write the failing test for JSONExporter**

```python
# 已在Task 2中包含在tests/test_dxf_parser.py中
```

- [ ] **Step 2: Implement JSONExporter class**

```python
# dwg_parser/dxf_parser.py (追加到文件)
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

- [ ] **Step 3: Run tests to verify they pass**

Run: `pytest dwg_parser/tests/test_dxf_parser.py::TestJSONExporter -v`
Expected: PASS

- [ ] **Step 4: Commit**

```bash
git add dwg_parser/dxf_parser.py
git commit -m "feat: implement JSONExporter class"
```

## Task 7: Implement Main Function and Integration

**Files:**
- Modify: `dxf_parser.py`

- [ ] **Step 1: Write integration test**

```python
# dwg_parser/tests/test_dxf_parser.py (追加到文件)
class TestIntegration:
    def test_full_workflow(self):
        """测试完整工作流程"""
        import ezdxf
        from ezdxf.enums import TextEntityAlignment
        
        # 创建临时DXF文件
        doc = ezdxf.new(dxfversion="R2010")
        msp = doc.modelspace()
        
        # 添加图层
        doc.layers.add("TEST_LAYER", color=7)
        
        # 添加文本
        msp.add_text(
            "Test Text",
            dxfattribs={"layer": "TEST_LAYER"}
        ).set_placement((0, 0), align=TextEntityAlignment.LEFT)
        
        # 添加线条
        msp.add_line((0, 0), (10, 0), dxfattribs={"layer": "TEST_LAYER"})
        
        # 保存到临时文件
        with tempfile.NamedTemporaryFile(suffix='.dxf', delete=False) as f:
            temp_dxf_path = f.name
            doc.saveas(temp_dxf_path)
        
        # 创建临时JSON文件路径
        with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as f:
            temp_json_path = f.name
        
        try:
            # 执行完整工作流程
            reader = DXFReader(temp_dxf_path)
            assert reader.read() == True
            
            layer_extractor = LayerExtractor(reader.doc)
            layers = layer_extractor.extract_layers()
            assert len(layers) >= 2  # 默认图层 + TEST_LAYER
            
            text_extractor = TextExtractor(reader.doc)
            texts = text_extractor.extract_text()
            assert len(texts) == 1
            assert texts[0]['text'] == "Test Text"
            
            data = {
                'layers': layers,
                'texts': texts
            }
            
            exporter = JSONExporter(temp_json_path)
            assert exporter.export(data) == True
            
            # 验证JSON文件内容
            with open(temp_json_path, 'r', encoding='utf-8') as f:
                loaded_data = json.load(f)
                assert loaded_data['layers'] == layers
                assert loaded_data['texts'] == texts
                
        finally:
            os.unlink(temp_dxf_path)
            os.unlink(temp_json_path)
```

- [ ] **Step 2: Run integration test**

Run: `pytest dwg_parser/tests/test_dxf_parser.py::TestIntegration -v`
Expected: PASS

- [ ] **Step 3: Update main function**

```python
# dwg_parser/dxf_parser.py (更新main函数)
def main():
    import sys
    
    if len(sys.argv) < 2:
        print("用法: python dxf_parser.py <input.dxf> [output.json]")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else "output.json"
    
    # 读取DXF文件
    reader = DXFReader(input_file)
    if not reader.read():
        sys.exit(1)
    
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
    exporter = JSONExporter(output_file)
    if exporter.export(data):
        print(f"数据提取成功！输出文件: {output_file}")
        print(f"图层数量: {len(layers)}")
        print(f"文本数量: {len(texts)}")
    else:
        print("数据提取失败！")
        sys.exit(1)

if __name__ == '__main__':
    main()
```

- [ ] **Step 4: Run all tests**

Run: `pytest dwg_parser/tests/test_dxf_parser.py -v`
Expected: ALL PASS

- [ ] **Step 5: Commit**

```bash
git add dwg_parser/dxf_parser.py
git commit -m "feat: implement main function and integration"
```

## Task 8: Update Package Configuration

**Files:**
- Modify: `setup.py`

- [ ] **Step 1: Update setup.py with correct entry point**

```python
# dwg_parser/setup.py
from setuptools import setup, find_packages

setup(
    name="dxf_parser",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "ezdxf>=0.18.0",
    ],
    entry_points={
        'console_scripts': [
            'dxf-parser=dxf_parser.dxf_parser:main',
        ],
    },
)
```

- [ ] **Step 2: Install package**

Run: `pip install -e .`

- [ ] **Step 3: Commit**

```bash
git add dwg_parser/setup.py
git commit -m "chore: update package configuration"
```

## Task 9: Create Usage Documentation

**Files:**
- Create: `USAGE.md`

- [ ] **Step 1: Create usage documentation**

```markdown
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
```

- [ ] **Step 2: Commit**

```bash
git add USAGE.md
git commit -m "docs: add usage documentation"
```

## Task 10: Final Testing and Verification

**Files:**
- No new files

- [ ] **Step 1: Run all tests**

Run: `pytest dwg_parser/tests/test_dxf_parser.py -v`
Expected: ALL PASS

- [ ] **Step 2: Test with sample DXF file**

Run: `python dxf_parser.py sample.dwf sample_output.json`
Expected: Successful extraction

- [ ] **Step 3: Commit**

```bash
git add -A
git commit -m "chore: final testing and verification"
```