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
