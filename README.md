# Inticore Estimation Automation

A Streamlit-based application for automated cost estimation of CAD parts for manufacturing.

## Features

- **CAD File Processing**: Upload and process STEP, STL, and OBJ files
- **Geometry Extraction**: Automatic extraction of volume, surface area, weight, and features
- **Cost Estimation**: Calculate material, machining, tooling, and finishing costs
- **Real-time Processing**: Live progress updates during file processing
- **Results Dashboard**: Interactive charts and detailed cost breakdowns
- **Estimate History**: Store and view past estimates
- **Export Functionality**: Download estimates as JSON reports

## Installation

1. **Clone or download the project files**

2. **Install Python dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:

   ```bash
   streamlit run app.py
   ```

4. **Open your browser** and navigate to `http://localhost:8501`

## Usage

### Step 1: Upload & Configure

- Upload a CAD file (STEP, STL, or OBJ format)
- Select material type (AlSi7Mg, AlSi10Mg, AlSi12, Steel)
- Enter annual quantity
- Choose surface finish and testing requirements
- Click "Process File"

### Step 2: Processing

- Watch real-time progress as the system:
  - Validates the uploaded file
  - Extracts geometric properties
  - Detects features (holes, faces, vertices)
  - Calculates manufacturing costs

### Step 3: Results Dashboard

- View detailed cost breakdown
- See cost distribution charts
- Review material, machining, and tooling costs
- Check lead time estimates
- Save or download the estimate

### Step 4: Estimate History

- View all previous estimates
- Access detailed information from past calculations

## File Structure

```
inticore-estimation/
├── app.py                 # Main Streamlit application
├── cad_processor.py       # CAD file processing engine
├── estimation_engine.py   # Cost calculation logic
├── config.py             # Configuration and rate cards
├── database.py           # Database operations
├── requirements.txt      # Python dependencies
├── .streamlit/
│   └── config.toml      # Streamlit configuration
├── data/
│   ├── rate_cards.json  # Material and rate data
│   └── estimates.db     # SQLite database (auto-created)
└── README.md            # This file
```

## Supported File Formats

- **STL** (.stl) - Stereolithography format
- **OBJ** (.obj) - Wavefront OBJ format
- **PLY** (.ply) - Polygon File Format
- **OFF** (.off) - Object File Format
- **GLB** (.glb) - Binary glTF format
- **GLTF** (.gltf) - GL Transmission Format

## Cost Calculation Components

1. **Material Cost**: Based on part weight, material density, and yield percentage
2. **Machining Cost**: Calculated from estimated machining time and machine rates
3. **Tooling Cost**: Amortized tooling cost based on part complexity and quantity
4. **Finishing Cost**: Surface treatment costs (anodizing, coating, etc.)
5. **Testing Cost**: Quality control and testing requirements
6. **Overhead**: 15% overhead on total costs
7. **Scrap Allowance**: 5% allowance for material waste

## Configuration

Edit `config.py` to modify:

- Material properties and costs
- Machining rates
- Finishing and testing costs
- Tooling factors
- Overhead and scrap percentages

## Database

The application uses SQLite to store:

- Estimate history
- CAD properties
- Cost breakdowns
- Configuration parameters

Database file is automatically created at `data/estimates.db`

## Troubleshooting

### Common Issues

1. **File Upload Errors**: Ensure the file is in a supported format and not corrupted
2. **Processing Errors**: Large files (>100MB) may take longer to process
3. **Memory Issues**: For very large files, consider using a machine with more RAM

### Dependencies

If you encounter import errors, ensure all dependencies are installed:

```bash
pip install --upgrade -r requirements.txt
```

## Development

To extend the application:

1. **Add new materials**: Update `MATERIALS` in `config.py`
2. **Modify cost calculations**: Edit `estimation_engine.py`
3. **Add new file formats**: Extend `cad_processor.py`
4. **Customize UI**: Modify `app.py` and add custom CSS

## Deployment

### Local Development

```bash
streamlit run app.py
```

### Streamlit Cloud (Recommended)

1. Push code to GitHub
2. Connect to Streamlit Cloud
3. Deploy automatically

### Docker

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app.py"]
```

## License

This project is for internal use at Inticore.

## Support

For technical support or feature requests, contact the development team.
