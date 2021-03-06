# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: karps/proto/std.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from karps.proto import computation_pb2 as karps_dot_proto_dot_computation__pb2
from karps.proto import structured_transform_pb2 as karps_dot_proto_dot_structured__transform__pb2
from karps.proto import graph_pb2 as karps_dot_proto_dot_graph__pb2
from karps.proto import types_pb2 as karps_dot_proto_dot_types__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='karps/proto/std.proto',
  package='karps.core',
  syntax='proto3',
  serialized_pb=_b('\n\x15karps/proto/std.proto\x12\nkarps.core\x1a\x1dkarps/proto/computation.proto\x1a&karps/proto/structured_transform.proto\x1a\x17karps/proto/graph.proto\x1a\x17karps/proto/types.proto\"]\n\x0bPlaceholder\x12&\n\x08locality\x18\x01 \x01(\x0e\x32\x14.karps.core.Locality\x12&\n\tdata_type\x18\x02 \x01(\x0b\x32\x13.karps.core.SQLType\"2\n\x07Shuffle\x12\'\n\x06\x61gg_op\x18\x01 \x01(\x0b\x32\x17.karps.core.Aggregation\"9\n\x13StructuredTransform\x12\"\n\x06\x63ol_op\x18\x01 \x01(\x0b\x32\x12.karps.core.Column\">\n\x18LocalStructuredTransform\x12\"\n\x06\x63ol_op\x18\x01 \x01(\x0b\x32\x12.karps.core.Column\";\n\x10StructuredReduce\x12\'\n\x06\x61gg_op\x18\x01 \x01(\x0b\x32\x17.karps.core.Aggregation\"\x8c\x01\n\x0cLocalPointer\x12.\n\x0b\x63omputation\x18\x01 \x01(\x0b\x32\x19.karps.core.ComputationId\x12$\n\nlocal_path\x18\x02 \x01(\x0b\x32\x10.karps.core.Path\x12&\n\tdata_type\x18\x04 \x01(\x0b\x32\x13.karps.core.SQLType\"L\n\x04Join\x12-\n\njoint_type\x18\x01 \x01(\x0e\x32\x19.karps.core.Join.JoinType\"\x15\n\x08JoinType\x12\t\n\x05INNER\x10\x00\x62\x06proto3')
  ,
  dependencies=[karps_dot_proto_dot_computation__pb2.DESCRIPTOR,karps_dot_proto_dot_structured__transform__pb2.DESCRIPTOR,karps_dot_proto_dot_graph__pb2.DESCRIPTOR,karps_dot_proto_dot_types__pb2.DESCRIPTOR,])



_JOIN_JOINTYPE = _descriptor.EnumDescriptor(
  name='JoinType',
  full_name='karps.core.Join.JoinType',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='INNER', index=0, number=0,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=687,
  serialized_end=708,
)
_sym_db.RegisterEnumDescriptor(_JOIN_JOINTYPE)


_PLACEHOLDER = _descriptor.Descriptor(
  name='Placeholder',
  full_name='karps.core.Placeholder',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='locality', full_name='karps.core.Placeholder.locality', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='data_type', full_name='karps.core.Placeholder.data_type', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=158,
  serialized_end=251,
)


_SHUFFLE = _descriptor.Descriptor(
  name='Shuffle',
  full_name='karps.core.Shuffle',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='agg_op', full_name='karps.core.Shuffle.agg_op', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=253,
  serialized_end=303,
)


_STRUCTUREDTRANSFORM = _descriptor.Descriptor(
  name='StructuredTransform',
  full_name='karps.core.StructuredTransform',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='col_op', full_name='karps.core.StructuredTransform.col_op', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=305,
  serialized_end=362,
)


_LOCALSTRUCTUREDTRANSFORM = _descriptor.Descriptor(
  name='LocalStructuredTransform',
  full_name='karps.core.LocalStructuredTransform',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='col_op', full_name='karps.core.LocalStructuredTransform.col_op', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=364,
  serialized_end=426,
)


_STRUCTUREDREDUCE = _descriptor.Descriptor(
  name='StructuredReduce',
  full_name='karps.core.StructuredReduce',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='agg_op', full_name='karps.core.StructuredReduce.agg_op', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=428,
  serialized_end=487,
)


_LOCALPOINTER = _descriptor.Descriptor(
  name='LocalPointer',
  full_name='karps.core.LocalPointer',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='computation', full_name='karps.core.LocalPointer.computation', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='local_path', full_name='karps.core.LocalPointer.local_path', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='data_type', full_name='karps.core.LocalPointer.data_type', index=2,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=490,
  serialized_end=630,
)


_JOIN = _descriptor.Descriptor(
  name='Join',
  full_name='karps.core.Join',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='joint_type', full_name='karps.core.Join.joint_type', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _JOIN_JOINTYPE,
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=632,
  serialized_end=708,
)

