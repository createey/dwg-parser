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
