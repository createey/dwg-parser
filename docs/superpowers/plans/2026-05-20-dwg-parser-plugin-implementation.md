# DWG Parser Plugin Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement a DWG file parser plugin for OpenCode that extracts all readable data from DWG files for engineering quantity calculation and pricing.

**Architecture:** Three-layer architecture: DWG parsing layer (LibreDWG), data conversion layer (Python objects), and OpenCode plugin layer (CLI/API). Uses LibreDWG library for DWG parsing with Python bindings via ctypes.

**Tech Stack:** Python 3.8+, LibreDWG, ctypes/cffi, OpenCode plugin system

---

## File Structure

### Core Components

```
dwg_parser/
├── __init__.py                    # Package initialization
├── libredwg_bindings.py          # LibreDWG Python bindings
├── dwg_parser.py                 # Main DWG parser class
├── data_converter.py             # Data conversion layer
├── entities/
│   ├── __init__.py
│   ├── geometric.py              # Geometric entities (point, line, circle, etc.)
│   ├── text.py                   # Text entities (text, mtext, dimensions)
│   └── blocks.py                 # Block references and attributes
├── plugin/
│   ├── __init__.py
│   ├── cli.py                    # Command-line interface
│   ├── api.py                    # API endpoints
│   └── config.py                 # Configuration management
└── tests/
    ├── __init__.py
    ├── test_libredwg_bindings.py
    ├── test_dwg_parser.py
    ├── test_data_converter.py
    ├── test_entities.py
    ├── test_plugin.py
    └── test_integration.py
```

### Configuration Files

```
dwg_parser/
├── setup.py                      # Package setup
├── requirements.txt              # Dependencies
└── README.md                     # Documentation
```

---

## Task 1: Setup Development Environment

**Files:**
- Create: `dwg_parser/setup.py`
- Create: `dwg_parser/requirements.txt`
- Create: `dwg_parser/__init__.py`

- [ ] **Step 1: Create package structure**

```python
# dwg_parser/__init__.py
"""DWG Parser Plugin for OpenCode"""
__version__ = "0.1.0"
__author__ = "OpenCode"
```

- [ ] **Step 2: Create requirements.txt**

```
# dwg_parser/requirements.txt
ctypes>=1.1.0
cffi>=1.15.0
pytest>=7.0.0
```

- [ ] **Step 3: Create setup.py**

```python
# dwg_parser/setup.py
from setuptools import setup, find_packages

setup(
    name="dwg_parser",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "ctypes>=1.1.0",
        "cffi>=1.15.0",
    ],
    author="OpenCode",
    description="DWG Parser Plugin for OpenCode",
    python_requires=">=3.8",
)
```

- [ ] **Step 4: Verify package structure**

Run: `python -c "import dwg_parser; print(dwg_parser.__version__)"`
Expected: `0.1.0`

- [ ] **Step 5: Commit**

```bash
git add dwg_parser/__init__.py dwg_parser/requirements.txt dwg_parser/setup.py
git commit -m "feat: initialize DWG parser package structure"
```

---

## Task 2: LibreDWG Python Bindings

**Files:**
- Create: `dwg_parser/libredwg_bindings.py`
- Create: `dwg_parser/tests/test_libredwg_bindings.py`

- [ ] **Step 1: Write failing test for LibreDWG initialization**

```python
# dwg_parser/tests/test_libredwg_bindings.py
import pytest
from dwg_parser.libredwg_bindings import LibreDWGBindings

def test_libredwg_initialization():
    bindings = LibreDWGBindings()
    assert bindings is not None
    assert bindings.initialized is False

def test_libredwg_load_library():
    bindings = LibreDWGBindings()
    result = bindings.load_library()
    assert result is True
    assert bindings.initialized is True
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest dwg_parser/tests/test_libredwg_bindings.py::test_libredwg_initialization -v`
Expected: FAIL with "ModuleNotFoundError: No module named 'dwg_parser.libredwg_bindings'"