_PLACEHOLDER.fields_by_name['locality'].enum_type = karps_dot_proto_dot_graph__pb2._LOCALITY
_PLACEHOLDER.fields_by_name['data_type'].message_type = karps_dot_proto_dot_types__pb2._SQLTYPE
_SHUFFLE.fields_by_name['agg_op'].message_type = karps_dot_proto_dot_structured__transform__pb2._AGGREGATION
_STRUCTUREDTRANSFORM.fields_by_name['col_op'].message_type = karps_dot_proto_dot_structured__transform__pb2._COLUMN
_LOCALSTRUCTUREDTRANSFORM.fields_by_name['col_op'].message_type = karps_dot_proto_dot_structured__transform__pb2._COLUMN
_STRUCTUREDREDUCE.fields_by_name['agg_op'].message_type = karps_dot_proto_dot_structured__transform__pb2._AGGREGATION
_LOCALPOINTER.fields_by_name['computation'].message_type = karps_dot_proto_dot_computation__pb2._COMPUTATIONID
_LOCALPOINTER.fields_by_name['local_path'].message_type = karps_dot_proto_dot_graph__pb2._PATH
_LOCALPOINTER.fields_by_name['data_type'].message_type = karps_dot_proto_dot_types__pb2._SQLTYPE
_JOIN.fields_by_name['joint_type'].enum_type = _JOIN_JOINTYPE
_JOIN_JOINTYPE.containing_type = _JOIN
DESCRIPTOR.message_types_by_name['Placeholder'] = _PLACEHOLDER
DESCRIPTOR.message_types_by_name['Shuffle'] = _SHUFFLE
DESCRIPTOR.message_types_by_name['StructuredTransform'] = _STRUCTUREDTRANSFORM
DESCRIPTOR.message_types_by_name['LocalStructuredTransform'] = _LOCALSTRUCTUREDTRANSFORM
DESCRIPTOR.message_types_by_name['StructuredReduce'] = _STRUCTUREDREDUCE
DESCRIPTOR.message_types_by_name['LocalPointer'] = _LOCALPOINTER
DESCRIPTOR.message_types_by_name['Join'] = _JOIN
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Placeholder = _reflection.GeneratedProtocolMessageType('Placeholder', (_message.Message,), dict(
  DESCRIPTOR = _PLACEHOLDER,
  __module__ = 'karps.proto.std_pb2'
  # @@protoc_insertion_point(class_scope:karps.core.Placeholder)
  ))
_sym_db.RegisterMessage(Placeholder)

Shuffle = _reflection.GeneratedProtocolMessageType('Shuffle', (_message.Message,), dict(
  DESCRIPTOR = _SHUFFLE,
  __module__ = 'karps.proto.std_pb2'
  # @@protoc_insertion_point(class_scope:karps.core.Shuffle)
  ))
_sym_db.RegisterMessage(Shuffle)

StructuredTransform = _reflection.GeneratedProtocolMessageType('StructuredTransform', (_message.Message,), dict(
  DESCRIPTOR = _STRUCTUREDTRANSFORM,
  __module__ = 'karps.proto.std_pb2'
  # @@protoc_insertion_point(class_scope:karps.core.StructuredTransform)
  ))
_sym_db.RegisterMessage(StructuredTransform)

LocalStructuredTransform = _reflection.GeneratedProtocolMessageType('LocalStructuredTransform', (_message.Message,), dict(
  DESCRIPTOR = _LOCALSTRUCTUREDTRANSFORM,
  __module__ = 'karps.proto.std_pb2'
  # @@protoc_insertion_point(class_scope:karps.core.LocalStructuredTransform)
  ))
_sym_db.RegisterMessage(LocalStructuredTransform)

StructuredReduce = _reflection.GeneratedProtocolMessageType('StructuredReduce', (_message.Message,), dict(
  DESCRIPTOR = _STRUCTUREDREDUCE,
  __module__ = 'karps.proto.std_pb2'
  # @@protoc_insertion_point(class_scope:karps.core.StructuredReduce)
  ))
_sym_db.RegisterMessage(StructuredReduce)

LocalPointer = _reflection.GeneratedProtocolMessageType('LocalPointer', (_message.Message,), dict(
  DESCRIPTOR = _LOCALPOINTER,
  __module__ = 'karps.proto.std_pb2'
  # @@protoc_insertion_point(class_scope:karps.core.LocalPointer)
  ))
_sym_db.RegisterMessage(LocalPointer)

Join = _reflection.GeneratedProtocolMessageType('Join', (_message.Message,), dict(
  DESCRIPTOR = _JOIN,
  __module__ = 'karps.proto.std_pb2'
  # @@protoc_insertion_point(class_scope:karps.core.Join)
  ))
_sym_db.RegisterMessage(Join)


try:
  # THESE ELEMENTS WILL BE DEPRECATED.
  # Please use the generated *_pb2_grpc.py files instead.
  import grpc
  from grpc.beta import implementations as beta_implementations
  from grpc.beta import interfaces as beta_interfaces
  from grpc.framework.common import cardinality
  from grpc.framework.interfaces.face import utilities as face_utilities
except ImportError:
  pass
# @@protoc_insertion_point(module_scope)
