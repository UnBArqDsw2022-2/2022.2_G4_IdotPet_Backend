import pydantic


class AllOptionalMeta(pydantic.main.ModelMetaclass):
    """Converts all fields from a Pydantic Model to optional."""

    def __new__(cls, name, bases, namespaces, **kwargs):
        annotations = namespaces.get('__annotations__', {})
        for base in bases:
            annotations.update({value.name: value.annotation for value in base.__fields__.values()})
            annotations.update(base.__annotations__)
        for field in annotations:
            if not field.startswith('__'):
                annotations[field] = annotations[field] | None
        namespaces['__annotations__'] = annotations
        return super().__new__(cls, name, bases, namespaces, **kwargs)
