# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild
# type: ignore

import kaitaistruct
from kaitaistruct import ReadWriteKaitaiStruct, KaitaiStream, BytesIO


if getattr(kaitaistruct, 'API_VERSION', (0, 9)) < (0, 11):
    raise Exception("Incompatible Kaitai Struct Python API: 0.11 or later is required, but you have %s" % (kaitaistruct.__version__))

class Nbfx(ReadWriteKaitaiStruct):
    def __init__(self, _io=None, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self

    def _read(self):
        self.records = []
        i = 0
        while not self._io.is_eof():
            _t_records = Nbfx.Record(self._io, self, self._root)
            _t_records._read()
            self.records.append(_t_records)
            i += 1



    def _fetch_instances(self):
        pass
        for i in range(len(self.records)):
            pass
            self.records[i]._fetch_instances()



    def _write__seq(self, io=None):
        super(Nbfx, self)._write__seq(io)
        for i in range(len(self.records)):
            pass
            if self._io.is_eof():
                raise kaitaistruct.ConsistencyError(u"records", self._io.size() - self._io.pos(), 0)
            self.records[i]._write__seq(self._io)

        if not self._io.is_eof():
            raise kaitaistruct.ConsistencyError(u"records", self._io.size() - self._io.pos(), 0)


    def _check(self):
        pass
        for i in range(len(self.records)):
            pass
            if self.records[i]._root != self._root:
                raise kaitaistruct.ConsistencyError(u"records", self.records[i]._root, self._root)
            if self.records[i]._parent != self:
                raise kaitaistruct.ConsistencyError(u"records", self.records[i]._parent, self)


    class PrefixDictionaryElement(ReadWriteKaitaiStruct):
        def __init__(self, _io=None, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root

        def _read(self):
            self.name_id = Nbfx.MultiByteInt31(self._io, self, self._root)
            self.name_id._read()


        def _fetch_instances(self):
            pass
            self.name_id._fetch_instances()


        def _write__seq(self, io=None):
            super(Nbfx.PrefixDictionaryElement, self)._write__seq(io)
            self.name_id._write__seq(self._io)


        def _check(self):
            pass
            if self.name_id._root != self._root:
                raise kaitaistruct.ConsistencyError(u"name_id", self.name_id._root, self._root)
            if self.name_id._parent != self:
                raise kaitaistruct.ConsistencyError(u"name_id", self.name_id._parent, self)


    class MultiByteInt31(ReadWriteKaitaiStruct):
        def __init__(self, _io=None, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root

        def _read(self):
            self.multibytes = []
            i = 0
            while True:
                _t_multibytes = Nbfx.Multibyte(self._io, self, self._root)
                _t_multibytes._read()
                _ = _t_multibytes
                self.multibytes.append(_)
                if not (_.has_next):
                    break
                i += 1


        def _fetch_instances(self):
            pass
            for i in range(len(self.multibytes)):
                pass
                self.multibytes[i]._fetch_instances()



        def _write__seq(self, io=None):
            super(Nbfx.MultiByteInt31, self)._write__seq(io)
            for i in range(len(self.multibytes)):
                pass
                self.multibytes[i]._write__seq(self._io)



        def _check(self):
            pass
            if (len(self.multibytes) == 0):
                raise kaitaistruct.ConsistencyError(u"multibytes", len(self.multibytes), 0)
            for i in range(len(self.multibytes)):
                pass
                if self.multibytes[i]._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"multibytes", self.multibytes[i]._root, self._root)
                if self.multibytes[i]._parent != self:
                    raise kaitaistruct.ConsistencyError(u"multibytes", self.multibytes[i]._parent, self)
                _ = self.multibytes[i]
                if (not (_.has_next) != (i == (len(self.multibytes) - 1))):
                    raise kaitaistruct.ConsistencyError(u"multibytes", not (_.has_next), (i == (len(self.multibytes) - 1)))



    class Multibyte(ReadWriteKaitaiStruct):
        def __init__(self, _io=None, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root

        def _read(self):
            self.has_next = self._io.read_bits_int_be(1) != 0
            self.value = self._io.read_bits_int_be(7)


        def _fetch_instances(self):
            pass


        def _write__seq(self, io=None):
            super(Nbfx.Multibyte, self)._write__seq(io)
            self._io.write_bits_int_be(1, int(self.has_next))
            self._io.write_bits_int_be(7, self.value)


        def _check(self):
            pass


    class UnknownByte(ReadWriteKaitaiStruct):
        def __init__(self, _io=None, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root

        def _read(self):
            self.value = self._io.read_u1()


        def _fetch_instances(self):
            pass


        def _write__seq(self, io=None):
            super(Nbfx.UnknownByte, self)._write__seq(io)
            self._io.write_u1(self.value)


        def _check(self):
            pass


    class DictionaryXmlsAttribute(ReadWriteKaitaiStruct):
        def __init__(self, _io=None, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root

        def _read(self):
            self.prefix = self._io.read_u2le()
            self.value = Nbfx.MultiByteInt31(self._io, self, self._root)
            self.value._read()


        def _fetch_instances(self):
            pass
            self.value._fetch_instances()


        def _write__seq(self, io=None):
            super(Nbfx.DictionaryXmlsAttribute, self)._write__seq(io)
            self._io.write_u2le(self.prefix)
            self.value._write__seq(self._io)


        def _check(self):
            pass
            if self.value._root != self._root:
                raise kaitaistruct.ConsistencyError(u"value", self.value._root, self._root)
            if self.value._parent != self:
                raise kaitaistruct.ConsistencyError(u"value", self.value._parent, self)


    class DictionaryText(ReadWriteKaitaiStruct):
        def __init__(self, _io=None, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root

        def _read(self):
            self.string_id = Nbfx.MultiByteInt31(self._io, self, self._root)
            self.string_id._read()


        def _fetch_instances(self):
            pass
            self.string_id._fetch_instances()


        def _write__seq(self, io=None):
            super(Nbfx.DictionaryText, self)._write__seq(io)
            self.string_id._write__seq(self._io)


        def _check(self):
            pass
            if self.string_id._root != self._root:
                raise kaitaistruct.ConsistencyError(u"string_id", self.string_id._root, self._root)
            if self.string_id._parent != self:
                raise kaitaistruct.ConsistencyError(u"string_id", self.string_id._parent, self)


    class OneText(ReadWriteKaitaiStruct):
        def __init__(self, _io=None, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root

        def _read(self):
            pass


        def _fetch_instances(self):
            pass


        def _write__seq(self, io=None):
            super(Nbfx.OneText, self)._write__seq(io)


        def _check(self):
            pass


    class PrefixAttribute(ReadWriteKaitaiStruct):
        def __init__(self, _io=None, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root

        def _read(self):
            self.name = Nbfx.NbfxString(self._io, self, self._root)
            self.name._read()
            self.value = Nbfx.NbfxString(self._io, self, self._root)
            self.value._read()


        def _fetch_instances(self):
            pass
            self.name._fetch_instances()
            self.value._fetch_instances()


        def _write__seq(self, io=None):
            super(Nbfx.PrefixAttribute, self)._write__seq(io)
            self.name._write__seq(self._io)
            self.value._write__seq(self._io)


        def _check(self):
            pass
            if self.name._root != self._root:
                raise kaitaistruct.ConsistencyError(u"name", self.name._root, self._root)
            if self.name._parent != self:
                raise kaitaistruct.ConsistencyError(u"name", self.name._parent, self)
            if self.value._root != self._root:
                raise kaitaistruct.ConsistencyError(u"value", self.value._root, self._root)
            if self.value._parent != self:
                raise kaitaistruct.ConsistencyError(u"value", self.value._parent, self)


    class Chars8Text(ReadWriteKaitaiStruct):
        def __init__(self, _io=None, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root

        def _read(self):
            self.length = self._io.read_u1()
            self.bytes = self._io.read_bytes(self.length)


        def _fetch_instances(self):
            pass


        def _write__seq(self, io=None):
            super(Nbfx.Chars8Text, self)._write__seq(io)
            self._io.write_u1(self.length)
            self._io.write_bytes(self.bytes)


        def _check(self):
            pass
            if (len(self.bytes) != self.length):
                raise kaitaistruct.ConsistencyError(u"bytes", len(self.bytes), self.length)


    class NbfxString(ReadWriteKaitaiStruct):
        def __init__(self, _io=None, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root

        def _read(self):
            self.str_len = self._io.read_u1()
            self.str = (self._io.read_bytes(self.str_len)).decode("ASCII")


        def _fetch_instances(self):
            pass


        def _write__seq(self, io=None):
            super(Nbfx.NbfxString, self)._write__seq(io)
            self._io.write_u1(self.str_len)
            self._io.write_bytes((self.str).encode(u"ASCII"))


        def _check(self):
            pass
            if (len((self.str).encode(u"ASCII")) != self.str_len):
                raise kaitaistruct.ConsistencyError(u"str", len((self.str).encode(u"ASCII")), self.str_len)


    class UniqueidText(ReadWriteKaitaiStruct):
        def __init__(self, _io=None, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root

        def _read(self):
            self.uuid = self._io.read_bytes(16)


        def _fetch_instances(self):
            pass


        def _write__seq(self, io=None):
            super(Nbfx.UniqueidText, self)._write__seq(io)
            self._io.write_bytes(self.uuid)


        def _check(self):
            pass
            if (len(self.uuid) != 16):
                raise kaitaistruct.ConsistencyError(u"uuid", len(self.uuid), 16)


    class PrefixDictionaryAttribute(ReadWriteKaitaiStruct):
        def __init__(self, _io=None, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root

        def _read(self):
            self.name_id = Nbfx.MultiByteInt31(self._io, self, self._root)
            self.name_id._read()


        def _fetch_instances(self):
            pass
            self.name_id._fetch_instances()


        def _write__seq(self, io=None):
            super(Nbfx.PrefixDictionaryAttribute, self)._write__seq(io)
            self.name_id._write__seq(self._io)


        def _check(self):
            pass
            if self.name_id._root != self._root:
                raise kaitaistruct.ConsistencyError(u"name_id", self.name_id._root, self._root)
            if self.name_id._parent != self:
                raise kaitaistruct.ConsistencyError(u"name_id", self.name_id._parent, self)


    class Record(ReadWriteKaitaiStruct):
        def __init__(self, _io=None, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root

        def _read(self):
            self.rec_type = self._io.read_u1()
            _on = self.rec_type
            if _on == 14:
                pass
                self.rec_body = Nbfx.PrefixDictionaryAttribute(self._io, self, self._root)
                self.rec_body._read()
            elif _on == 61:
                pass
                self.rec_body = Nbfx.PrefixAttribute(self._io, self, self._root)
                self.rec_body._read()
            elif _on == 17:
                pass
                self.rec_body = Nbfx.PrefixDictionaryAttribute(self._io, self, self._root)
                self.rec_body._read()
            elif _on == 47:
                pass
                self.rec_body = Nbfx.PrefixAttribute(self._io, self, self._root)
                self.rec_body._read()
            elif _on == 73:
                pass
                self.rec_body = Nbfx.PrefixDictionaryElement(self._io, self, self._root)
                self.rec_body._read()
            elif _on == 42:
                pass
                self.rec_body = Nbfx.PrefixAttribute(self._io, self, self._root)
                self.rec_body._read()
            elif _on == 46:
                pass
                self.rec_body = Nbfx.PrefixAttribute(self._io, self, self._root)
                self.rec_body._read()
            elif _on == 81:
                pass
                self.rec_body = Nbfx.PrefixDictionaryElement(self._io, self, self._root)
                self.rec_body._read()
            elif _on == 39:
                pass
                self.rec_body = Nbfx.PrefixAttribute(self._io, self, self._root)
                self.rec_body._read()
            elif _on == 60:
                pass
                self.rec_body = Nbfx.PrefixAttribute(self._io, self, self._root)
                self.rec_body._read()
            elif _on == 24:
                pass
                self.rec_body = Nbfx.PrefixDictionaryAttribute(self._io, self, self._root)
                self.rec_body._read()
            elif _on == 35:
                pass
                self.rec_body = Nbfx.PrefixDictionaryAttribute(self._io, self, self._root)
                self.rec_body._read()
            elif _on == 62:
                pass
                self.rec_body = Nbfx.PrefixAttribute(self._io, self, self._root)
                self.rec_body._read()
            elif _on == 20:
                pass
                self.rec_body = Nbfx.PrefixDictionaryAttribute(self._io, self, self._root)
                self.rec_body._read()
            elif _on == 32:
                pass
                self.rec_body = Nbfx.PrefixDictionaryAttribute(self._io, self, self._root)
                self.rec_body._read()
            elif _on == 1:
                pass
                self.rec_body = Nbfx.EndElement(self._io, self, self._root)
                self.rec_body._read()
            elif _on == 55:
                pass
                self.rec_body = Nbfx.PrefixAttribute(self._io, self, self._root)
                self.rec_body._read()
            elif _on == 27:
                pass
                self.rec_body = Nbfx.PrefixDictionaryAttribute(self._io, self, self._root)
                self.rec_body._read()
            elif _on == 77:
                pass
                self.rec_body = Nbfx.PrefixDictionaryElement(self._io, self, self._root)
                self.rec_body._read()
            elif _on == 13:
                pass
                self.rec_body = Nbfx.PrefixDictionaryAttribute(self._io, self, self._root)
                self.rec_body._read()
            elif _on == 52:
                pass
                self.rec_body = Nbfx.PrefixAttribute(self._io, self, self._root)
                self.rec_body._read()
            elif _on == 56:
                pass
                self.rec_body = Nbfx.PrefixAttribute(self._io, self, self._root)
                self.rec_body._read()
            elif _on == 45:
                pass
                self.rec_body = Nbfx.PrefixAttribute(self._io, self, self._root)
                self.rec_body._read()
            elif _on == 85:
                pass
                self.rec_body = Nbfx.PrefixDictionaryElement(self._io, self, self._root)
                self.rec_body._read()
            elif _on == 11:
                pass
                self.rec_body = Nbfx.DictionaryXmlsAttribute(self._io, self, self._root)
                self.rec_body._read()
            elif _on == 69:
                pass
                self.rec_body = Nbfx.PrefixDictionaryElement(self._io, self, self._root)
                self.rec_body._read()
            elif _on == 12:
                pass
                self.rec_body = Nbfx.PrefixDictionaryAttribute(self._io, self, self._root)
                self.rec_body._read()
            elif _on == 59:
                pass
                self.rec_body = Nbfx.PrefixAttribute(self._io, self, self._root)
                self.rec_body._read()
            elif _on == 58:
                pass
                self.rec_body = Nbfx.PrefixAttribute(self._io, self, self._root)
                self.rec_body._read()
            elif _on == 33:
                pass
                self.rec_body = Nbfx.PrefixDictionaryAttribute(self._io, self, self._root)
                self.rec_body._read()
            elif _on == 82:
                pass
                self.rec_body = Nbfx.PrefixDictionaryElement(self._io, self, self._root)
                self.rec_body._read()
            elif _on == 86:
                pass
                self.rec_body = Nbfx.PrefixDictionaryElement(self._io, self, self._root)
                self.rec_body._read()
            elif _on == 19:
                pass
                self.rec_body = Nbfx.PrefixDictionaryAttribute(self._io, self, self._root)
                self.rec_body._read()
            elif _on == 84:
                pass
                self.rec_body = Nbfx.PrefixDictionaryElement(self._io, self, self._root)
                self.rec_body._read()
            elif _on == 63:
                pass
                self.rec_body = Nbfx.PrefixAttribute(self._io, self, self._root)
                self.rec_body._read()
            elif _on == 51:
                pass
                self.rec_body = Nbfx.PrefixAttribute(self._io, self, self._root)
                self.rec_body._read()
            elif _on == 23:
                pass
                self.rec_body = Nbfx.PrefixDictionaryAttribute(self._io, self, self._root)
                self.rec_body._read()
            elif _on == 83:
                pass
                self.rec_body = Nbfx.PrefixDictionaryElement(self._io, self, self._root)
                self.rec_body._read()
            elif _on == 48:
                pass
                self.rec_body = Nbfx.PrefixAttribute(self._io, self, self._root)
                self.rec_body._read()
            elif _on == 153:
                pass
                self.rec_body = Nbfx.Chars8Text(self._io, self, self._root)
                self.rec_body._read()
            elif _on == 78:
                pass
                self.rec_body = Nbfx.PrefixDictionaryElement(self._io, self, self._root)
                self.rec_body._read()
            elif _on == 53:
                pass
                self.rec_body = Nbfx.PrefixAttribute(self._io, self, self._root)
                self.rec_body._read()
            elif _on == 15:
                pass
                self.rec_body = Nbfx.PrefixDictionaryAttribute(self._io, self, self._root)
                self.rec_body._read()
            elif _on == 38:
                pass
                self.rec_body = Nbfx.PrefixAttribute(self._io, self, self._root)
                self.rec_body._read()
            elif _on == 40:
                pass
                self.rec_body = Nbfx.PrefixAttribute(self._io, self, self._root)
                self.rec_body._read()
            elif _on == 152:
                pass
                self.rec_body = Nbfx.Chars8Text(self._io, self, self._root)
                self.rec_body._read()
            elif _on == 44:
                pass
                self.rec_body = Nbfx.PrefixAttribute(self._io, self, self._root)
                self.rec_body._read()
            elif _on == 76:
                pass
                self.rec_body = Nbfx.PrefixDictionaryElement(self._io, self, self._root)
                self.rec_body._read()
            elif _on == 79:
                pass
                self.rec_body = Nbfx.PrefixDictionaryElement(self._io, self, self._root)
                self.rec_body._read()
            elif _on == 57:
                pass
                self.rec_body = Nbfx.PrefixAttribute(self._io, self, self._root)
                self.rec_body._read()
            elif _on == 172:
                pass
                self.rec_body = Nbfx.UniqueidText(self._io, self, self._root)
                self.rec_body._read()
            elif _on == 130:
                pass
                self.rec_body = Nbfx.OneText(self._io, self, self._root)
                self.rec_body._read()
            elif _on == 21:
                pass
                self.rec_body = Nbfx.PrefixDictionaryAttribute(self._io, self, self._root)
                self.rec_body._read()
            elif _on == 170:
                pass
                self.rec_body = Nbfx.DictionaryText(self._io, self, self._root)
                self.rec_body._read()
            elif _on == 37:
                pass
                self.rec_body = Nbfx.PrefixDictionaryAttribute(self._io, self, self._root)
                self.rec_body._read()
            elif _on == 41:
                pass
                self.rec_body = Nbfx.PrefixAttribute(self._io, self, self._root)
                self.rec_body._read()
            elif _on == 72:
                pass
                self.rec_body = Nbfx.PrefixDictionaryElement(self._io, self, self._root)
                self.rec_body._read()
            elif _on == 71:
                pass
                self.rec_body = Nbfx.PrefixDictionaryElement(self._io, self, self._root)
                self.rec_body._read()
            elif _on == 171:
                pass
                self.rec_body = Nbfx.DictionaryText(self._io, self, self._root)
                self.rec_body._read()
            elif _on == 36:
                pass
                self.rec_body = Nbfx.PrefixDictionaryAttribute(self._io, self, self._root)
                self.rec_body._read()
            elif _on == 70:
                pass
                self.rec_body = Nbfx.PrefixDictionaryElement(self._io, self, self._root)
                self.rec_body._read()
            elif _on == 28:
                pass
                self.rec_body = Nbfx.PrefixDictionaryAttribute(self._io, self, self._root)
                self.rec_body._read()
            elif _on == 74:
                pass
                self.rec_body = Nbfx.PrefixDictionaryElement(self._io, self, self._root)
                self.rec_body._read()
            elif _on == 16:
                pass
                self.rec_body = Nbfx.PrefixDictionaryAttribute(self._io, self, self._root)
                self.rec_body._read()
            elif _on == 18:
                pass
                self.rec_body = Nbfx.PrefixDictionaryAttribute(self._io, self, self._root)
                self.rec_body._read()
            elif _on == 80:
                pass
                self.rec_body = Nbfx.PrefixDictionaryElement(self._io, self, self._root)
                self.rec_body._read()
            elif _on == 68:
                pass
                self.rec_body = Nbfx.PrefixDictionaryElement(self._io, self, self._root)
                self.rec_body._read()
            elif _on == 26:
                pass
                self.rec_body = Nbfx.PrefixDictionaryAttribute(self._io, self, self._root)
                self.rec_body._read()
            elif _on == 31:
                pass
                self.rec_body = Nbfx.PrefixDictionaryAttribute(self._io, self, self._root)
                self.rec_body._read()
            elif _on == 49:
                pass
                self.rec_body = Nbfx.PrefixAttribute(self._io, self, self._root)
                self.rec_body._read()
            elif _on == 34:
                pass
                self.rec_body = Nbfx.PrefixDictionaryAttribute(self._io, self, self._root)
                self.rec_body._read()
            elif _on == 54:
                pass
                self.rec_body = Nbfx.PrefixAttribute(self._io, self, self._root)
                self.rec_body._read()
            elif _on == 29:
                pass
                self.rec_body = Nbfx.PrefixDictionaryAttribute(self._io, self, self._root)
                self.rec_body._read()
            elif _on == 75:
                pass
                self.rec_body = Nbfx.PrefixDictionaryElement(self._io, self, self._root)
                self.rec_body._read()
            elif _on == 25:
                pass
                self.rec_body = Nbfx.PrefixDictionaryAttribute(self._io, self, self._root)
                self.rec_body._read()
            elif _on == 43:
                pass
                self.rec_body = Nbfx.PrefixAttribute(self._io, self, self._root)
                self.rec_body._read()
            elif _on == 50:
                pass
                self.rec_body = Nbfx.PrefixAttribute(self._io, self, self._root)
                self.rec_body._read()
            elif _on == 22:
                pass
                self.rec_body = Nbfx.PrefixDictionaryAttribute(self._io, self, self._root)
                self.rec_body._read()
            elif _on == 30:
                pass
                self.rec_body = Nbfx.PrefixDictionaryAttribute(self._io, self, self._root)
                self.rec_body._read()
            elif _on == 173:
                pass
                self.rec_body = Nbfx.UniqueidText(self._io, self, self._root)
                self.rec_body._read()


        def _fetch_instances(self):
            pass
            _on = self.rec_type
            if _on == 14:
                pass
                self.rec_body._fetch_instances()
            elif _on == 61:
                pass
                self.rec_body._fetch_instances()
            elif _on == 17:
                pass
                self.rec_body._fetch_instances()
            elif _on == 47:
                pass
                self.rec_body._fetch_instances()
            elif _on == 73:
                pass
                self.rec_body._fetch_instances()
            elif _on == 42:
                pass
                self.rec_body._fetch_instances()
            elif _on == 46:
                pass
                self.rec_body._fetch_instances()
            elif _on == 81:
                pass
                self.rec_body._fetch_instances()
            elif _on == 39:
                pass
                self.rec_body._fetch_instances()
            elif _on == 60:
                pass
                self.rec_body._fetch_instances()
            elif _on == 24:
                pass
                self.rec_body._fetch_instances()
            elif _on == 35:
                pass
                self.rec_body._fetch_instances()
            elif _on == 62:
                pass
                self.rec_body._fetch_instances()
            elif _on == 20:
                pass
                self.rec_body._fetch_instances()
            elif _on == 32:
                pass
                self.rec_body._fetch_instances()
            elif _on == 1:
                pass
                self.rec_body._fetch_instances()
            elif _on == 55:
                pass
                self.rec_body._fetch_instances()
            elif _on == 27:
                pass
                self.rec_body._fetch_instances()
            elif _on == 77:
                pass
                self.rec_body._fetch_instances()
            elif _on == 13:
                pass
                self.rec_body._fetch_instances()
            elif _on == 52:
                pass
                self.rec_body._fetch_instances()
            elif _on == 56:
                pass
                self.rec_body._fetch_instances()
            elif _on == 45:
                pass
                self.rec_body._fetch_instances()
            elif _on == 85:
                pass
                self.rec_body._fetch_instances()
            elif _on == 11:
                pass
                self.rec_body._fetch_instances()
            elif _on == 69:
                pass
                self.rec_body._fetch_instances()
            elif _on == 12:
                pass
                self.rec_body._fetch_instances()
            elif _on == 59:
                pass
                self.rec_body._fetch_instances()
            elif _on == 58:
                pass
                self.rec_body._fetch_instances()
            elif _on == 33:
                pass
                self.rec_body._fetch_instances()
            elif _on == 82:
                pass
                self.rec_body._fetch_instances()
            elif _on == 86:
                pass
                self.rec_body._fetch_instances()
            elif _on == 19:
                pass
                self.rec_body._fetch_instances()
            elif _on == 84:
                pass
                self.rec_body._fetch_instances()
            elif _on == 63:
                pass
                self.rec_body._fetch_instances()
            elif _on == 51:
                pass
                self.rec_body._fetch_instances()
            elif _on == 23:
                pass
                self.rec_body._fetch_instances()
            elif _on == 83:
                pass
                self.rec_body._fetch_instances()
            elif _on == 48:
                pass
                self.rec_body._fetch_instances()
            elif _on == 153:
                pass
                self.rec_body._fetch_instances()
            elif _on == 78:
                pass
                self.rec_body._fetch_instances()
            elif _on == 53:
                pass
                self.rec_body._fetch_instances()
            elif _on == 15:
                pass
                self.rec_body._fetch_instances()
            elif _on == 38:
                pass
                self.rec_body._fetch_instances()
            elif _on == 40:
                pass
                self.rec_body._fetch_instances()
            elif _on == 152:
                pass
                self.rec_body._fetch_instances()
            elif _on == 44:
                pass
                self.rec_body._fetch_instances()
            elif _on == 76:
                pass
                self.rec_body._fetch_instances()
            elif _on == 79:
                pass
                self.rec_body._fetch_instances()
            elif _on == 57:
                pass
                self.rec_body._fetch_instances()
            elif _on == 172:
                pass
                self.rec_body._fetch_instances()
            elif _on == 130:
                pass
                self.rec_body._fetch_instances()
            elif _on == 21:
                pass
                self.rec_body._fetch_instances()
            elif _on == 170:
                pass
                self.rec_body._fetch_instances()
            elif _on == 37:
                pass
                self.rec_body._fetch_instances()
            elif _on == 41:
                pass
                self.rec_body._fetch_instances()
            elif _on == 72:
                pass
                self.rec_body._fetch_instances()
            elif _on == 71:
                pass
                self.rec_body._fetch_instances()
            elif _on == 171:
                pass
                self.rec_body._fetch_instances()
            elif _on == 36:
                pass
                self.rec_body._fetch_instances()
            elif _on == 70:
                pass
                self.rec_body._fetch_instances()
            elif _on == 28:
                pass
                self.rec_body._fetch_instances()
            elif _on == 74:
                pass
                self.rec_body._fetch_instances()
            elif _on == 16:
                pass
                self.rec_body._fetch_instances()
            elif _on == 18:
                pass
                self.rec_body._fetch_instances()
            elif _on == 80:
                pass
                self.rec_body._fetch_instances()
            elif _on == 68:
                pass
                self.rec_body._fetch_instances()
            elif _on == 26:
                pass
                self.rec_body._fetch_instances()
            elif _on == 31:
                pass
                self.rec_body._fetch_instances()
            elif _on == 49:
                pass
                self.rec_body._fetch_instances()
            elif _on == 34:
                pass
                self.rec_body._fetch_instances()
            elif _on == 54:
                pass
                self.rec_body._fetch_instances()
            elif _on == 29:
                pass
                self.rec_body._fetch_instances()
            elif _on == 75:
                pass
                self.rec_body._fetch_instances()
            elif _on == 25:
                pass
                self.rec_body._fetch_instances()
            elif _on == 43:
                pass
                self.rec_body._fetch_instances()
            elif _on == 50:
                pass
                self.rec_body._fetch_instances()
            elif _on == 22:
                pass
                self.rec_body._fetch_instances()
            elif _on == 30:
                pass
                self.rec_body._fetch_instances()
            elif _on == 173:
                pass
                self.rec_body._fetch_instances()


        def _write__seq(self, io=None):
            super(Nbfx.Record, self)._write__seq(io)
            self._io.write_u1(self.rec_type)
            _on = self.rec_type
            if _on == 14:
                pass
                self.rec_body._write__seq(self._io)
            elif _on == 61:
                pass
                self.rec_body._write__seq(self._io)
            elif _on == 17:
                pass
                self.rec_body._write__seq(self._io)
            elif _on == 47:
                pass
                self.rec_body._write__seq(self._io)
            elif _on == 73:
                pass
                self.rec_body._write__seq(self._io)
            elif _on == 42:
                pass
                self.rec_body._write__seq(self._io)
            elif _on == 46:
                pass
                self.rec_body._write__seq(self._io)
            elif _on == 81:
                pass
                self.rec_body._write__seq(self._io)
            elif _on == 39:
                pass
                self.rec_body._write__seq(self._io)
            elif _on == 60:
                pass
                self.rec_body._write__seq(self._io)
            elif _on == 24:
                pass
                self.rec_body._write__seq(self._io)
            elif _on == 35:
                pass
                self.rec_body._write__seq(self._io)
            elif _on == 62:
                pass
                self.rec_body._write__seq(self._io)
            elif _on == 20:
                pass
                self.rec_body._write__seq(self._io)
            elif _on == 32:
                pass
                self.rec_body._write__seq(self._io)
            elif _on == 1:
                pass
                self.rec_body._write__seq(self._io)
            elif _on == 55:
                pass
                self.rec_body._write__seq(self._io)
            elif _on == 27:
                pass
                self.rec_body._write__seq(self._io)
            elif _on == 77:
                pass
                self.rec_body._write__seq(self._io)
            elif _on == 13:
                pass
                self.rec_body._write__seq(self._io)
            elif _on == 52:
                pass
                self.rec_body._write__seq(self._io)
            elif _on == 56:
                pass
                self.rec_body._write__seq(self._io)
            elif _on == 45:
                pass
                self.rec_body._write__seq(self._io)
            elif _on == 85:
                pass
                self.rec_body._write__seq(self._io)
            elif _on == 11:
                pass
                self.rec_body._write__seq(self._io)
            elif _on == 69:
                pass
                self.rec_body._write__seq(self._io)
            elif _on == 12:
                pass
                self.rec_body._write__seq(self._io)
            elif _on == 59:
                pass
                self.rec_body._write__seq(self._io)
            elif _on == 58:
                pass
                self.rec_body._write__seq(self._io)
            elif _on == 33:
                pass
                self.rec_body._write__seq(self._io)
            elif _on == 82:
                pass
                self.rec_body._write__seq(self._io)
            elif _on == 86:
                pass
                self.rec_body._write__seq(self._io)
            elif _on == 19:
                pass
                self.rec_body._write__seq(self._io)
            elif _on == 84:
                pass
                self.rec_body._write__seq(self._io)
            elif _on == 63:
                pass
                self.rec_body._write__seq(self._io)
            elif _on == 51:
                pass
                self.rec_body._write__seq(self._io)
            elif _on == 23:
                pass
                self.rec_body._write__seq(self._io)
            elif _on == 83:
                pass
                self.rec_body._write__seq(self._io)
            elif _on == 48:
                pass
                self.rec_body._write__seq(self._io)
            elif _on == 153:
                pass
                self.rec_body._write__seq(self._io)
            elif _on == 78:
                pass
                self.rec_body._write__seq(self._io)
            elif _on == 53:
                pass
                self.rec_body._write__seq(self._io)
            elif _on == 15:
                pass
                self.rec_body._write__seq(self._io)
            elif _on == 38:
                pass
                self.rec_body._write__seq(self._io)
            elif _on == 40:
                pass
                self.rec_body._write__seq(self._io)
            elif _on == 152:
                pass
                self.rec_body._write__seq(self._io)
            elif _on == 44:
                pass
                self.rec_body._write__seq(self._io)
            elif _on == 76:
                pass
                self.rec_body._write__seq(self._io)
            elif _on == 79:
                pass
                self.rec_body._write__seq(self._io)
            elif _on == 57:
                pass
                self.rec_body._write__seq(self._io)
            elif _on == 172:
                pass
                self.rec_body._write__seq(self._io)
            elif _on == 130:
                pass
                self.rec_body._write__seq(self._io)
            elif _on == 21:
                pass
                self.rec_body._write__seq(self._io)
            elif _on == 170:
                pass
                self.rec_body._write__seq(self._io)
            elif _on == 37:
                pass
                self.rec_body._write__seq(self._io)
            elif _on == 41:
                pass
                self.rec_body._write__seq(self._io)
            elif _on == 72:
                pass
                self.rec_body._write__seq(self._io)
            elif _on == 71:
                pass
                self.rec_body._write__seq(self._io)
            elif _on == 171:
                pass
                self.rec_body._write__seq(self._io)
            elif _on == 36:
                pass
                self.rec_body._write__seq(self._io)
            elif _on == 70:
                pass
                self.rec_body._write__seq(self._io)
            elif _on == 28:
                pass
                self.rec_body._write__seq(self._io)
            elif _on == 74:
                pass
                self.rec_body._write__seq(self._io)
            elif _on == 16:
                pass
                self.rec_body._write__seq(self._io)
            elif _on == 18:
                pass
                self.rec_body._write__seq(self._io)
            elif _on == 80:
                pass
                self.rec_body._write__seq(self._io)
            elif _on == 68:
                pass
                self.rec_body._write__seq(self._io)
            elif _on == 26:
                pass
                self.rec_body._write__seq(self._io)
            elif _on == 31:
                pass
                self.rec_body._write__seq(self._io)
            elif _on == 49:
                pass
                self.rec_body._write__seq(self._io)
            elif _on == 34:
                pass
                self.rec_body._write__seq(self._io)
            elif _on == 54:
                pass
                self.rec_body._write__seq(self._io)
            elif _on == 29:
                pass
                self.rec_body._write__seq(self._io)
            elif _on == 75:
                pass
                self.rec_body._write__seq(self._io)
            elif _on == 25:
                pass
                self.rec_body._write__seq(self._io)
            elif _on == 43:
                pass
                self.rec_body._write__seq(self._io)
            elif _on == 50:
                pass
                self.rec_body._write__seq(self._io)
            elif _on == 22:
                pass
                self.rec_body._write__seq(self._io)
            elif _on == 30:
                pass
                self.rec_body._write__seq(self._io)
            elif _on == 173:
                pass
                self.rec_body._write__seq(self._io)


        def _check(self):
            pass
            _on = self.rec_type
            if _on == 14:
                pass
                if self.rec_body._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._root, self._root)
                if self.rec_body._parent != self:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._parent, self)
            elif _on == 61:
                pass
                if self.rec_body._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._root, self._root)
                if self.rec_body._parent != self:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._parent, self)
            elif _on == 17:
                pass
                if self.rec_body._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._root, self._root)
                if self.rec_body._parent != self:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._parent, self)
            elif _on == 47:
                pass
                if self.rec_body._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._root, self._root)
                if self.rec_body._parent != self:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._parent, self)
            elif _on == 73:
                pass
                if self.rec_body._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._root, self._root)
                if self.rec_body._parent != self:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._parent, self)
            elif _on == 42:
                pass
                if self.rec_body._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._root, self._root)
                if self.rec_body._parent != self:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._parent, self)
            elif _on == 46:
                pass
                if self.rec_body._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._root, self._root)
                if self.rec_body._parent != self:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._parent, self)
            elif _on == 81:
                pass
                if self.rec_body._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._root, self._root)
                if self.rec_body._parent != self:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._parent, self)
            elif _on == 39:
                pass
                if self.rec_body._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._root, self._root)
                if self.rec_body._parent != self:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._parent, self)
            elif _on == 60:
                pass
                if self.rec_body._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._root, self._root)
                if self.rec_body._parent != self:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._parent, self)
            elif _on == 24:
                pass
                if self.rec_body._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._root, self._root)
                if self.rec_body._parent != self:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._parent, self)
            elif _on == 35:
                pass
                if self.rec_body._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._root, self._root)
                if self.rec_body._parent != self:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._parent, self)
            elif _on == 62:
                pass
                if self.rec_body._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._root, self._root)
                if self.rec_body._parent != self:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._parent, self)
            elif _on == 20:
                pass
                if self.rec_body._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._root, self._root)
                if self.rec_body._parent != self:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._parent, self)
            elif _on == 32:
                pass
                if self.rec_body._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._root, self._root)
                if self.rec_body._parent != self:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._parent, self)
            elif _on == 1:
                pass
                if self.rec_body._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._root, self._root)
                if self.rec_body._parent != self:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._parent, self)
            elif _on == 55:
                pass
                if self.rec_body._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._root, self._root)
                if self.rec_body._parent != self:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._parent, self)
            elif _on == 27:
                pass
                if self.rec_body._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._root, self._root)
                if self.rec_body._parent != self:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._parent, self)
            elif _on == 77:
                pass
                if self.rec_body._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._root, self._root)
                if self.rec_body._parent != self:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._parent, self)
            elif _on == 13:
                pass
                if self.rec_body._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._root, self._root)
                if self.rec_body._parent != self:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._parent, self)
            elif _on == 52:
                pass
                if self.rec_body._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._root, self._root)
                if self.rec_body._parent != self:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._parent, self)
            elif _on == 56:
                pass
                if self.rec_body._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._root, self._root)
                if self.rec_body._parent != self:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._parent, self)
            elif _on == 45:
                pass
                if self.rec_body._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._root, self._root)
                if self.rec_body._parent != self:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._parent, self)
            elif _on == 85:
                pass
                if self.rec_body._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._root, self._root)
                if self.rec_body._parent != self:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._parent, self)
            elif _on == 11:
                pass
                if self.rec_body._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._root, self._root)
                if self.rec_body._parent != self:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._parent, self)
            elif _on == 69:
                pass
                if self.rec_body._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._root, self._root)
                if self.rec_body._parent != self:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._parent, self)
            elif _on == 12:
                pass
                if self.rec_body._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._root, self._root)
                if self.rec_body._parent != self:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._parent, self)
            elif _on == 59:
                pass
                if self.rec_body._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._root, self._root)
                if self.rec_body._parent != self:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._parent, self)
            elif _on == 58:
                pass
                if self.rec_body._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._root, self._root)
                if self.rec_body._parent != self:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._parent, self)
            elif _on == 33:
                pass
                if self.rec_body._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._root, self._root)
                if self.rec_body._parent != self:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._parent, self)
            elif _on == 82:
                pass
                if self.rec_body._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._root, self._root)
                if self.rec_body._parent != self:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._parent, self)
            elif _on == 86:
                pass
                if self.rec_body._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._root, self._root)
                if self.rec_body._parent != self:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._parent, self)
            elif _on == 19:
                pass
                if self.rec_body._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._root, self._root)
                if self.rec_body._parent != self:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._parent, self)
            elif _on == 84:
                pass
                if self.rec_body._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._root, self._root)
                if self.rec_body._parent != self:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._parent, self)
            elif _on == 63:
                pass
                if self.rec_body._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._root, self._root)
                if self.rec_body._parent != self:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._parent, self)
            elif _on == 51:
                pass
                if self.rec_body._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._root, self._root)
                if self.rec_body._parent != self:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._parent, self)
            elif _on == 23:
                pass
                if self.rec_body._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._root, self._root)
                if self.rec_body._parent != self:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._parent, self)
            elif _on == 83:
                pass
                if self.rec_body._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._root, self._root)
                if self.rec_body._parent != self:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._parent, self)
            elif _on == 48:
                pass
                if self.rec_body._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._root, self._root)
                if self.rec_body._parent != self:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._parent, self)
            elif _on == 153:
                pass
                if self.rec_body._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._root, self._root)
                if self.rec_body._parent != self:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._parent, self)
            elif _on == 78:
                pass
                if self.rec_body._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._root, self._root)
                if self.rec_body._parent != self:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._parent, self)
            elif _on == 53:
                pass
                if self.rec_body._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._root, self._root)
                if self.rec_body._parent != self:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._parent, self)
            elif _on == 15:
                pass
                if self.rec_body._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._root, self._root)
                if self.rec_body._parent != self:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._parent, self)
            elif _on == 38:
                pass
                if self.rec_body._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._root, self._root)
                if self.rec_body._parent != self:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._parent, self)
            elif _on == 40:
                pass
                if self.rec_body._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._root, self._root)
                if self.rec_body._parent != self:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._parent, self)
            elif _on == 152:
                pass
                if self.rec_body._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._root, self._root)
                if self.rec_body._parent != self:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._parent, self)
            elif _on == 44:
                pass
                if self.rec_body._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._root, self._root)
                if self.rec_body._parent != self:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._parent, self)
            elif _on == 76:
                pass
                if self.rec_body._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._root, self._root)
                if self.rec_body._parent != self:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._parent, self)
            elif _on == 79:
                pass
                if self.rec_body._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._root, self._root)
                if self.rec_body._parent != self:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._parent, self)
            elif _on == 57:
                pass
                if self.rec_body._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._root, self._root)
                if self.rec_body._parent != self:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._parent, self)
            elif _on == 172:
                pass
                if self.rec_body._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._root, self._root)
                if self.rec_body._parent != self:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._parent, self)
            elif _on == 130:
                pass
                if self.rec_body._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._root, self._root)
                if self.rec_body._parent != self:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._parent, self)
            elif _on == 21:
                pass
                if self.rec_body._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._root, self._root)
                if self.rec_body._parent != self:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._parent, self)
            elif _on == 170:
                pass
                if self.rec_body._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._root, self._root)
                if self.rec_body._parent != self:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._parent, self)
            elif _on == 37:
                pass
                if self.rec_body._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._root, self._root)
                if self.rec_body._parent != self:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._parent, self)
            elif _on == 41:
                pass
                if self.rec_body._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._root, self._root)
                if self.rec_body._parent != self:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._parent, self)
            elif _on == 72:
                pass
                if self.rec_body._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._root, self._root)
                if self.rec_body._parent != self:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._parent, self)
            elif _on == 71:
                pass
                if self.rec_body._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._root, self._root)
                if self.rec_body._parent != self:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._parent, self)
            elif _on == 171:
                pass
                if self.rec_body._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._root, self._root)
                if self.rec_body._parent != self:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._parent, self)
            elif _on == 36:
                pass
                if self.rec_body._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._root, self._root)
                if self.rec_body._parent != self:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._parent, self)
            elif _on == 70:
                pass
                if self.rec_body._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._root, self._root)
                if self.rec_body._parent != self:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._parent, self)
            elif _on == 28:
                pass
                if self.rec_body._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._root, self._root)
                if self.rec_body._parent != self:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._parent, self)
            elif _on == 74:
                pass
                if self.rec_body._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._root, self._root)
                if self.rec_body._parent != self:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._parent, self)
            elif _on == 16:
                pass
                if self.rec_body._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._root, self._root)
                if self.rec_body._parent != self:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._parent, self)
            elif _on == 18:
                pass
                if self.rec_body._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._root, self._root)
                if self.rec_body._parent != self:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._parent, self)
            elif _on == 80:
                pass
                if self.rec_body._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._root, self._root)
                if self.rec_body._parent != self:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._parent, self)
            elif _on == 68:
                pass
                if self.rec_body._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._root, self._root)
                if self.rec_body._parent != self:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._parent, self)
            elif _on == 26:
                pass
                if self.rec_body._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._root, self._root)
                if self.rec_body._parent != self:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._parent, self)
            elif _on == 31:
                pass
                if self.rec_body._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._root, self._root)
                if self.rec_body._parent != self:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._parent, self)
            elif _on == 49:
                pass
                if self.rec_body._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._root, self._root)
                if self.rec_body._parent != self:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._parent, self)
            elif _on == 34:
                pass
                if self.rec_body._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._root, self._root)
                if self.rec_body._parent != self:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._parent, self)
            elif _on == 54:
                pass
                if self.rec_body._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._root, self._root)
                if self.rec_body._parent != self:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._parent, self)
            elif _on == 29:
                pass
                if self.rec_body._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._root, self._root)
                if self.rec_body._parent != self:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._parent, self)
            elif _on == 75:
                pass
                if self.rec_body._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._root, self._root)
                if self.rec_body._parent != self:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._parent, self)
            elif _on == 25:
                pass
                if self.rec_body._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._root, self._root)
                if self.rec_body._parent != self:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._parent, self)
            elif _on == 43:
                pass
                if self.rec_body._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._root, self._root)
                if self.rec_body._parent != self:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._parent, self)
            elif _on == 50:
                pass
                if self.rec_body._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._root, self._root)
                if self.rec_body._parent != self:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._parent, self)
            elif _on == 22:
                pass
                if self.rec_body._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._root, self._root)
                if self.rec_body._parent != self:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._parent, self)
            elif _on == 30:
                pass
                if self.rec_body._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._root, self._root)
                if self.rec_body._parent != self:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._parent, self)
            elif _on == 173:
                pass
                if self.rec_body._root != self._root:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._root, self._root)
                if self.rec_body._parent != self:
                    raise kaitaistruct.ConsistencyError(u"rec_body", self.rec_body._parent, self)


    class EndElement(ReadWriteKaitaiStruct):
        def __init__(self, _io=None, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root

        def _read(self):
            pass


        def _fetch_instances(self):
            pass


        def _write__seq(self, io=None):
            super(Nbfx.EndElement, self)._write__seq(io)


        def _check(self):
            pass



