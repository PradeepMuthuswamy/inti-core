"""
Configuration file for Inticore Estimation Automation
Contains rate cards, material data, and estimation parameters
"""

# Material properties and costs (₹/kg)
MATERIALS = {
    "AlSi7Mg": {
        "density": 2.68,  # g/cc
        "cost_per_kg": 290,
        "yield_percentage": 70
    },
    "AlSi10Mg": {
        "density": 2.68,
        "cost_per_kg": 290,
        "yield_percentage": 70
    },
    "AlSi12": {
        "density": 2.65,
        "cost_per_kg": 280,
        "yield_percentage": 72
    },
    "Steel": {
        "density": 7.85,
        "cost_per_kg": 120,
        "yield_percentage": 85
    }
}

# Machining rates (₹/hour)
MACHINING_RATES = {
    "VMC": 800,  # Vertical Machining Center
    "HMC": 900,  # Horizontal Machining Center
    "CNC_Turning": 700,
    "Drilling": 500
}

# Finishing costs (₹/piece)
FINISHING_COSTS = {
    "Anodized": 60,
    "Coated": 40,
    "Polished": 30,
    "As_Cast": 0
}

# Testing costs (₹/piece)
TESTING_COSTS = {
    "Leak_Test": 40,
    "X_Ray": 100,
    "Dimensional_Check": 20,
    "None": 0
}

# Tooling cost factors
TOOLING_FACTORS = {
    "small": 0.15,      # < 100mm
    "medium": 0.20,     # 100-300mm
    "large": 0.25       # > 300mm
}

# Overhead percentage
OVERHEAD_PERCENTAGE = 15

# Scrap allowance percentage
SCRAP_ALLOWANCE = 5

