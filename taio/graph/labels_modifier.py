class LabelsModifier:
    # TODO: need refactor
    DEFAULT_MODIFIER = lambda x: x

    def __init__(self, **kwargs):
        self._modifiers = kwargs

    def modify(self, label, value):
        return self.get(label)(value)

    def get(self, label, fallback=DEFAULT_MODIFIER):
        return self._modifiers.get(label, fallback)