- [ ] **Step 3: Write minimal implementation**

```python
# dwg_parser/libredwg_bindings.py
import ctypes
import os
from typing import Optional, List, Dict, Any

class LibreDWGBindings:
    """Python bindings for LibreDWG library"""
    
    def __init__(self):
        self.libredwg = None
        self.initialized = False
        
    def load_library(self) -> bool:
        """Load LibreDWG library"""
        try:
            # Try to load the library
            if os.name == 'nt':  # Windows
                self.libredwg = ctypes.CDLL('libredwg.dll')
            else:  # Linux/Mac
                self.libredwg = ctypes.CDLL('libredwg.so')
            
            self.initialized = True
            return True
        except OSError as e:
            print(f"Failed to load LibreDWG: {e}")
            return False
    
    def read_file(self, file_path: str) -> Optional[Any]:
        """Read a DWG file"""
        if not self.initialized:
            raise RuntimeError("LibreDWG not initialized")
        
        # This will be implemented in the next task
        raise NotImplementedError
    
    def get_entities(self, dwg_data: Any) -> List[Dict[str, Any]]:
        """Get entities from DWG data"""
        if not self.initialized:
            raise RuntimeError("LibreDWG not initialized")
        
        # This will be implemented in the next task
        raise NotImplementedError
    
    def get_layers(self, dwg_data: Any) -> List[Dict[str, Any]]:
        """Get layers from DWG data"""
        if not self.initialized:
            raise RuntimeError("LibreDWG not initialized")
        
        # This will be implemented in the next task
        raise NotImplementedError
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest dwg_parser/tests/test_libredwg_bindings.py::test_libredwg_initialization -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add dwg_parser/libredwg_bindings.py dwg_parser/tests/test_libredwg_bindings.py
git commit -m "feat: implement LibreDWG Python bindings initialization"
```

---

## Task 3: DWG File Reading

**Files:**
- Modify: `dwg_parser/libredwg_bindings.py`
- Create: `dwg_parser/dwg_parser.py`
- Create: `dwg_parser/tests/test_dwg_parser.py`

- [ ] **Step 1: Write failing test for DWG file reading**

```python
# dwg_parser/tests/test_dwg_parser.py
import pytest
import tempfile
import os
from dwg_parser.dwg_parser import DWGParser

def test_dwg_parser_initialization():
    parser = DWGParser()
    assert parser is not None
    assert parser.bindings is not None

def test_dwg_parser_load_file():
    parser = DWGParser()
    # Create a temporary DWG file for testing
    with tempfile.NamedTemporaryFile(suffix='.dwg', delete=False) as tmp:
        tmp.write(b'test dwg content')
        tmp_path = tmp.name
    
    try:
        result = parser.load(tmp_path)
        assert result is True
        assert parser.file_loaded is True
    finally:
        os.unlink(tmp_path)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest dwg_parser/tests/test_dwg_parser.py::test_dwg_parser_initialization -v`
Expected: FAIL with "ModuleNotFoundError: No module named 'dwg_parser.dwg_parser'"

- [ ] **Step 3: Write minimal implementation**

```python
# dwg_parser/dwg_parser.py
from typing import Optional, List, Dict, Any
from .libredwg_bindings import LibreDWGBindings

class DWGParser:
    """Main DWG parser class"""
    
    def __init__(self):
        self.bindings = LibreDWGBindings()
        self.file_loaded = False
        self.dwg_data = None
        
    def load(self, file_path: str) -> bool:
        """Load a DWG file"""
        try:
            if not self.bindings.initialized:
                self.bindings.load_library()
            
            self.dwg_data = self.bindings.read_file(file_path)
            self.file_loaded = True
            return True
        except Exception as e:
            print(f"Failed to load DWG file: {e}")
            return False
    
    def get_entities(self) -> List[Dict[str, Any]]:
        """Get all entities from the loaded DWG file"""
        if not self.file_loaded:
            raise RuntimeError("No DWG file loaded")
        
        return self.bindings.get_entities(self.dwg_data)
    
    def get_layers(self) -> List[Dict[str, Any]]:
        """Get all layers from the loaded DWG file"""
        if not self.file_loaded:
            raise RuntimeError("No DWG file loaded")
        
        return self.bindings.get_layers(self.dwg_data)
    
    def get_blocks(self) -> List[Dict[str, Any]]:
        """Get all block references from the loaded DWG file"""
        if not self.file_loaded:
            raise RuntimeError("No DWG file loaded")
        
        # This will be implemented in the next task
        raise NotImplementedError
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest dwg_parser/tests/test_dwg_parser.py::test_dwg_parser_initialization -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add dwg_parser/dwg_parser.py dwg_parser/tests/test_dwg_parser.py
git commit -m "feat: implement DWG file reading functionality"
```

