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