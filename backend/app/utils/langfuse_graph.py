from app.utils.langfuse_utils import langfuse_client


class LangfuseGraphTrace:

    def __init__(self, name: str):
        self.name = name

    def __enter__(self):
        self.trace = langfuse_client.start_as_current_observation(
            name=self.name,
        )
        self.span = self.trace.__enter__()
        return self

    def __exit__(self, exc_type, exc, tb):
        return self.trace.__exit__(exc_type, exc, tb)

    def update(self, **kwargs):
        self.span.update(**kwargs)