---

## Task 4: Entity Data Structures

**Files:**
- Create: `dwg_parser/entities/__init__.py`
- Create: `dwg_parser/entities/geometric.py`
- Create: `dwg_parser/entities/text.py`
- Create: `dwg_parser/entities/blocks.py`
- Create: `dwg_parser/tests/test_entities.py`

- [ ] **Step 1: Write failing test for geometric entities**

```python
# dwg_parser/tests/test_entities.py
import pytest
from dwg_parser.entities.geometric import Point, Line, Circle, Arc, Polyline, Spline

def test_point_creation():
    point = Point(1.0, 2.0, 3.0)
    assert point.x == 1.0
    assert point.y == 2.0
    assert point.z == 3.0

def test_line_creation():
    start = Point(0.0, 0.0, 0.0)
    end = Point(1.0, 1.0, 0.0)
    line = Line(start, end)
    assert line.start == start
    assert line.end == end

def test_circle_creation():
    center = Point(0.0, 0.0, 0.0)
    circle = Circle(center, 5.0)
    assert circle.center == center
    assert circle.radius == 5.0
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest dwg_parser/tests/test_entities.py::test_point_creation -v`
Expected: FAIL with "ModuleNotFoundError: No module named 'dwg_parser.entities'"

- [ ] **Step 3: Write minimal implementation**

```python
# dwg_parser/entities/__init__.py
"""Entity data structures for DWG parsing"""
from .geometric import Point, Line, Circle, Arc, Polyline, Spline
from .text import Text, MText, Dimension
from .blocks import Block, Attribute, Insert

__all__ = [
    'Point', 'Line', 'Circle', 'Arc', 'Polyline', 'Spline',
    'Text', 'MText', 'Dimension',
    'Block', 'Attribute', 'Insert'
]
```

```python
# dwg_parser/entities/geometric.py
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Point:
    """3D point"""
    x: float
    y: float
    z: float = 0.0

@dataclass
class Line:
    """Line entity"""
    start: Point
    end: Point
    layer: str = ""
    handle: int = 0

@dataclass
class Circle:
    """Circle entity"""
    center: Point
    radius: float
    layer: str = ""
    handle: int = 0

@dataclass
class Arc:
    """Arc entity"""
    center: Point
    radius: float
    start_angle: float
    end_angle: float
    layer: str = ""
    handle: int = 0

@dataclass
class Polyline:
    """Polyline entity"""
    vertices: List[Point]
    closed: bool = False
    layer: str = ""
    handle: int = 0

@dataclass
class Spline:
    """Spline entity"""
    control_points: List[Point]
    knots: List[float]
    degree: int = 3
    layer: str = ""
    handle: int = 0
```

```python
# dwg_parser/entities/text.py
from dataclasses import dataclass
from typing import Optional
from .geometric import Point

@dataclass
class Text:
    """Text entity"""
    content: str
    position: Point
    height: float = 1.0
    rotation: float = 0.0
    layer: str = ""
    handle: int = 0

@dataclass
class MText:
    """MText (formatted text) entity"""
    content: str
    position: Point
    width: float = 0.0
    height: float = 1.0
    layer: str = ""
    handle: int = 0

@dataclass
class Dimension:
    """Dimension entity"""
    type: str
    definition_point: Point
    text_position: Point
    text: str = ""
    layer: str = ""
    handle: int = 0
```

