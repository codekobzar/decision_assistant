import pytest

from progress_tracker import ProgressTracker


@pytest.fixture
def example_steps():
    return [
        "decision",
        "decision_options",
        "evaluation_factors",
        "evaluation_factor_importance",
        "decision_option_evaluation",
    ]

@pytest.fixture
def example_progress_tracker(example_steps):
    return ProgressTracker(steps=example_steps)

class TestProgressTracker:

    def test_init(self, example_steps):
        progress_tracker = ProgressTracker(example_steps)
        assert progress_tracker.steps == example_steps
        assert len(progress_tracker.progress) == len(example_steps)

    def test_step_set_active(self, example_progress_tracker):
        progress_tracker = example_progress_tracker
        progress_tracker.step_set_active("decision_options")
        assert progress_tracker.progress[1] is True
        progress_tracker.step_set_active("decision_options", False)
        assert progress_tracker.progress[1] is False

    def test_steps_set_active(self, example_progress_tracker):
        progress_tracker = example_progress_tracker
        steps = [s for s in progress_tracker.steps if s != 'decision_options']
        progress_tracker.steps_set_active(steps)
        assert progress_tracker.progress[1] is False
        assert progress_tracker.progress[2:] == [True] * 3
        progress_tracker.step_set_active("decision_options")
        progress_tracker.steps_set_active(steps, False)
        assert progress_tracker.progress[1] is True
        assert progress_tracker.progress[2:] == [False] * 3

    def test_prev_steps_set_active(self, example_progress_tracker):
        progress_tracker = example_progress_tracker
        step = 'evaluation_factors'
        progress_tracker.prev_steps_set_active(step)
        assert progress_tracker.progress[2] is False
        assert progress_tracker.progress[:2] == [True] * 2
        assert progress_tracker.progress[3:] == [False] * 2
        progress_tracker.prev_steps_set_active(step, False)
        assert progress_tracker.progress[:2] == [False] * 2
        progress_tracker.next_steps_set_active(step)
        assert progress_tracker.progress[2] is False
        assert progress_tracker.progress[:2] == [False] * 2
        assert progress_tracker.progress[3:] == [True] * 2
        progress_tracker.next_steps_set_active(step, False)
        assert progress_tracker.progress[3:] == [False] * 2

    def test_check(self, example_progress_tracker):
        progress_tracker = example_progress_tracker
        step = 'evaluation_factors'
        assert progress_tracker.check(step) is False
        progress_tracker.step_set_active(step)
        assert progress_tracker.check(step) is True

    def test_active_step(self, example_progress_tracker):
        progress_tracker = example_progress_tracker
        step = 'decision_option_evaluation'
        assert progress_tracker.active_step == progress_tracker.steps[0]
        assert progress_tracker.next_step == progress_tracker.steps[1]
        with pytest.raises(ValueError):
            progress_tracker.prev_step()
        progress_tracker.step_set_active(step)
        assert progress_tracker.active_step == step
        with pytest.raises(ValueError):
            progress_tracker.next_step()
        assert progress_tracker.prev_step == progress_tracker.steps[-2]

    def test_next(self, example_progress_tracker):
        progress_tracker = example_progress_tracker
        progress_tracker.next()
        assert progress_tracker.active_step == progress_tracker.steps[1]
        progress_tracker.step_set_active(progress_tracker.steps[-1])
        with pytest.raises(ValueError):
            progress_tracker.next()

    def test_prev(self, example_progress_tracker):
        progress_tracker = example_progress_tracker
        with pytest.raises(ValueError):
            progress_tracker.back()
        progress_tracker.step_set_active(progress_tracker.steps[2])
        progress_tracker.back()
        assert progress_tracker.active_step == progress_tracker.steps[1]
