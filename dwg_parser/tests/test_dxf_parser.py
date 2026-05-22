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

from dwg_parser.dxf_parser import TextExtractor

class TestTextExtractor:
    def test_extract_text_from_empty_document(self):
        """测试从空文档提取文本"""
        import ezdxf
        doc = ezdxf.new(dxfversion="R2010")
        extractor = TextExtractor(doc)
        texts = extractor.extract_text()
        assert isinstance(texts, list)
        assert len(texts) == 0

from dwg_parser.dxf_parser import JSONExporter
import json

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

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
