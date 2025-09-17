class AnnotationNotFoundError(Exception):
    ...

class AnnotationOverlapError(Exception):
    def __init__(self, msg="Provided annotations are not the same."):
        super().__init__(msg)

