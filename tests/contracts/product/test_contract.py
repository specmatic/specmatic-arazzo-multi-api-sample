import pytest

from services.product.schema import schema
from tests.contracts.conftest import ProviderEnvironment


@pytest.mark.parametrize(
    "provider_environment",
    [ProviderEnvironment("product", "product", 4000)],
    indirect=True,
)
def test_product_contract(provider_environment):
    provider_environment.run_contract()


def test_products_requires_location_code():
    result = schema.execute_sync("query { products { productId } }")
    assert result.data is None
    assert result.errors
    assert "locationCode" in result.errors[0].message