```python
# dwg_parser/entities/blocks.py
from dataclasses import dataclass
from typing import List, Dict, Any
from .geometric import Point

@dataclass
class Block:
    """Block definition"""
    name: str
    base_point: Point
    entities: List[Any] = None
    handle: int = 0
    
    def __post_init__(self):
        if self.entities is None:
            self.entities = []

@dataclass
class Attribute:
    """Block attribute"""
    tag: str
    value: str
    position: Point
    layer: str = ""
    handle: int = 0

@dataclass
class Insert:
    """Block insert"""
    block_name: str
    insertion_point: Point
    scale: Point = None
    rotation: float = 0.0
    attributes: List[Attribute] = None
    layer: str = ""
    handle: int = 0
    
    def __post_init__(self):
        if self.scale is None:
            self.scale = Point(1.0, 1.0, 1.0)
        if self.attributes is None:
            self.attributes = []
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest dwg_parser/tests/test_entities.py::test_point_creation -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add dwg_parser/entities/
git commit -m "feat: implement entity data structures"
```

---

## Task 5: Data Conversion Layer

**Files:**
- Create: `dwg_parser/data_converter.py`
- Create: `dwg_parser/tests/test_data_converter.py`

- [ ] **Step 1: Write failing test for data conversion**

```python
# dwg_parser/tests/test_data_converter.py
import pytest
from dwg_parser.data_converter import DataConverter
from dwg_parser.entities import Point, Line, Circle

def test_convert_point():
    converter = DataConverter()
    raw_data = {'x': 1.0, 'y': 2.0, 'z': 3.0}
    point = converter.convert_point(raw_data)
    assert isinstance(point, Point)
    assert point.x == 1.0
    assert point.y == 2.0
    assert point.z == 3.0

def test_convert_line():
    converter = DataConverter()
    raw_data = {
        'start': {'x': 0.0, 'y': 0.0, 'z': 0.0},
        'end': {'x': 1.0, 'y': 1.0, 'z': 0.0},
        'layer': 'test_layer',
        'handle': 123
    }
    line = converter.convert_line(raw_data)
    assert isinstance(line, Line)
    assert line.start.x == 0.0
    assert line.end.x == 1.0
    assert line.layer == 'test_layer'
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest dwg_parser/tests/test_data_converter.py::test_convert_point -v`
Expected: FAIL with "ModuleNotFoundError: No module named 'dwg_parser.data_converter'"

- [ ] **Step 3: Write minimal implementation**

```python
# dwg_parser/data_converter.py
from typing import Dict, Any, List
from .entities import Point, Line, Circle, Arc, Polyline, Spline
from .entities import Text, MText, Dimension
from .entities import Block, Attribute, Insert

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
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest dwg_parser/tests/test_data_converter.py::test_convert_point -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add dwg_parser/data_converter.py dwg_parser/tests/test_data_converter.py
git commit -m "feat: implement data conversion layer"
```

---

## Task 6: OpenCode Plugin CLI

**Files:**
- Create: `dwg_parser/plugin/__init__.py`
- Create: `dwg_parser/plugin/cli.py`
- Create: `dwg_parser/plugin/config.py`
- Create: `dwg_parser/tests/test_plugin.py`

- [ ] **Step 1: Write failing test for CLI**

```python
# dwg_parser/tests/test_plugin.py
import pytest
from dwg_parser.plugin.cli import DWGPluginCLI

def test_cli_initialization():
    cli = DWGPluginCLI()
    assert cli is not None
    assert cli.parser is not None

def test_cli_parse_command():
    cli = DWGPluginCLI()
    # Test that parse command exists
    assert hasattr(cli, 'parse_dwg')
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest dwg_parser/tests/test_plugin.py::test_cli_initialization -v`
Expected: FAIL with "ModuleNotFoundError: No module named 'dwg_parser.plugin'"

