import json


class ProgressTracker:
    def __init__(self, steps: list[str], progress: list[bool] = None):
        if len(steps) != len(set(steps)):
            raise AssertionError(f"Duplicated steps are not supported. "
                                 f"Found {len(steps) - len(set(steps))} duplicated steps.")
        self.steps = steps
        self.steps_count = len(steps)
        self.progress = progress if progress else [True] + [False] * (len(steps) - 1)

    def __repr__(self):
        return json.dumps(self.to_dict(), indent=4)

    def to_dict(self):
        return {
            self.steps[i]: self.progress[i] for i in range(self.steps_count)
        }

    def __str__(self):
        return f"Progress tracker " \
               f"with {self.steps_count} steps " \
               f"and `{self.active_step}` active step."

    def __eq__(self, other) -> bool:
        if isinstance(other, ProgressTracker):
            return (
                self.steps == other.steps
                and self.progress == other.progress
            )
        return False

    def validate_step(self, step: str):
        if step not in self.steps:
            raise AssertionError(f"Step '{step}' is not in steps.")

    def step_set_active(self, step: str, value: bool = True):
        self.validate_step(step)
        self.progress[self.steps.index(step)] = value

    def steps_set_active(self, steps: list[str], value: bool = True):
        for step in steps:
            self.step_set_active(step, value)

    def prev_steps_set_active(self, step: str, value: bool = True):
        steps = self.steps[:(self.steps.index(step))]
        self.steps_set_active(steps, value)

    def next_steps_set_active(self, step: str, value: bool = True):
        steps = self.steps[(self.steps.index(step) + 1):]
        self.steps_set_active(steps, value)

    def check(self, step: str) -> bool:
        self.validate_step(step)
        return self.progress[self.steps.index(step)]

    @property
    def active_step(self):
        active_step = self.steps[0]
        for i, step in enumerate(self.steps):
            if self.progress[i]:
                active_step = step
        return active_step

    @property
    def next_step(self):
        next_step_index = self.steps.index(self.active_step) + 1
        if next_step_index >= self.steps_count:
            raise ValueError("No more steps.")
        return self.steps[next_step_index]

    @property
    def prev_step(self):
        prev_step_index = self.steps.index(self.active_step) - 1
        if prev_step_index < 0:
            raise ValueError("No previous steps.")
        return self.steps[prev_step_index]

    def next(self):
        next_step = self.next_step
        self.step_set_active(self.active_step, False)
        self.step_set_active(next_step, True)

    def back(self):
        prev_step = self.prev_step
        self.step_set_active(self.active_step, False)
        self.step_set_active(prev_step, True)

    def focus(self, step: str):
        self.steps_set_active(self.steps, False)
        self.step_set_active(step)

