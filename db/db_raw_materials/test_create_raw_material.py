from datetime import datetime
import uuid
from routers.schemas import RawMaterialBase
from db_raw_materials.db_raw_material import create_raw_material

# Test input
test_request = RawMaterialBase(
    raw_material_id=uuid.uuid4(),
    raw_material_name=uuid.uuid4(),
    raw_material_code="RM001",
    quantity=100,
    reorder_level=10,
    unit_cost=50,
    category="Raw Material",
    created_at=datetime.now(),
    created_by=uuid.uuid4()
)

mock_user = {
    "access_token": "mock_access_token",
    "refresh_token": "mock_refresh_token",
    "id": uuid.uuid4()
}

# Simulate the function call
try:
    result = create_raw_material(test_request, mock_user)
    print("Raw material created successfully:", result)
except Exception as e:
    print("Error occurred:", str(e))
