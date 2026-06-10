import torch

class CategoryChecker:
    @staticmethod
    def assert_chart_transition_inverse(chart0, chart1, num_samples=10000):
        coords = torch.rand(num_samples) * 2*torch.pi
        coords_0 = chart0.phi(coords)
        coords_1 = chart1.phi(coords)
        back = chart0.phi(chart1.inv_phi(coords_1))
        error = torch.abs(back - coords_0).max().item()
        assert error < 1e-10, f"Chart transition error: {error}"
        print(f"[Category] OK (max error {error:.2e})")

    @staticmethod
    def assert_fiber_type(fiber_element, expected_bundle_name: str):
        assert fiber_element.bundle.name == expected_bundle_name

    @staticmethod
    def assert_point_on_manifold(point_coords: torch.Tensor, manifold):
        for chart in manifold.atlas.values():
            if chart.valid_region(point_coords).any():
                return True
        raise ValueError("Point not in any chart's valid region")