# CFD Workflow Automation and Best Practices

This guide covers automated workflows, scripting techniques, and best practices for efficient CFD operations.

## Table of Contents

- [Automation Philosophy](#automation-philosophy)
- [Scripting Frameworks](#scripting-frameworks)
- [Parametric Studies](#parametric-studies)
- [Mesh Convergence Studies](#mesh-convergence-studies)
- [High-Performance Computing](#high-performance-computing)
- [Quality Assurance](#quality-assurance)
- [Data Management](#data-management)

## Automation Philosophy

### Why Automate CFD?
- **Reproducibility**: Consistent results across runs
- **Efficiency**: Reduce manual effort and errors
- **Scalability**: Handle large parameter studies
- **Documentation**: Automatic logging and reporting
- **Quality**: Standardized procedures and checks

### Automation Levels
1. **Basic**: Shell scripts for common tasks
2. **Intermediate**: Python frameworks for workflows
3. **Advanced**: Complete automation with monitoring
4. **Enterprise**: CI/CD for CFD development

## Scripting Frameworks

### Python CFD Framework
```python
#!/usr/bin/env python3
"""
Advanced CFD Workflow Framework
Supports multiple solvers and automated analysis
"""

import os
import subprocess
import shutil
import json
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from datetime import datetime
import logging

class CFDWorkflow:
    def __init__(self, config_file):
        """Initialize workflow from configuration file"""
        with open(config_file, 'r') as f:
            self.config = json.load(f)
        
        self.setup_logging()
        self.create_workspace()
        
    def setup_logging(self):
        """Setup logging system"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('cfd_workflow.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def create_workspace(self):
        """Create organized workspace structure"""
        self.workspace = Path(self.config['workspace_name'])
        directories = [
            'cases', 'results', 'scripts', 'geometry', 
            'mesh', 'validation', 'reports'
        ]
        
        for dir_name in directories:
            (self.workspace / dir_name).mkdir(parents=True, exist_ok=True)
            
        self.logger.info(f"Workspace created: {self.workspace}")
        
    def parametric_study(self):
        """Run parametric study"""
        parameters = self.config['parameters']
        results = []
        
        for i, param_set in enumerate(self.generate_parameter_combinations(parameters)):
            case_name = f"case_{i:04d}"
            self.logger.info(f"Running case: {case_name}")
            
            try:
                case_result = self.run_single_case(case_name, param_set)
                results.append({
                    'case': case_name,
                    'parameters': param_set,
                    'results': case_result
                })
            except Exception as e:
                self.logger.error(f"Case {case_name} failed: {str(e)}")
                continue
                
        self.save_results(results)
        self.generate_report(results)
        
    def generate_parameter_combinations(self, parameters):
        """Generate all parameter combinations"""
        import itertools
        
        param_names = list(parameters.keys())
        param_values = [parameters[name] for name in param_names]
        
        for combination in itertools.product(*param_values):
            yield dict(zip(param_names, combination))
            
    def run_single_case(self, case_name, parameters):
        """Run a single CFD case"""
        case_dir = self.workspace / 'cases' / case_name
        case_dir.mkdir(exist_ok=True)
        
        # Copy template
        template_dir = Path(self.config['template_case'])
        self.copy_template(template_dir, case_dir)
        
        # Modify parameters
        self.modify_case_parameters(case_dir, parameters)
        
        # Generate mesh
        self.generate_mesh(case_dir)
        
        # Run simulation
        results = self.run_simulation(case_dir)
        
        # Post-process
        post_results = self.post_process(case_dir)
        
        return {**results, **post_results}
        
    def copy_template(self, src, dst):
        """Copy template case with filtering"""
        if dst.exists():
            shutil.rmtree(dst)
        shutil.copytree(src, dst)
        
    def modify_case_parameters(self, case_dir, parameters):
        """Modify case files with parameters"""
        replacements = {}
        
        for param_name, param_value in parameters.items():
            replacements[f"__{param_name.upper()}__"] = str(param_value)
        
        # Process all template files
        for file_path in case_dir.rglob("*"):
            if file_path.is_file() and file_path.suffix in ['.cfg', '.geo', '']:
                self.replace_in_file(file_path, replacements)
                
    def replace_in_file(self, file_path, replacements):
        """Replace placeholders in file"""
        try:
            with open(file_path, 'r') as f:
                content = f.read()
            
            for placeholder, value in replacements.items():
                content = content.replace(placeholder, value)
            
            with open(file_path, 'w') as f:
                f.write(content)
        except UnicodeDecodeError:
            # Skip binary files
            pass
            
    def generate_mesh(self, case_dir):
        """Generate mesh for case"""
        os.chdir(case_dir)
        
        solver = self.config['solver']
        if solver == 'openfoam':
            subprocess.run(['blockMesh'], check=True, capture_output=True)
            subprocess.run(['checkMesh'], check=True, capture_output=True)
        elif solver == 'su2':
            # SU2 mesh generation if needed
            pass
            
    def run_simulation(self, case_dir):
        """Run CFD simulation"""
        os.chdir(case_dir)
        
        solver = self.config['solver']
        solver_executable = self.config['solver_executable']
        
        start_time = datetime.now()
        
        if self.config.get('parallel', False):
            np_proc = self.config.get('processors', 4)
            if solver == 'openfoam':
                subprocess.run(['decomposePar'], check=True)
                result = subprocess.run(
                    ['mpirun', '-np', str(np_proc), solver_executable, '-parallel'],
                    check=True, capture_output=True, text=True
                )
                subprocess.run(['reconstructPar'], check=True)
            else:
                result = subprocess.run(
                    ['mpirun', '-np', str(np_proc), solver_executable],
                    check=True, capture_output=True, text=True
                )
        else:
            result = subprocess.run(
                [solver_executable], 
                check=True, capture_output=True, text=True
            )
        
        end_time = datetime.now()
        runtime = (end_time - start_time).total_seconds()
        
        return {
            'runtime': runtime,
            'converged': self.check_convergence(case_dir),
            'iterations': self.extract_iterations(result.stdout)
        }
        
    def check_convergence(self, case_dir):
        """Check if simulation converged"""
        # Implementation depends on solver
        # Look for residual files, convergence criteria, etc.
        return True  # Placeholder
        
    def extract_iterations(self, stdout):
        """Extract iteration count from solver output"""
        # Parser depends on solver
        return 0  # Placeholder
        
    def post_process(self, case_dir):
        """Post-process simulation results"""
        os.chdir(case_dir)
        
        # Run post-processing utilities
        if self.config['solver'] == 'openfoam':
            # Sample data
            subprocess.run(['sample'], check=True)
            
            # Calculate forces
            subprocess.run([
                self.config['solver_executable'], 
                '-postProcess', '-func', 'forceCoeffs'
            ], check=True)
            
            # Extract results
            return self.extract_openfoam_results(case_dir)
        
        return {}
        
    def extract_openfoam_results(self, case_dir):
        """Extract OpenFOAM results"""
        results = {}
        
        # Force coefficients
        force_file = case_dir / 'postProcessing/forceCoeffs/0/forceCoeffs.dat'
        if force_file.exists():
            data = np.loadtxt(force_file, comments='#')
            if len(data.shape) > 1:
                results['Cd'] = data[-1, 1]
                results['Cl'] = data[-1, 2]
        
        # Pressure drop
        # Mass flow rate
        # Heat transfer rates
        # etc.
        
        return results
        
    def save_results(self, results):
        """Save results to file"""
        results_file = self.workspace / 'results' / 'parametric_study.json'
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2)
            
    def generate_report(self, results):
        """Generate automated report"""
        report_dir = self.workspace / 'reports'
        
        # Extract data for plotting
        parameters = []
        drag_coeffs = []
        
        for result in results:
            if 'Cd' in result['results']:
                parameters.append(result['parameters'])
                drag_coeffs.append(result['results']['Cd'])
        
        # Generate plots
        self.plot_parameter_sensitivity(parameters, drag_coeffs, report_dir)
        
        # Generate HTML report
        self.generate_html_report(results, report_dir)
        
    def plot_parameter_sensitivity(self, parameters, values, output_dir):
        """Plot parameter sensitivity"""
        if not parameters:
            return
            
        param_names = list(parameters[0].keys())
        
        for param_name in param_names:
            param_values = [p[param_name] for p in parameters]
            
            plt.figure(figsize=(10, 6))
            plt.scatter(param_values, values)
            plt.xlabel(param_name)
            plt.ylabel('Drag Coefficient')
            plt.title(f'Sensitivity to {param_name}')
            plt.grid(True)
            
            plt.savefig(output_dir / f'sensitivity_{param_name}.png', dpi=300)
            plt.close()
            
    def generate_html_report(self, results, output_dir):
        """Generate HTML report"""
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>CFD Parametric Study Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; }}
                table {{ border-collapse: collapse; width: 100%; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #f2f2f2; }}
                .summary {{ background-color: #e7f3ff; padding: 20px; margin: 20px 0; }}
            </style>
        </head>
        <body>
            <h1>CFD Parametric Study Report</h1>
            <div class="summary">
                <h2>Summary</h2>
                <p>Total cases: {len(results)}</p>
                <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            </div>
            
            <h2>Results Table</h2>
            <table>
                <tr>
                    <th>Case</th>
                    <th>Parameters</th>
                    <th>Results</th>
                </tr>
        """
        
        for result in results:
            html_content += f"""
                <tr>
                    <td>{result['case']}</td>
                    <td>{json.dumps(result['parameters'], indent=2)}</td>
                    <td>{json.dumps(result['results'], indent=2)}</td>
                </tr>
            """
        
        html_content += """
            </table>
        </body>
        </html>
        """
        
        with open(output_dir / 'report.html', 'w') as f:
            f.write(html_content)

# Configuration file example
config_example = {
    "workspace_name": "parametric_study",
    "template_case": "template_airfoil",
    "solver": "openfoam",
    "solver_executable": "simpleFoam",
    "parallel": True,
    "processors": 4,
    "parameters": {
        "velocity": [10, 20, 30],
        "angle_of_attack": [0, 5, 10, 15],
        "viscosity": [1e-5, 1e-4]
    }
}

# Usage example
if __name__ == "__main__":
    # Save example config
    with open('config.json', 'w') as f:
        json.dump(config_example, f, indent=2)
    
    # Run workflow
    workflow = CFDWorkflow('config.json')
    workflow.parametric_study()
```

### Bash Automation Scripts

#### Mesh Convergence Study
```bash
#!/bin/bash
# mesh_convergence.sh

set -e  # Exit on error

# Configuration
CASE_NAME="mesh_study"
TEMPLATE_CASE="template"
MESH_SIZES=(0.1 0.05 0.025 0.0125 0.00625)
SOLVER="simpleFoam"
RESULTS_FILE="convergence_results.dat"

# Initialize results file
echo "# Mesh_Size Cells Cd Cl Runtime" > $RESULTS_FILE

for size in "${MESH_SIZES[@]}"; do
    echo "Processing mesh size: $size"
    
    # Create case directory
    CURRENT_CASE="${CASE_NAME}_${size}"
    
    if [ -d "$CURRENT_CASE" ]; then
        rm -rf "$CURRENT_CASE"
    fi
    
    cp -r "$TEMPLATE_CASE" "$CURRENT_CASE"
    cd "$CURRENT_CASE"
    
    # Modify mesh size in blockMeshDict
    sed -i "s/MESH_SIZE_PLACEHOLDER/$size/g" system/blockMeshDict
    
    # Generate mesh
    echo "Generating mesh..."
    blockMesh > log.blockMesh 2>&1
    
    # Check mesh quality
    checkMesh > log.checkMesh 2>&1
    
    # Count cells
    CELL_COUNT=$(grep "cells:" log.checkMesh | awk '{print $2}')
    
    # Run simulation
    echo "Running simulation..."
    START_TIME=$(date +%s)
    $SOLVER > log.$SOLVER 2>&1
    END_TIME=$(date +%s)
    RUNTIME=$((END_TIME - START_TIME))
    
    # Extract forces
    $SOLVER -postProcess -func forceCoeffs > log.forces 2>&1
    
    # Get latest force coefficients
    FORCE_FILE=$(find postProcessing/forceCoeffs -name "forceCoeffs.dat" | head -1)
    if [ -f "$FORCE_FILE" ]; then
        LAST_LINE=$(tail -1 "$FORCE_FILE")
        CD=$(echo $LAST_LINE | awk '{print $2}')
        CL=$(echo $LAST_LINE | awk '{print $3}')
    else
        CD="N/A"
        CL="N/A"
    fi
    
    # Append to results
    echo "$size $CELL_COUNT $CD $CL $RUNTIME" >> ../$RESULTS_FILE
    
    cd ..
    
    echo "Completed mesh size: $size"
    echo "Cells: $CELL_COUNT, Cd: $CD, Cl: $CL, Runtime: ${RUNTIME}s"
    echo "----------------------------------------"
done

# Generate convergence plot
python3 -c "
import numpy as np
import matplotlib.pyplot as plt

data = np.loadtxt('$RESULTS_FILE')
mesh_sizes = data[:, 0]
cells = data[:, 1]
cd_values = data[:, 2]

plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
plt.loglog(cells, cd_values, 'o-')
plt.xlabel('Number of Cells')
plt.ylabel('Drag Coefficient')
plt.title('Mesh Convergence Study')
plt.grid(True)

plt.subplot(1, 2, 2)
plt.semilogx(mesh_sizes, cd_values, 's-')
plt.xlabel('Mesh Size')
plt.ylabel('Drag Coefficient')
plt.title('Drag vs Mesh Size')
plt.grid(True)

plt.tight_layout()
plt.savefig('mesh_convergence.png', dpi=300)
print('Convergence plot saved as mesh_convergence.png')
"

echo "Mesh convergence study completed!"
echo "Results saved in: $RESULTS_FILE"
echo "Plot saved as: mesh_convergence.png"
```

#### Automated Quality Checks
```bash
#!/bin/bash
# quality_check.sh

# Quality assurance script for CFD cases

check_mesh_quality() {
    local case_dir=$1
    
    cd "$case_dir"
    
    echo "Checking mesh quality for: $case_dir"
    
    # Run checkMesh
    checkMesh -allGeometry -allTopology > mesh_quality.log 2>&1
    
    # Extract quality metrics
    local max_skewness=$(grep "Max skewness" mesh_quality.log | awk '{print $4}')
    local max_aspect_ratio=$(grep "Max aspect ratio" mesh_quality.log | awk '{print $5}')
    local min_orthogonality=$(grep "Minimum face orthogonality" mesh_quality.log | awk '{print $5}')
    
    # Check against thresholds
    local quality_ok=true
    
    if (( $(echo "$max_skewness > 0.85" | bc -l) )); then
        echo "WARNING: High skewness detected: $max_skewness"
        quality_ok=false
    fi
    
    if (( $(echo "$max_aspect_ratio > 1000" | bc -l) )); then
        echo "WARNING: High aspect ratio detected: $max_aspect_ratio"
        quality_ok=false
    fi
    
    if (( $(echo "$min_orthogonality < 0.1" | bc -l) )); then
        echo "WARNING: Low orthogonality detected: $min_orthogonality"
        quality_ok=false
    fi
    
    if [ "$quality_ok" = true ]; then
        echo "✓ Mesh quality passed for: $case_dir"
        return 0
    else
        echo "✗ Mesh quality issues detected for: $case_dir"
        return 1
    fi
}

check_convergence() {
    local case_dir=$1
    
    cd "$case_dir"
    
    echo "Checking convergence for: $case_dir"
    
    # Check if log file exists
    if [ ! -f "log.simpleFoam" ]; then
        echo "✗ No solver log found"
        return 1
    fi
    
    # Extract final residuals
    local u_residual=$(grep "Solving for Ux" log.simpleFoam | tail -1 | awk '{print $9}' | tr -d ',')
    local p_residual=$(grep "Solving for p" log.simpleFoam | tail -1 | awk '{print $9}' | tr -d ',')
    
    # Check convergence criteria
    if (( $(echo "$u_residual < 1e-6" | bc -l) )) && (( $(echo "$p_residual < 1e-6" | bc -l) )); then
        echo "✓ Convergence achieved for: $case_dir"
        return 0
    else
        echo "✗ Poor convergence for: $case_dir (U: $u_residual, p: $p_residual)"
        return 1
    fi
}

# Main quality check loop
for case_dir in case_*; do
    if [ -d "$case_dir" ]; then
        echo "======================================="
        
        # Check mesh quality
        if ! check_mesh_quality "$case_dir"; then
            echo "Consider mesh refinement for: $case_dir"
        fi
        
        # Check convergence
        if ! check_convergence "$case_dir"; then
            echo "Consider adjusting solver settings for: $case_dir"
        fi
        
        echo ""
    fi
done

echo "Quality check completed!"
```

## Best Practices Summary

### Workflow Organization
```
project/
├── config/                 # Configuration files
├── templates/              # Case templates
├── scripts/               # Automation scripts
├── cases/                 # Individual simulations
├── results/               # Processed results
├── validation/            # Experimental data
├── reports/               # Generated reports
└── documentation/         # Project documentation
```

### Version Control Integration
```bash
# Git hooks for CFD projects
# pre-commit hook
#!/bin/bash
# Check mesh quality before commit
for case in cases/*/; do
    check_mesh_quality "$case"
done
```

### Continuous Integration
```yaml
# .github/workflows/cfd-tests.yml
name: CFD Validation Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    
    - name: Install OpenFOAM
      run: |
        sudo apt update
        sudo apt install openfoam11
        
    - name: Run validation cases
      run: |
        source /opt/openfoam11/etc/bashrc
        ./scripts/run_validation.sh
        
    - name: Check results
      run: |
        python3 scripts/validate_results.py
```

This comprehensive automation framework provides the foundation for efficient, reproducible CFD workflows at any scale.
