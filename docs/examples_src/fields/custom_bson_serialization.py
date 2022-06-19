from bson import Binary

from odmantic import AIOEngine, Model


class ASCIISerializedAsBinary(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if isinstance(v, bytes):  # Handle data coming from MongoDB
            return v.decode("ascii")
        if not isinstance(v, str):
            raise TypeError("string required")
        if not v.isascii():
            raise ValueError("Only ascii characters are allowed")
        return v

    @classmethod
    def __bson__(cls, v: str):
        return v.encode("ascii")


class Example(Model):
    field: ASCIISerializedAsBinary


engine = AIOEngine()
await engine.save(Example(field="hello world"))
fetched = await engine.find_one(Example)
print(fetched.field)
#> hello world
