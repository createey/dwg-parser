# dwg_parser/data_converter.py
from typing import Dict, Any, List
from .entities import Point, Line, Circle, Arc, Polyline, Spline
from .entities import Text, MText, Dimension

class DataConverter:
    """Convert raw DWG data to Python objects"""
    
    def convert_point(self, raw_data: Dict[str, Any]) -> Point:
        """Convert raw data to Point object"""
        return Point(
            x=float(raw_data.get('x', 0.0)),
            y=float(raw_data.get('y', 0.0)),
            z=float(raw_data.get('z', 0.0))
        )
    
    def convert_line(self, raw_data: Dict[str, Any]) -> Line:
        """Convert raw data to Line object"""
        return Line(
            start=self.convert_point(raw_data.get('start', {})),
            end=self.convert_point(raw_data.get('end', {})),
            layer=raw_data.get('layer', ''),
            handle=int(raw_data.get('handle', 0))
        )
    
    def convert_circle(self, raw_data: Dict[str, Any]) -> Circle:
        """Convert raw data to Circle object"""
        return Circle(
            center=self.convert_point(raw_data.get('center', {})),
            radius=float(raw_data.get('radius', 0.0)),
            layer=raw_data.get('layer', ''),
            handle=int(raw_data.get('handle', 0))
        )
    
    def convert_arc(self, raw_data: Dict[str, Any]) -> Arc:
        """Convert raw data to Arc object"""
        return Arc(
            center=self.convert_point(raw_data.get('center', {})),
            radius=float(raw_data.get('radius', 0.0)),
            start_angle=float(raw_data.get('start_angle', 0.0)),
            end_angle=float(raw_data.get('end_angle', 0.0)),
            layer=raw_data.get('layer', ''),
            handle=int(raw_data.get('handle', 0))
        )
    
    def convert_polyline(self, raw_data: Dict[str, Any]) -> Polyline:
        """Convert raw data to Polyline object"""
        vertices = [self.convert_point(v) for v in raw_data.get('vertices', [])]
        return Polyline(
            vertices=vertices,
            closed=bool(raw_data.get('closed', False)),
            layer=raw_data.get('layer', ''),
            handle=int(raw_data.get('handle', 0))
        )
    
    def convert_text(self, raw_data: Dict[str, Any]) -> Text:
        """Convert raw data to Text object"""
        return Text(
            content=raw_data.get('content', ''),
            position=self.convert_point(raw_data.get('position', {})),
            height=float(raw_data.get('height', 1.0)),
            rotation=float(raw_data.get('rotation', 0.0)),
            layer=raw_data.get('layer', ''),
            handle=int(raw_data.get('handle', 0))
        )
    
    def convert_entities(self, raw_entities: List[Dict[str, Any]]) -> List[Any]:
        """Convert list of raw entities to Python objects"""
        converted = []
        for raw in raw_entities:
            entity_type = raw.get('type', '').lower()
            
            if entity_type == 'line':
                converted.append(self.convert_line(raw))
            elif entity_type == 'circle':
                converted.append(self.convert_circle(raw))
            elif entity_type == 'arc':
                converted.append(self.convert_arc(raw))
            elif entity_type == 'polyline':
                converted.append(self.convert_polyline(raw))
            elif entity_type == 'text':
                converted.append(self.convert_text(raw))
            # Add more entity types as needed
        
        return converted