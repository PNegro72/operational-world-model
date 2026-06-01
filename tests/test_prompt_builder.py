from pathlib import Path
import inspect
import tempfile
import unittest

from operational_world_model.prompt_builder import DynamicPromptBuilder
from operational_world_model.schemas import ControlDecision, OperationalState, SkillDecision


class PromptBuilderTests(unittest.TestCase):
    def test_loads_markdown_file_and_interpolates_variables(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            module_path = Path(temp_dir) / "module.md"
            module_path.write_text(
                "Question={{question}}\nMissing={{optional_value}}",
                encoding="utf-8",
            )
            builder = DynamicPromptBuilder(
                prompt_registry={
                    "custom": {
                        "name": "custom",
                        "description": "custom module",
                        "module_type": "test",
                        "applies_to": ["test"],
                        "path": "module.md",
                    }
                },
                base_path=Path(temp_dir),
            )

            prompt = builder.build(
                OperationalState(
                    state_id="state-1",
                    domain="test",
                    facts={"question": "Which date?"},
                ),
                ControlDecision(action="continue", priority=1, rationale="test"),
                SkillDecision(skill_name="sql_skill", confidence=1.0, rationale="test"),
                ["custom"],
            )

            self.assertIn("Question=Which date?", prompt)
            self.assertIn("Missing=", prompt)

    def test_unknown_module_raises_clear_error(self) -> None:
        builder = DynamicPromptBuilder(prompt_registry={})

        with self.assertRaisesRegex(ValueError, "Unknown prompt module 'missing_module'"):
            builder.build(
                OperationalState(state_id="state-1", domain="test"),
                ControlDecision(action="continue", priority=1, rationale="test"),
                SkillDecision(skill_name="noop", confidence=1.0, rationale="test"),
                ["missing_module"],
            )

    def test_missing_file_raises_clear_error(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            builder = DynamicPromptBuilder(
                prompt_registry={
                    "missing_file": {
                        "name": "missing_file",
                        "description": "missing file",
                        "module_type": "test",
                        "applies_to": ["test"],
                        "path": "does_not_exist.md",
                    }
                },
                base_path=Path(temp_dir),
            )

            with self.assertRaisesRegex(FileNotFoundError, "file does not exist"):
                builder.build(
                    OperationalState(state_id="state-1", domain="test"),
                    ControlDecision(action="continue", priority=1, rationale="test"),
                    SkillDecision(skill_name="noop", confidence=1.0, rationale="test"),
                    ["missing_file"],
                )

    def test_builder_does_not_hardcode_pf_module_content(self) -> None:
        source = inspect.getsource(DynamicPromptBuilder)

        self.assertNotIn("Core vs Site is unidirectional", source)
        self.assertNotIn("SQL Skill only generates BigQuery SQL", source)


if __name__ == "__main__":
    unittest.main()