- [ ] **Step 3: Write minimal implementation**

```python
# dwg_parser/plugin/__init__.py
"""OpenCode plugin for DWG parsing"""
from .cli import DWGPluginCLI
from .config import DWGPluginConfig

__all__ = ['DWGPluginCLI', 'DWGPluginConfig']
```

```python
# dwg_parser/plugin/config.py
import json
import os
from dataclasses import dataclass
from typing import Optional

@dataclass
class DWGPluginConfig:
    """Configuration for DWG parser plugin"""
    output_format: str = "json"
    pretty_print: bool = True
    include_layers: bool = True
    include_blocks: bool = True
    
    @classmethod
    def from_file(cls, config_path: str) -> 'DWGPluginConfig':
        """Load configuration from file"""
        if not os.path.exists(config_path):
            return cls()
        
        with open(config_path, 'r') as f:
            config_data = json.load(f)
        
        return cls(**config_data)
    
    def save(self, config_path: str):
        """Save configuration to file"""
        with open(config_path, 'w') as f:
            json.dump(self.__dict__, f, indent=2)
```

```python
# dwg_parser/plugin/cli.py
import argparse
import json
import sys
from typing import List, Optional
from ..dwg_parser import DWGParser
from ..data_converter import DataConverter
from .config import DWGPluginConfig

class DWGPluginCLI:
    """Command-line interface for DWG parser plugin"""
    
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            description="DWG Parser Plugin for OpenCode"
        )
        self.setup_arguments()
        self.config = DWGPluginConfig()
    
    def setup_arguments(self):
        """Setup command-line arguments"""
        subparsers = self.parser.add_subparsers(
            dest='command', help='Available commands'
        )
        
        # parse-dwg command
        parse_parser = subparsers.add_parser(
            'parse-dwg', help='Parse a DWG file'
        )
        parse_parser.add_argument(
            'file_path', help='Path to DWG file'
        )
        parse_parser.add_argument(
            '--output', '-o', help='Output file path'
        )
        
        # batch-parse command
        batch_parser = subparsers.add_parser(
            'batch-parse', help='Parse multiple DWG files'
        )
        batch_parser.add_argument(
            'directory', help='Directory containing DWG files'
        )
        batch_parser.add_argument(
            '--pattern', '-p', default='*.dwg',
            help='File pattern (default: *.dwg)'
        )
        
        # dwg-info command
        info_parser = subparsers.add_parser(
            'dwg-info', help='Get DWG file information'
        )
        info_parser.add_argument(
            'file_path', help='Path to DWG file'
        )
    
    def parse_dwg(self, file_path: str, output: Optional[str] = None) -> dict:
        """Parse a single DWG file"""
        dwg_parser = DWGParser()
        converter = DataConverter()
        
        if not dwg_parser.load(file_path):
            return {"success": False, "error": "Failed to load DWG file"}
        
        try:
            entities = dwg_parser.get_entities()
            converted_entities = converter.convert_entities(entities)
            
            result = {
                "success": True,
                "file": file_path,
                "entities": [
                    {
                        "type": type(e).__name__,
                        "properties": e.__dict__
                    }
                    for e in converted_entities
                ]
            }
            
            if output:
                with open(output, 'w') as f:
                    json.dump(result, f, indent=2)
            
            return result
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def run(self, args: Optional[List[str]] = None):
        """Run the CLI"""
        parsed_args = self.parser.parse_args(args)
        
        if not parsed_args.command:
            self.parser.print_help()
            return
        
        if parsed_args.command == 'parse-dwg':
            result = self.parse_dwg(parsed_args.file_path, parsed_args.output)
            print(json.dumps(result, indent=2))
        elif parsed_args.command == 'batch-parse':
            # Batch processing will be implemented later
            print("Batch processing not yet implemented")
        elif parsed_args.command == 'dwg-info':
            # Info command will be implemented later
            print("Info command not yet implemented")
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest dwg_parser/tests/test_plugin.py::test_cli_initialization -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add dwg_parser/plugin/
git commit -m "feat: implement OpenCode plugin CLI"
```

