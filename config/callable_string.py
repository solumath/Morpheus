import discord


class CallableString(str):
    to_escape = ["role", "not_role", "line"]

    def __call__(self, *args, **kwargs):
        for arg in self.to_escape:
            if arg in kwargs:
                kwargs[arg] = discord.utils.escape_mentions(kwargs[arg])

        return self.format(**kwargs)


class Formatable(type):
    def __init__(cls, clsname, superclasses, attributedict):
        cls.clsname = clsname

    def __getattribute__(cls, key):
        try:
            return CallableString(object.__getattribute__(cls, key))
        except AttributeError:
            try:
                return CallableString(super().__getattribute__(key))
            except AttributeError:
                raise AttributeError(f"{cls.clsname} class has no attribute {key}")
