# Hackaton Contract Documentation

## Features
- **Traceability**: Ensures that all products in the supply chain are traceable.
- **Environmental and Cost Tracking**: Tracks environmental impact and costs associated with each product stage.

## Contract Structure
The Hackaton contract comprises several entry points, each corresponding to a different stage in a product's lifecycle:
- `build`: Initializes a new product in the blockchain.
- `production`: Records production details, including emissions and costs.
- `transport`: Logs transportation details, adjusting the product's environmental and cost metrics.
- `transformation`: Notes transformation processes, again adjusting metrics.
- `distribution`: Finalizes the product's journey by documenting distribution impacts.
- `deleteProduct`: Removes a product from tracking.
- `setPause`: Toggles the traceability feature of the contract.

## How to Use
1. **Initialization**: Create an instance of the Hackaton contract.
2. **Product Lifecycle Management**:
   - Start by adding a product using the `build` entry point.
   - Proceed through the lifecycle using the `production`, `transport`, `transformation`, and `distribution` entry points as appropriate.
   - Each entry point adjusts the product's environmental impact and cost according to the parameters provided.
3. **Product Deletion**: Remove a product from tracking with `deleteProduct`.
4. **Pause Tracking**: Temporarily disable traceability if necessary with `setPause`.

## Example Usage
```python
# Initialize contract
c1 = Hackaton()

# Add a new product
c1.build(product="tomatoes")

# Record production details
c1.production(product="tomatoes", emission_producer=400000, volume_producer=30000, ...)

# Continue through transport, transformation, and distribution stages
...

# Remove a product
c1.deleteProduct(product="apples")

