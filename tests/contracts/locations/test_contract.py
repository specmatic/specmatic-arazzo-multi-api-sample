import pytest

from tests.contracts.conftest import ProviderEnvironment


@pytest.mark.parametrize(
    "provider_environment",
    [
        pytest.param(
            ProviderEnvironment(
                "location_examples",
                "location",
                50051,
                protocol="grpc",
                contract_directory="locations",
                specmatic_system_properties={
                    "LOCATION_EXAMPLES_PATH": "examples",
                    "LOCATION_SCHEMA_RESILIENCY": "none",
                },
            ),
            id="examples",
        ),
        pytest.param(
            ProviderEnvironment(
                "location_resiliency",
                "location",
                50051,
                protocol="grpc",
                contract_directory="locations",
                specmatic_system_properties={
                    "LOCATION_EXAMPLES_PATH": "examples/location_get_not_found_unknown.json",
                    "LOCATION_SCHEMA_RESILIENCY": "all",
                },
            ),
            id="schema-resiliency",
        ),
    ],
    indirect=True,
)
def test_location_contract(provider_environment):
    provider_environment.run_contract()
