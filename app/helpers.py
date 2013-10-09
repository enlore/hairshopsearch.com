import simplejson as json

class JSONSerializer():
    """Smart mixin that tags a SQLAlchemy model as serializable"""

    __json_public__     = None
    __json_hidden__     = None
    __json_modifiers__  = None

    def get_attrs(self):
        for name in self.__mapper__.iterate_properties:
            yield name.key

    def to_json(self):
        names = self.get_attrs()
        public = self.__json_public__ or names
        hidden = self.__json_hidden__ or []
        modifiers = self.__json_modifiers__ or dict()

        ret = dict()
        for key in public:
            ret[key] = getattr(self, key)
        for key, modifier in modifiers.items():
            val = modifier(getattr(self, key))
            ret[key] = val
        for key in hidden:
            ret.pop(key, None)
        return ret

class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, JSONSerializer):
            return obj.to_json()
        return super(JSONEncoder, self).default(obj)
