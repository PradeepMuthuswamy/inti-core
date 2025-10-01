"""
Estimation Engine for Inticore Estimation Automation
Calculates costs for casting, machining, tooling, and finishing
"""

from typing import Dict, Any
import math
from config import (
    MATERIALS, MACHINING_RATES, FINISHING_COSTS, 
    TESTING_COSTS, TOOLING_FACTORS, OVERHEAD_PERCENTAGE, SCRAP_ALLOWANCE
)

class EstimationEngine:
    """Calculates manufacturing costs based on CAD properties"""
    
    def __init__(self):
        self.materials = MATERIALS
        self.machining_rates = MACHINING_RATES
        self.finishing_costs = FINISHING_COSTS
        self.testing_costs = TESTING_COSTS
        self.tooling_factors = TOOLING_FACTORS
    
    def calculate_estimate(self, 
                          cad_properties: Dict[str, Any], 
                          material: str, 
                          quantity: int, 
                          finish: str, 
                          testing: str = "None") -> Dict[str, Any]:
        """
        Calculate complete cost estimate
        
        Args:
            cad_properties: Properties extracted from CAD file
            material: Material type (e.g., 'AlSi10Mg')
            quantity: Annual quantity
            finish: Surface finish type
            testing: Testing requirements
            
        Returns:
            Dictionary with cost breakdown and calculation steps
        """
        
        # Initialize calculation steps
        calculation_steps = []
        
        # Step 1: Material cost calculation
        material_result = self._calculate_material_cost_with_steps(cad_properties, material)
        material_cost = material_result['cost']
        calculation_steps.extend(material_result['steps'])
        
        # Step 2: Machining cost calculation
        machining_result = self._calculate_machining_cost_with_steps(cad_properties)
        machining_cost = machining_result['cost']
        calculation_steps.extend(machining_result['steps'])
        
        # Step 3: Tooling cost calculation
        tooling_result = self._calculate_tooling_cost_with_steps(cad_properties, quantity)
        tooling_cost = tooling_result['cost']
        calculation_steps.extend(tooling_result['steps'])
        
        # Step 4: Finishing cost
        finishing_cost = self.finishing_costs.get(finish, 0)
        calculation_steps.append({
            'step': 'Finishing Cost',
            'description': f'Surface finish: {finish}',
            'calculation': f'₹{finishing_cost} per piece',
            'cost': finishing_cost
        })
        
        # Step 5: Testing cost
        testing_cost = self.testing_costs.get(testing, 0)
        calculation_steps.append({
            'step': 'Testing Cost',
            'description': f'Testing requirement: {testing}',
            'calculation': f'₹{testing_cost} per piece',
            'cost': testing_cost
        })
        
        # Step 6: Calculate subtotal
        subtotal = material_cost + machining_cost + tooling_cost + finishing_cost + testing_cost
        calculation_steps.append({
            'step': 'Subtotal',
            'description': 'Sum of all direct costs',
            'calculation': f'₹{material_cost:,.0f} + ₹{machining_cost:,.0f} + ₹{tooling_cost:,.0f} + ₹{finishing_cost:,.0f} + ₹{testing_cost:,.0f} = ₹{subtotal:,.0f}',
            'cost': subtotal
        })
        
        # Step 7: Calculate overhead and scrap allowance
        overhead = subtotal * (OVERHEAD_PERCENTAGE / 100)
        scrap_allowance = subtotal * (SCRAP_ALLOWANCE / 100)
        calculation_steps.append({
            'step': 'Overhead',
            'description': f'Factory overhead ({OVERHEAD_PERCENTAGE}%)',
            'calculation': f'₹{subtotal:,.0f} × {OVERHEAD_PERCENTAGE}% = ₹{overhead:,.0f}',
            'cost': overhead
        })
        calculation_steps.append({
            'step': 'Scrap Allowance',
            'description': f'Material waste allowance ({SCRAP_ALLOWANCE}%)',
            'calculation': f'₹{subtotal:,.0f} × {SCRAP_ALLOWANCE}% = ₹{scrap_allowance:,.0f}',
            'cost': scrap_allowance
        })
        
        # Step 8: Total cost per piece
        total_per_piece = subtotal + overhead + scrap_allowance
        calculation_steps.append({
            'step': 'Total Cost',
            'description': 'Final cost per piece',
            'calculation': f'₹{subtotal:,.0f} + ₹{overhead:,.0f} + ₹{scrap_allowance:,.0f} = ₹{total_per_piece:,.0f}',
            'cost': total_per_piece
        })
        
        # Calculate lead time
        lead_time = self._calculate_lead_time(cad_properties, quantity)
        
        return {
            'material_cost': round(material_cost, 2),
            'machining_cost': round(machining_cost, 2),
            'tooling_cost': round(tooling_cost, 2),
            'finishing_cost': round(finishing_cost, 2),
            'testing_cost': round(testing_cost, 2),
            'overhead': round(overhead, 2),
            'scrap_allowance': round(scrap_allowance, 2),
            'total_per_piece': round(total_per_piece, 2),
            'lead_time_weeks': lead_time,
            'breakdown': {
                'Material': material_cost,
                'Machining': machining_cost,
                'Tooling': tooling_cost,
                'Finishing': finishing_cost,
                'Testing': testing_cost,
                'Overhead': overhead,
                'Scrap Allowance': scrap_allowance
            },
            'calculation_steps': calculation_steps
        }
    
    def _calculate_material_cost(self, properties: Dict[str, Any], material: str) -> float:
        """Calculate material cost per piece"""
        if material not in self.materials:
            material = "AlSi10Mg"  # Default material
        
        material_data = self.materials[material]
        volume_mm3 = properties['volume_mm3']
        density = material_data['density']  # g/cc
        yield_percentage = material_data['yield_percentage']
        cost_per_kg = material_data['cost_per_kg']
        
        # Calculate net weight using correct density
        volume_cc = volume_mm3 / 1000  # Convert mm³ to cm³
        net_weight_kg = (volume_cc * density) / 1000  # Convert g to kg
        
        # Calculate gross weight considering yield
        gross_weight = net_weight_kg / (yield_percentage / 100)
        
        # Calculate material cost
        material_cost = gross_weight * cost_per_kg
        
        return material_cost
    
    def _calculate_material_cost_with_steps(self, properties: Dict[str, Any], material: str) -> Dict[str, Any]:
        """Calculate material cost per piece with detailed steps"""
        if material not in self.materials:
            material = "AlSi10Mg"  # Default material
        
        material_data = self.materials[material]
        volume_mm3 = properties['volume_mm3']
        density = material_data['density']  # g/cc
        yield_percentage = material_data['yield_percentage']
        cost_per_kg = material_data['cost_per_kg']
        
        steps = []
        
        # Step 1: Volume conversion
        volume_cc = volume_mm3 / 1000  # Convert mm³ to cm³
        steps.append({
            'step': 'Volume Conversion',
            'description': 'Convert volume from mm³ to cm³',
            'calculation': f'{volume_mm3:,.0f} mm³ ÷ 1000 = {volume_cc:,.2f} cm³',
            'cost': 0
        })
        
        # Step 2: Net weight calculation
        net_weight_kg = (volume_cc * density) / 1000  # Convert g to kg
        steps.append({
            'step': 'Net Weight',
            'description': f'Calculate net weight using {material} density',
            'calculation': f'{volume_cc:,.2f} cm³ × {density} g/cc ÷ 1000 = {net_weight_kg:.3f} kg',
            'cost': 0
        })
        
        # Step 3: Gross weight calculation
        gross_weight = net_weight_kg / (yield_percentage / 100)
        steps.append({
            'step': 'Gross Weight',
            'description': f'Account for casting yield ({yield_percentage}%)',
            'calculation': f'{net_weight_kg:.3f} kg ÷ {yield_percentage}% = {gross_weight:.3f} kg',
            'cost': 0
        })
        
        # Step 4: Material cost
        material_cost = gross_weight * cost_per_kg
        steps.append({
            'step': 'Material Cost',
            'description': f'Calculate cost using {material} rate',
            'calculation': f'{gross_weight:.3f} kg × ₹{cost_per_kg}/kg = ₹{material_cost:,.0f}',
            'cost': material_cost
        })
        
        return {'cost': material_cost, 'steps': steps}
    
    def _calculate_machining_cost(self, properties: Dict[str, Any]) -> float:
        """Calculate machining cost per piece"""
        # Get machining parameters
        volume_mm3 = properties['volume_mm3']
        surface_area_mm2 = properties['surface_area_mm2']
        features = properties['features']
        
        # Estimate machining time based on features
        machining_time = 0
        
        # Hole drilling time
        holes = features.get('holes', 0)
        machining_time += holes * 0.25  # 0.25 min per hole
        
        # Surface machining time (based on surface area)
        surface_machining_time = (surface_area_mm2 / 10000) * 0.02  # 0.02 min per cm²
        machining_time += surface_machining_time
        
        # Setup time
        setup_time = 15  # 15 minutes setup
        machining_time += setup_time
        
        # Use VMC rate
        machine_rate = self.machining_rates['VMC']
        machining_cost = (machining_time / 60) * machine_rate  # Convert to hours
        
        return machining_cost
    
    def _calculate_machining_cost_with_steps(self, properties: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate machining cost per piece with detailed steps"""
        # Get machining parameters
        volume_mm3 = properties['volume_mm3']
        surface_area_mm2 = properties['surface_area_mm2']
        features = properties['features']
        
        steps = []
        
        # Estimate machining time based on features
        machining_time = 0
        
        # Hole drilling time
        holes = features.get('holes', 0)
        hole_time = holes * 0.25  # 0.25 min per hole
        machining_time += hole_time
        if holes > 0:
            steps.append({
                'step': 'Hole Drilling',
                'description': f'Drill {holes} holes',
                'calculation': f'{holes} holes × 0.25 min/hole = {hole_time:.1f} min',
                'cost': 0
            })
        
        # Surface machining time (based on surface area)
        surface_machining_time = (surface_area_mm2 / 10000) * 0.02  # 0.02 min per cm²
        machining_time += surface_machining_time
        steps.append({
            'step': 'Surface Machining',
            'description': 'Machine all surfaces',
            'calculation': f'{surface_area_mm2:,.0f} mm² ÷ 10,000 × 0.02 min/cm² = {surface_machining_time:.1f} min',
            'cost': 0
        })
        
        # Setup time
        setup_time = 15  # 15 minutes setup
        machining_time += setup_time
        steps.append({
            'step': 'Setup Time',
            'description': 'Machine setup and fixturing',
            'calculation': f'15 min (standard setup)',
            'cost': 0
        })
        
        # Total machining time
        steps.append({
            'step': 'Total Machining Time',
            'description': 'Sum of all machining operations',
            'calculation': f'{hole_time:.1f} + {surface_machining_time:.1f} + {setup_time} = {machining_time:.1f} min',
            'cost': 0
        })
        
        # Use VMC rate
        machine_rate = self.machining_rates['VMC']
        machining_cost = (machining_time / 60) * machine_rate  # Convert to hours
        steps.append({
            'step': 'Machining Cost',
            'description': 'Calculate cost using VMC rate',
            'calculation': f'{machining_time:.1f} min ÷ 60 × ₹{machine_rate}/hr = ₹{machining_cost:,.0f}',
            'cost': machining_cost
        })
        
        return {'cost': machining_cost, 'steps': steps}
    
    def _calculate_tooling_cost(self, properties: Dict[str, Any], quantity: int) -> float:
        """Calculate tooling cost per piece (amortized)"""
        # Determine part size category
        bounding_box = properties['bounding_box']
        max_dimension = max(bounding_box['length'], bounding_box['width'], bounding_box['height'])
        
        if max_dimension < 100:
            size_category = 'small'
        elif max_dimension < 300:
            size_category = 'medium'
        else:
            size_category = 'large'
        
        # Calculate tooling cost based on part complexity and size
        complexity = properties['complexity_score']
        volume_mm3 = properties['volume_mm3']
        
        # More realistic tooling cost formula
        # Base tooling cost: ₹50,000 for small parts, scaling with volume
        if max_dimension < 50:  # Very small parts (like screws)
            base_tooling_cost = 50000  # ₹50K for simple tooling
        elif max_dimension < 100:  # Small parts
            base_tooling_cost = 100000  # ₹1L
        elif max_dimension < 300:  # Medium parts
            base_tooling_cost = 500000  # ₹5L
        else:  # Large parts
            base_tooling_cost = 2000000  # ₹20L
        
        # Apply complexity factor (1.0 to 2.0)
        complexity_factor = 1 + (complexity * 0.5)  # Max 1.5x for complexity
        size_factor = self.tooling_factors[size_category]
        
        total_tooling_cost = base_tooling_cost * complexity_factor * size_factor
        
        # Amortize over quantity
        tooling_cost_per_piece = total_tooling_cost / quantity
        
        return tooling_cost_per_piece
    
    def _calculate_tooling_cost_with_steps(self, properties: Dict[str, Any], quantity: int) -> Dict[str, Any]:
        """Calculate tooling cost per piece with detailed steps"""
        # Determine part size category
        bounding_box = properties['bounding_box']
        max_dimension = max(bounding_box['length'], bounding_box['width'], bounding_box['height'])
        
        steps = []
        
        # Size category determination
        if max_dimension < 100:
            size_category = 'small'
        elif max_dimension < 300:
            size_category = 'medium'
        else:
            size_category = 'large'
        
        steps.append({
            'step': 'Size Category',
            'description': f'Determine part size category',
            'calculation': f'Max dimension: {max_dimension:.1f}mm → {size_category}',
            'cost': 0
        })
        
        # Calculate tooling cost based on part complexity and size
        complexity = properties['complexity_score']
        volume_mm3 = properties['volume_mm3']
        
        # More realistic tooling cost formula
        if max_dimension < 50:  # Very small parts (like screws)
            base_tooling_cost = 50000  # ₹50K for simple tooling
        elif max_dimension < 100:  # Small parts
            base_tooling_cost = 100000  # ₹1L
        elif max_dimension < 300:  # Medium parts
            base_tooling_cost = 500000  # ₹5L
        else:  # Large parts
            base_tooling_cost = 2000000  # ₹20L
        
        steps.append({
            'step': 'Base Tooling Cost',
            'description': f'Base tooling cost for {size_category} parts',
            'calculation': f'₹{base_tooling_cost:,} (based on size)',
            'cost': 0
        })
        
        # Apply complexity factor (1.0 to 2.0)
        complexity_factor = 1 + (complexity * 0.5)  # Max 1.5x for complexity
        size_factor = self.tooling_factors[size_category]
        
        steps.append({
            'step': 'Complexity Factor',
            'description': f'Apply complexity factor (score: {complexity:.2f})',
            'calculation': f'1 + ({complexity:.2f} × 0.5) = {complexity_factor:.2f}',
            'cost': 0
        })
        
        steps.append({
            'step': 'Size Factor',
            'description': f'Apply size factor for {size_category} parts',
            'calculation': f'{size_factor} (from rate card)',
            'cost': 0
        })
        
        total_tooling_cost = base_tooling_cost * complexity_factor * size_factor
        steps.append({
            'step': 'Total Tooling Cost',
            'description': 'Calculate total tooling investment',
            'calculation': f'₹{base_tooling_cost:,} × {complexity_factor:.2f} × {size_factor} = ₹{total_tooling_cost:,.0f}',
            'cost': 0
        })
        
        # Amortize over quantity
        tooling_cost_per_piece = total_tooling_cost / quantity
        steps.append({
            'step': 'Amortized Tooling Cost',
            'description': f'Distribute tooling cost over {quantity:,} pieces',
            'calculation': f'₹{total_tooling_cost:,.0f} ÷ {quantity:,} pcs = ₹{tooling_cost_per_piece:,.0f}/pc',
            'cost': tooling_cost_per_piece
        })
        
        return {'cost': tooling_cost_per_piece, 'steps': steps}
    
    def _calculate_lead_time(self, properties: Dict[str, Any], quantity: int) -> int:
        """Calculate lead time in weeks"""
        # Base lead time
        base_weeks = 4
        
        # Add complexity factor
        complexity = properties['complexity_score']
        complexity_weeks = int(complexity * 4)
        
        # Add quantity factor (larger quantities may need more time)
        if quantity > 10000:
            quantity_weeks = 2
        elif quantity > 5000:
            quantity_weeks = 1
        else:
            quantity_weeks = 0
        
        total_weeks = base_weeks + complexity_weeks + quantity_weeks
        
        return min(total_weeks, 16)  # Cap at 16 weeks

