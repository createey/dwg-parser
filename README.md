# DWG Parser

DXF Parser - Extract layer information and text annotations from DXF files.

## Features

- Read DXF files using ezdxf library
- Extract layer information (name, color, linetype)
- Extract TEXT and MTEXT entities
- Export data to JSON format
- CLI interface for parsing DXF files

## Installation

```bash
pip install -r requirements.txt
pip install -e .
```

## Usage

```bash
# Parse DXF file
python dxf_parser.py input.dxf output.json
```

## License

MIT