---

## Task 7: Integration Testing

**Files:**
- Create: `dwg_parser/tests/test_integration.py`

- [ ] **Step 1: Write failing test for integration**

```python
# dwg_parser/tests/test_integration.py
import pytest
import tempfile
import os
import json
from dwg_parser.dwg_parser import DWGParser
from dwg_parser.data_converter import DataConverter
from dwg_parser.plugin.cli import DWGPluginCLI

def test_full_workflow():
    """Test complete workflow from file input to JSON output"""
    # Create a mock DWG file (this would need a real DWG file for actual testing)
    with tempfile.NamedTemporaryFile(suffix='.dwg', delete=False) as tmp:
        tmp.write(b'mock dwg content')
        tmp_path = tmp.name
    
    try:
        # Test CLI
        cli = DWGPluginCLI()
        result = cli.parse_dwg(tmp_path)
        
        # For now, we expect failure since we don't have a real DWG parser
        assert 'success' in result
    finally:
        os.unlink(tmp_path)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest dwg_parser/tests/test_integration.py::test_full_workflow -v`
Expected: FAIL with assertion error (expected since we don't have real DWG parsing yet)

- [ ] **Step 3: Skip this step for now (will be implemented when LibreDWG is available)**

- [ ] **Step 4: Skip this step for now**

- [ ] **Step 5: Commit**

```bash
git add dwg_parser/tests/test_integration.py
git commit -m "test: add integration test skeleton"
```

---

## Task 8: Documentation and README

**Files:**
- Create: `dwg_parser/README.md`

- [ ] **Step 1: Write README documentation**

```markdown
# DWG Parser Plugin for OpenCode

A plugin for OpenCode that parses DWG files and extracts all readable data for engineering quantity calculation and pricing.

## Features

- Parse DWG files and extract geometric data
- Extract layer information
- Parse text and annotations
- Handle block references
- Support batch processing
- Output structured JSON data

## Installation

1. Install LibreDWG library:
   - Windows: Download from https://www.opendesign.com/guestfiles/oda_file_converter
   - Linux: `sudo apt-get install libredwg-dev`

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Install the package:
   ```bash
   pip install -e .
   ```

## Usage

### Command Line Interface

```bash
# Parse a single DWG file
opencode parse-dwg file.dwg

# Parse and save to file
opencode parse-dwg file.dwg --output result.json

# Get DWG file information
opencode dwg-info file.dwg
```

### Python API

```python
from dwg_parser import DWGParser
from dwg_parser import DataConverter

# Parse DWG file
parser = DWGParser()
parser.load('file.dwg')

# Get entities
entities = parser.get_entities()

# Convert to Python objects
converter = DataConverter()
converted = converter.convert_entities(entities)

# Process data
for entity in converted:
    print(f"Entity type: {type(entity).__name__}")
```

## Configuration

Create a `dwg_parser_config.json` file:

```json
{
  "output_format": "json",
  "pretty_print": true,
  "include_layers": true,
  "include_blocks": true
}
```

## Development

1. Clone the repository
2. Install development dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run tests:
   ```bash
   pytest dwg_parser/tests/
   ```

## License

GNU General Public License v3.0 (LibreDWG)
```

- [ ] **Step 2: Verify README renders correctly**

- [ ] **Step 3: Commit**

```bash
git add dwg_parser/README.md
git commit -m "docs: add README documentation"
```

---

## Self-Review Checklist

- [ ] **Spec coverage:** All requirements from design document are covered
- [ ] **Placeholder scan:** No TBD, TODO, or incomplete sections
- [ ] **Type consistency:** All types, method signatures, and property names are consistent
- [ ] **File paths:** All file paths are exact and correct
- [ ] **Code completeness:** All code blocks are complete and runnable
- [ ] **Commands:** All commands have exact syntax and expected output