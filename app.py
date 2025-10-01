"""
Inticore Estimation Automation - Streamlit App
Main application for CAD file processing and cost estimation
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os
import tempfile
import json

# Import our modules
from cad_processor import CADProcessor
from estimation_engine import EstimationEngine
from database import EstimationDatabase
from config import MATERIALS, FINISHING_COSTS, TESTING_COSTS, MACHINING_RATES, TOOLING_FACTORS, OVERHEAD_PERCENTAGE, SCRAP_ALLOWANCE

# Page configuration
st.set_page_config(
    page_title="Inticore Estimation Automation",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .cost-card {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
        margin-bottom: 1rem;
    }
    .stExpander {
        background-color: #f8f9fa;
        border: 1px solid #e0e0e0;
        border-radius: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'estimates' not in st.session_state:
    st.session_state.estimates = []
if 'current_estimate' not in st.session_state:
    st.session_state.current_estimate = None
if 'rate_cards' not in st.session_state:
    # Initialize rate cards from config
    st.session_state.rate_cards = {
        'materials': dict(MATERIALS),
        'machining_rates': dict(MACHINING_RATES),
        'finishing_costs': dict(FINISHING_COSTS),
        'testing_costs': dict(TESTING_COSTS),
        'tooling_factors': dict(TOOLING_FACTORS),
        'overhead_percentage': OVERHEAD_PERCENTAGE,
        'scrap_allowance': SCRAP_ALLOWANCE
    }

# Initialize components
cad_processor = CADProcessor()
database = EstimationDatabase()

def get_estimation_engine():
    """Get estimation engine with current rate cards"""
    engine = EstimationEngine()
    engine.materials = st.session_state.rate_cards['materials']
    engine.machining_rates = st.session_state.rate_cards['machining_rates']
    engine.finishing_costs = st.session_state.rate_cards['finishing_costs']
    engine.testing_costs = st.session_state.rate_cards['testing_costs']
    engine.tooling_factors = st.session_state.rate_cards['tooling_factors']
    return engine

def main():
    """Main application function"""
    
    # Header
    st.markdown('<h1 class="main-header">🏭 Inticore Estimation Automation</h1>', unsafe_allow_html=True)
    
    # Tab-based navigation
    tab1, tab2, tab3 = st.tabs(["📁 Estimate", "💰 Rate Cards", "📚 History"])
    
    with tab1:
        estimate_page()
    with tab2:
        rate_cards_page()
    with tab3:
        estimate_history_page()

def estimate_page():
    """Main estimation page"""
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📤 Upload CAD File")
        
        # File uploader
        uploaded_file = st.file_uploader(
            "Upload CAD File",
            type=['stl', 'obj', 'ply', 'off', 'glb', 'gltf'],
            help="Supported formats: STL, OBJ, PLY, OFF, GLB, GLTF",
            key="file_uploader"
        )
        
        if uploaded_file is not None:
            # Save uploaded file temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                tmp_file_path = tmp_file.name
            
            # Validate file
            if cad_processor.validate_file(tmp_file_path):
                st.success(f"✅ File '{uploaded_file.name}' uploaded successfully!")
                
                # Store file info in session state
                st.session_state.uploaded_file = {
                    'name': uploaded_file.name,
                    'path': tmp_file_path,
                    'size': uploaded_file.size
                }
            else:
                st.error("❌ Invalid file format.")
                return
    
    with col2:
        st.subheader("⚙️ Configuration")
        
        # Material selection
        material = st.selectbox(
            "Material",
            list(st.session_state.rate_cards['materials'].keys()),
            index=list(st.session_state.rate_cards['materials'].keys()).index("Steel") if "Steel" in st.session_state.rate_cards['materials'] else 0,
            help="Select the material for the part"
        )
        
        # Quantity input
        quantity = st.number_input(
            "Annual Quantity",
            min_value=1,
            max_value=1000000,
            value=10000,
            help="Annual production quantity"
        )
        
        # Finish selection
        finish = st.selectbox(
            "Surface Finish",
            list(st.session_state.rate_cards['finishing_costs'].keys()),
            index=0,
            help="Select surface finish requirement"
        )
        
        # Testing selection
        testing = st.selectbox(
            "Testing Requirements",
            list(st.session_state.rate_cards['testing_costs'].keys()),
            index=0,
            help="Select testing requirements"
        )
    
    # Process button
    if uploaded_file is not None:
        if st.button("🚀 Calculate Estimate", type="primary", use_container_width=True):
            config = {
                'material': material,
                'quantity': quantity,
                'finish': finish,
                'testing': testing
            }
            process_and_calculate_estimate(config)
    
    # Display results if available
    if 'current_estimate' in st.session_state and st.session_state.current_estimate is not None:
        st.divider()
        display_results()

def process_and_calculate_estimate(config):
    """Process CAD file and calculate estimate"""
    uploaded_file = st.session_state.uploaded_file
    
    with st.spinner("Processing..."):
        try:
            # Process CAD file
            cad_properties = cad_processor.process_file(uploaded_file['path'])
            
            # Calculate costs
            estimation_engine = get_estimation_engine()
            cost_breakdown = estimation_engine.calculate_estimate(
                cad_properties, 
                config['material'], 
                config['quantity'], 
                config['finish'], 
                config['testing']
            )
            
            # Store results
            st.session_state.current_estimate = {
                'filename': uploaded_file['name'],
                'cad_properties': cad_properties,
                'config': config,
                'cost_breakdown': cost_breakdown,
                'timestamp': datetime.now()
            }
            
            # Save to database
            estimate_id = database.save_estimate(
                uploaded_file['name'],
                config['material'],
                config['quantity'],
                config['finish'],
                config['testing'],
                cad_properties,
                cost_breakdown
            )
            
            st.session_state.current_estimate['id'] = estimate_id
            st.success("✅ Estimation Complete!")
            st.rerun()
                
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

def display_results():
    """Display estimation results"""
    estimate = st.session_state.current_estimate
    cost_breakdown = estimate['cost_breakdown']
    config = estimate['config']
    cad_props = estimate['cad_properties']
    
    st.subheader("📊 Cost Estimation Results")
    
    # Summary metrics in one row
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("Total Cost/pc", f"₹{cost_breakdown['total_per_piece']:,.0f}")
    with col2:
        st.metric("Material", f"₹{cost_breakdown['material_cost']:,.0f}")
    with col3:
        st.metric("Machining", f"₹{cost_breakdown['machining_cost']:,.0f}")
    with col4:
        st.metric("Tooling", f"₹{cost_breakdown['tooling_cost']:,.0f}")
    with col5:
        st.metric("Lead Time", f"{cost_breakdown['lead_time_weeks']} weeks")
    
    # Two column layout
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # Part properties
        st.markdown("**Part Properties**")
        props_df = pd.DataFrame([
            {"Property": "Volume", "Value": f"{cad_props['volume_mm3']:,.1f} mm³"},
            {"Property": "Surface Area", "Value": f"{cad_props['surface_area_mm2']:,.1f} mm²"},
            {"Property": "Weight", "Value": f"{cad_props['weight_kg']:.3f} kg"},
            {"Property": "Size (L×W×H)", "Value": f"{cad_props['bounding_box']['length']:.1f} × {cad_props['bounding_box']['width']:.1f} × {cad_props['bounding_box']['height']:.1f} mm"},
        ])
        st.dataframe(props_df, hide_index=True, use_container_width=True)
        
        # Configuration
        st.markdown("**Configuration**")
        config_df = pd.DataFrame([
            {"Parameter": "Material", "Value": config['material']},
            {"Parameter": "Quantity", "Value": f"{config['quantity']:,}"},
            {"Parameter": "Finish", "Value": config['finish']},
            {"Parameter": "Testing", "Value": config['testing']},
        ])
        st.dataframe(config_df, hide_index=True, use_container_width=True)
    
    with col2:
        # Cost breakdown chart
        fig = px.pie(
            values=list(cost_breakdown['breakdown'].values()),
            names=list(cost_breakdown['breakdown'].keys()),
            title="Cost Distribution",
            hole=0.3
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Calculation steps in compact expander
    with st.expander("🔍 View Detailed Calculation Steps", expanded=False):
        if 'calculation_steps' in cost_breakdown:
            for i, step in enumerate(cost_breakdown['calculation_steps'], 1):
                if step['cost'] > 0:  # Only show steps with cost
                    st.markdown(f"**{step['step']}:** {step['calculation']}")
                    st.caption(step['description'])
                    if i < len(cost_breakdown['calculation_steps']):
                        st.divider()
    
    # Action buttons
    col1, col2 = st.columns(2)
    with col1:
        estimate_json = json.dumps(estimate, indent=2, default=str)
        st.download_button(
            label="📄 Download Report (JSON)",
            data=estimate_json,
            file_name=f"estimate_{estimate['filename']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json",
            use_container_width=True
        )
    with col2:
        if st.button("🔄 New Estimate", use_container_width=True):
            st.session_state.current_estimate = None
            if 'uploaded_file' in st.session_state:
                del st.session_state.uploaded_file
            st.rerun()

def rate_cards_page():
    """Rate cards management page"""
    st.subheader("💰 Rate Cards Configuration")
    st.info("💡 Edit the rates below. Changes apply immediately to new estimates.")
    
    # Material rates
    st.markdown("### Material Rates")
    materials = st.session_state.rate_cards['materials']
    
    for material_name, material_data in materials.items():
        with st.expander(f"🔩 {material_name}", expanded=False):
            col1, col2, col3 = st.columns(3)
            with col1:
                materials[material_name]['density'] = st.number_input(
                    "Density (g/cc)",
                    value=float(material_data['density']),
                    min_value=0.1,
                    max_value=20.0,
                    step=0.01,
                    key=f"density_{material_name}"
                )
            with col2:
                materials[material_name]['cost_per_kg'] = st.number_input(
                    "Cost per kg (₹)",
                    value=int(material_data['cost_per_kg']),
                    min_value=1,
                    max_value=10000,
                    step=10,
                    key=f"cost_{material_name}"
                )
            with col3:
                materials[material_name]['yield_percentage'] = st.number_input(
                    "Yield %",
                    value=int(material_data['yield_percentage']),
                    min_value=1,
                    max_value=100,
                    step=1,
                    key=f"yield_{material_name}"
                )
    
    # Machining rates
    st.markdown("### Machining Rates (₹/hour)")
    machining_rates = st.session_state.rate_cards['machining_rates']
    col1, col2, col3, col4 = st.columns(4)
    for i, (machine, rate) in enumerate(machining_rates.items()):
        with [col1, col2, col3, col4][i % 4]:
            machining_rates[machine] = st.number_input(
                machine,
                value=int(rate),
                min_value=100,
                max_value=5000,
                step=50,
                key=f"machine_{machine}"
            )
    
    # Finishing costs
    st.markdown("### Finishing Costs (₹/piece)")
    finishing_costs = st.session_state.rate_cards['finishing_costs']
    col1, col2 = st.columns(2)
    for i, (finish, cost) in enumerate(finishing_costs.items()):
        with [col1, col2][i % 2]:
            finishing_costs[finish] = st.number_input(
                finish,
                value=int(cost),
                min_value=0,
                max_value=1000,
                step=10,
                key=f"finish_{finish}"
            )
    
    # Testing costs
    st.markdown("### Testing Costs (₹/piece)")
    testing_costs = st.session_state.rate_cards['testing_costs']
    col1, col2 = st.columns(2)
    for i, (test, cost) in enumerate(testing_costs.items()):
        with [col1, col2][i % 2]:
            testing_costs[test] = st.number_input(
                test,
                value=int(cost),
                min_value=0,
                max_value=1000,
                step=10,
                key=f"test_{test}"
            )
    
    # Other parameters
    st.markdown("### Other Parameters")
    col1, col2 = st.columns(2)
    with col1:
        st.session_state.rate_cards['overhead_percentage'] = st.number_input(
            "Overhead %",
            value=int(st.session_state.rate_cards['overhead_percentage']),
            min_value=0,
            max_value=50,
            step=1,
            key="overhead"
        )
    with col2:
        st.session_state.rate_cards['scrap_allowance'] = st.number_input(
            "Scrap Allowance %",
            value=int(st.session_state.rate_cards['scrap_allowance']),
            min_value=0,
            max_value=20,
            step=1,
            key="scrap"
        )
    
    # Reset button
    if st.button("🔄 Reset to Default Values"):
        st.session_state.rate_cards = {
            'materials': dict(MATERIALS),
            'machining_rates': dict(MACHINING_RATES),
            'finishing_costs': dict(FINISHING_COSTS),
            'testing_costs': dict(TESTING_COSTS),
            'tooling_factors': dict(TOOLING_FACTORS),
            'overhead_percentage': OVERHEAD_PERCENTAGE,
            'scrap_allowance': SCRAP_ALLOWANCE
        }
        st.success("✅ Reset to default values!")
        st.rerun()

def estimate_history_page():
    """Estimate history page"""
    st.subheader("📚 Estimate History")
    
    # Get estimates from database
    estimates = database.get_estimates(limit=50)
    
    if not estimates:
        st.info("No estimates found. Create some estimates to see history here.")
        return
    
    # Display estimates in a table
    history_data = []
    for estimate in estimates:
        history_data.append({
            'ID': estimate['id'],
            'Filename': estimate['filename'],
            'Material': estimate['material'],
            'Quantity': f"{estimate['quantity']:,}",
            'Total Cost': f"₹{estimate['total_cost']:,.0f}",
            'Lead Time': f"{estimate['lead_time']} weeks",
            'Created': estimate['created_at'][:19]
        })
    
    df_history = pd.DataFrame(history_data)
    st.dataframe(df_history, use_container_width=True, hide_index=True)
    
    if st.button("🔄 Refresh"):
        st.rerun()

if __name__ == "__main__":
    main()
