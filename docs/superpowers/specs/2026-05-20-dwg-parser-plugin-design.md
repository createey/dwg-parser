# DWG Parser Plugin for OpenCode

## Overview

This design document outlines the implementation of a DWG file parser plugin for OpenCode, enabling users to extract and analyze DWG file data for engineering quantity calculation and pricing.

## Requirements

### Functional Requirements

1. **DWG File Parsing**: Parse DWG files and extract all readable data
2. **Data Extraction**: Extract geometric data, layer information, text/annotations, and block references
3. **Output Format**: Return structured data in JSON format
4. **Batch Processing**: Support processing multiple DWG files
5. **Error Handling**: Provide detailed error messages for various failure scenarios

### Non-Functional Requirements

1. **Performance**: Efficient parsing of large DWG files
2. **Reliability**: Robust error handling and recovery
3. **Usability**: Simple API and command-line interface
4. **Compatibility**: Support Windows platform (primary target)

## Architecture

The plugin will be structured in three layers:

### 1. DWG Parsing Layer

- **Responsibility**: Interface with LibreDWG library
- **Components**:
  - LibreDWG Python bindings
  - Low-level file I/O operations
  - Memory management

### 2. Data Conversion Layer

- **Responsibility**: Convert LibreDWG data to Python objects
- **Components**:
  - Entity parser (points, lines, circles, arcs, etc.)
  - Layer information extractor
  - Text and annotation processor
  - Block reference handler

### 3. OpenCode Plugin Layer

- **Responsibility**: Provide user interface and integration
- **Components**:
  - Command-line interface
  - API endpoints
  - Configuration management

## Data Flow

```
User Request → Plugin Layer → Data Conversion Layer → DWG Parsing Layer → File System
     ↓
Response (JSON) ← Plugin Layer ← Data Conversion Layer ← DWG Parsing Layer
```

## Component Details

### DWG Parsing Layer

#### LibreDWG Integration

- Use LibreDWG library (GNU project, completely free)
- Python bindings via ctypes or cffi
- Support DWG versions R13 through R2024

#### API Design

```python
class DWGParser:
    def __init__(self):
        self.libredwg = None
    
    def load(self, file_path: str) -> bool:
        """Load a DWG file"""
        pass
    
    def get_entities(self) -> List[Entity]:
        """Get all entities from the DWG file"""
        pass
    
    def get_layers(self) -> List[Layer]:
        """Get all layers from the DWG file"""
        pass
    
    def get_blocks(self) -> List[Block]:
        """Get all block references from the DWG file"""
        pass
```

### Data Conversion Layer

#### Entity Types

1. **Geometric Entities**
   - Point (x, y, z coordinates)
   - Line (start point, end point)
   - Circle (center, radius)
   - Arc (center, radius, start angle, end angle)
   - Polyline (vertices)
   - Spline (control points, knots)

2. **Text Entities**
   - Text (content, position, style)
   - MText (formatted text content)
   - Dimensions (dimension lines, text)

3. **Block References**
   - Insert (block name, insertion point, scale, rotation)
   - Attribute (tag, value, position)

#### Data Structures

```python
@dataclass
class Entity:
    type: str
    layer: str
    handle: int
    properties: Dict[str, Any]

@dataclass
class Point:
    x: float
    y: float
    z: float

@dataclass
class Layer:
    name: str
    color: int
    linetype: str
    frozen: bool
    locked: bool

@dataclass
class Block:
    name: str
    entities: List[Entity]
    base_point: Point
```

### OpenCode Plugin Layer

#### Commands

1. **parse-dwg**: Parse a single DWG file
   ```
   opencode parse-dwg <file_path> [--output <output_path>]
   ```

2. **batch-parse**: Parse multiple DWG files
   ```
   opencode batch-parse <directory> [--pattern <pattern>]
   ```

3. **dwg-info**: Get summary information about a DWG file
   ```
   opencode dwg-info <file_path>
   ```

#### API Endpoints

1. **POST /dwg/parse**: Parse a DWG file
2. **POST /dwg/batch**: Batch parse DWG files
3. **GET /dwg/info**: Get DWG file information

## Error Handling

### Error Categories

1. **File System Errors**
   - File not found
   - Permission denied
   - Disk full

2. **Format Errors**
   - Invalid DWG file
   - Unsupported DWG version
   - Corrupted file

3. **Parsing Errors**
   - LibreDWG initialization failed
   - Memory allocation failed
   - Entity parsing failed

4. **Conversion Errors**
   - Data type conversion failed
   - Invalid coordinates
   - Missing required fields

### Error Response Format

```json
{
  "success": false,
  "error": {
    "code": "PARSE_ERROR",
    "message": "Failed to parse DWG file",
    "details": "Unsupported DWG version: R12",
    "file": "example.dwg",
    "line": 1234
  }
}
```

## Testing Strategy

### Unit Tests

1. Test individual entity parsing
2. Test layer information extraction
3. Test text and annotation parsing
4. Test block reference handling

### Integration Tests

1. Test complete DWG file parsing
2. Test batch processing
3. Test error handling scenarios
4. Test performance with large files

### End-to-End Tests

1. Test full workflow from file input to JSON output
2. Test with real-world DWG files
3. Test edge cases (empty files, corrupted files)

## Implementation Plan

### Phase 1: Setup and Basic Parsing

1. Set up development environment
2. Install and configure LibreDWG
3. Implement basic DWG file loading
4. Create initial Python bindings

### Phase 2: Data Extraction

1. Implement geometric entity parsing
2. Add layer information extraction
3. Implement text and annotation parsing
4. Add block reference handling

### Phase 3: OpenCode Integration

1. Create command-line interface
2. Implement API endpoints
3. Add configuration management
4. Create documentation

### Phase 4: Testing and Optimization

1. Write comprehensive tests
2. Optimize performance
3. Add error handling
4. Create user documentation

## Dependencies

### External Libraries

1. **LibreDWG**: GNU library for DWG file parsing
2. **Python**: Version 3.8 or higher
3. **ctypes/cffi**: For Python-C interop

### Build Requirements

1. C compiler (GCC or MSVC)
2. Python development headers
3. LibreDWG development files

## Security Considerations

1. **Input Validation**: Validate file paths and content
2. **Memory Safety**: Use safe memory management practices
3. **Error Handling**: Prevent information leakage through error messages
4. **File Permissions**: Respect file system permissions

## Future Enhancements

1. **Write Support**: Add ability to create/modify DWG files
2. **Format Conversion**: Support DXF, PDF, and image export
3. **Advanced Analysis**: Add geometric analysis and measurement tools
4. **GUI Interface**: Create graphical user interface for visualization