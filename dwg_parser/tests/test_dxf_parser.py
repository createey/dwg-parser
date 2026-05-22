# dwg_parser/tests/test_dxf_parser.py
import pytest
import tempfile
import os
from dwg_parser.dxf_parser import DXFReader

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

from dwg_parser.dxf_parser import LayerExtractor

class TestLayerExtractor:
    def test_extract_layers_empty_doc(self):
        """测试从空文档提取图层"""
        extractor = LayerExtractor(None)
        assert extractor.extract_layers() == []

    def test_extract_layers(self):
        """测试提取图层信息"""
        import ezdxf
        doc = ezdxf.new(dxfversion="R2010")
        doc.layers.add("TestLayer", color=7, linetype="CONTINUOUS")
        extractor = LayerExtractor(doc)
        layers = extractor.extract_layers()
        assert len(layers) >= 1
        layer = layers[0]
        assert 'name' in layer
        assert 'color' in layer
        assert 'linetype' in layer

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
