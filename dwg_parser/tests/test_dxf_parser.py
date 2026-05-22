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