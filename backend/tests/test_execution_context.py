import unittest
import uuid
from app.runtime.execution_context import ExecutionContext
from app.runtime.step_result import StepResult


class TestExecutionContext(unittest.TestCase):
    def make_context(self):
        return ExecutionContext(
            execution_id=uuid.uuid4(),
            workflow_id=uuid.uuid4(),
            organization_id=uuid.uuid4(),
            ai_employee_id=uuid.uuid4(),
            input_data={"initial": "value"},
            variables={"initial": "value"},
        )

    def test_set_current_step(self):
        ctx = self.make_context()
        ctx.set_current_step("step_1")
        self.assertEqual(ctx.current_step_id, "step_1")

    def test_add_step_result(self):
        ctx = self.make_context()
        result = StepResult(step_id="step_1", success=True, output={"response": "ok"})
        ctx.add_step_result(result)
        self.assertEqual(len(ctx.get_step_results()), 1)
        self.assertEqual(ctx.get_step_results()[0].step_id, "step_1")

    def test_update_variables(self):
        ctx = self.make_context()
        ctx.update_variables({"next": "value"})
        self.assertEqual(ctx.variables["next"], "value")

    def test_step_results_is_typed_list(self):
        ctx = self.make_context()
        self.assertIsInstance(ctx.step_results, list)


if __name__ == "__main__":
    unittest.main()