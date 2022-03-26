// source: chesse_backend_api/v1alpha1/positions.proto
/**
 * @fileoverview
 * @enhanceable
 * @suppress {missingRequire} reports error on implicit type usages.
 * @suppress {messageConventions} JS Compiler reports an error if a variable or
 *     field starts with 'MSG_' and isn't a translatable message.
 * @public
 */
// GENERATED CODE -- DO NOT EDIT!
/* eslint-disable */
// @ts-nocheck

var jspb = require('google-protobuf');
var goog = jspb;
var global = Function('return this')();

goog.exportSymbol('proto.chesse_backend_api.v1alpha1.Position', null, global);
goog.exportSymbol('proto.chesse_backend_api.v1alpha1.PositionRatingStats', null, global);
goog.exportSymbol('proto.chesse_backend_api.v1alpha1.PositionResultStats', null, global);
goog.exportSymbol('proto.chesse_backend_api.v1alpha1.PositionStats', null, global);
goog.exportSymbol('proto.chesse_backend_api.v1alpha1.SimilarPosition', null, global);
/**
 * Generated by JsPbCodeGenerator.
 * @param {Array=} opt_data Optional initial data array, typically from a
 * server response, or constructed directly in Javascript. The array is used
 * in place and becomes part of the constructed object. It is not cloned.
 * If no data is provided, the constructed object will be empty, but still
 * valid.
 * @extends {jspb.Message}
 * @constructor
 */
proto.chesse_backend_api.v1alpha1.Position = function(opt_data) {
  jspb.Message.initialize(this, opt_data, 0, -1, null, null);
};
goog.inherits(proto.chesse_backend_api.v1alpha1.Position, jspb.Message);
if (goog.DEBUG && !COMPILED) {
  /**
   * @public
   * @override
   */
  proto.chesse_backend_api.v1alpha1.Position.displayName = 'proto.chesse_backend_api.v1alpha1.Position';
}
/**
 * Generated by JsPbCodeGenerator.
 * @param {Array=} opt_data Optional initial data array, typically from a
 * server response, or constructed directly in Javascript. The array is used
 * in place and becomes part of the constructed object. It is not cloned.
 * If no data is provided, the constructed object will be empty, but still
 * valid.
 * @extends {jspb.Message}
 * @constructor
 */
proto.chesse_backend_api.v1alpha1.PositionRatingStats = function(opt_data) {
  jspb.Message.initialize(this, opt_data, 0, -1, null, null);
};
goog.inherits(proto.chesse_backend_api.v1alpha1.PositionRatingStats, jspb.Message);
if (goog.DEBUG && !COMPILED) {
  /**
   * @public
   * @override
   */
  proto.chesse_backend_api.v1alpha1.PositionRatingStats.displayName = 'proto.chesse_backend_api.v1alpha1.PositionRatingStats';
}
/**
 * Generated by JsPbCodeGenerator.
 * @param {Array=} opt_data Optional initial data array, typically from a
 * server response, or constructed directly in Javascript. The array is used
 * in place and becomes part of the constructed object. It is not cloned.
 * If no data is provided, the constructed object will be empty, but still
 * valid.
 * @extends {jspb.Message}
 * @constructor
 */
proto.chesse_backend_api.v1alpha1.PositionResultStats = function(opt_data) {
  jspb.Message.initialize(this, opt_data, 0, -1, null, null);
};
goog.inherits(proto.chesse_backend_api.v1alpha1.PositionResultStats, jspb.Message);
if (goog.DEBUG && !COMPILED) {
  /**
   * @public
   * @override
   */
  proto.chesse_backend_api.v1alpha1.PositionResultStats.displayName = 'proto.chesse_backend_api.v1alpha1.PositionResultStats';
}
/**
 * Generated by JsPbCodeGenerator.
 * @param {Array=} opt_data Optional initial data array, typically from a
 * server response, or constructed directly in Javascript. The array is used
 * in place and becomes part of the constructed object. It is not cloned.
 * If no data is provided, the constructed object will be empty, but still
 * valid.
 * @extends {jspb.Message}
 * @constructor
 */
proto.chesse_backend_api.v1alpha1.PositionStats = function(opt_data) {
  jspb.Message.initialize(this, opt_data, 0, -1, null, null);
};
goog.inherits(proto.chesse_backend_api.v1alpha1.PositionStats, jspb.Message);
if (goog.DEBUG && !COMPILED) {
  /**
   * @public
   * @override
   */
  proto.chesse_backend_api.v1alpha1.PositionStats.displayName = 'proto.chesse_backend_api.v1alpha1.PositionStats';
}
/**
 * Generated by JsPbCodeGenerator.
 * @param {Array=} opt_data Optional initial data array, typically from a
 * server response, or constructed directly in Javascript. The array is used
 * in place and becomes part of the constructed object. It is not cloned.
 * If no data is provided, the constructed object will be empty, but still
 * valid.
 * @extends {jspb.Message}
 * @constructor
 */
proto.chesse_backend_api.v1alpha1.SimilarPosition = function(opt_data) {
  jspb.Message.initialize(this, opt_data, 0, -1, null, null);
};
goog.inherits(proto.chesse_backend_api.v1alpha1.SimilarPosition, jspb.Message);
if (goog.DEBUG && !COMPILED) {
  /**
   * @public
   * @override
   */
  proto.chesse_backend_api.v1alpha1.SimilarPosition.displayName = 'proto.chesse_backend_api.v1alpha1.SimilarPosition';
}



if (jspb.Message.GENERATE_TO_OBJECT) {
/**
 * Creates an object representation of this proto.
 * Field names that are reserved in JavaScript and will be renamed to pb_name.
 * Optional fields that are not set will be set to undefined.
 * To access a reserved field use, foo.pb_<name>, eg, foo.pb_default.
 * For the list of reserved names please see:
 *     net/proto2/compiler/js/internal/generator.cc#kKeyword.
 * @param {boolean=} opt_includeInstance Deprecated. whether to include the
 *     JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @return {!Object}
 */
proto.chesse_backend_api.v1alpha1.Position.prototype.toObject = function(opt_includeInstance) {
  return proto.chesse_backend_api.v1alpha1.Position.toObject(opt_includeInstance, this);
};


/**
 * Static version of the {@see toObject} method.
 * @param {boolean|undefined} includeInstance Deprecated. Whether to include
 *     the JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @param {!proto.chesse_backend_api.v1alpha1.Position} msg The msg instance to transform.
 * @return {!Object}
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.chesse_backend_api.v1alpha1.Position.toObject = function(includeInstance, msg) {
  var f, obj = {
    fen: jspb.Message.getFieldWithDefault(msg, 1, "")
  };

  if (includeInstance) {
    obj.$jspbMessageInstance = msg;
  }
  return obj;
};
}


/**
 * Deserializes binary data (in protobuf wire format).
 * @param {jspb.ByteSource} bytes The bytes to deserialize.
 * @return {!proto.chesse_backend_api.v1alpha1.Position}
 */
proto.chesse_backend_api.v1alpha1.Position.deserializeBinary = function(bytes) {
  var reader = new jspb.BinaryReader(bytes);
  var msg = new proto.chesse_backend_api.v1alpha1.Position;
  return proto.chesse_backend_api.v1alpha1.Position.deserializeBinaryFromReader(msg, reader);
};


/**
 * Deserializes binary data (in protobuf wire format) from the
 * given reader into the given message object.
 * @param {!proto.chesse_backend_api.v1alpha1.Position} msg The message object to deserialize into.
 * @param {!jspb.BinaryReader} reader The BinaryReader to use.
 * @return {!proto.chesse_backend_api.v1alpha1.Position}
 */
proto.chesse_backend_api.v1alpha1.Position.deserializeBinaryFromReader = function(msg, reader) {
  while (reader.nextField()) {
    if (reader.isEndGroup()) {
      break;
    }
    var field = reader.getFieldNumber();
    switch (field) {
    case 1:
      var value = /** @type {string} */ (reader.readString());
      msg.setFen(value);
      break;
    default:
      reader.skipField();
      break;
    }
  }
  return msg;
};


/**
 * Serializes the message to binary data (in protobuf wire format).
 * @return {!Uint8Array}
 */
proto.chesse_backend_api.v1alpha1.Position.prototype.serializeBinary = function() {
  var writer = new jspb.BinaryWriter();
  proto.chesse_backend_api.v1alpha1.Position.serializeBinaryToWriter(this, writer);
  return writer.getResultBuffer();
};


/**
 * Serializes the given message to binary data (in protobuf wire
 * format), writing to the given BinaryWriter.
 * @param {!proto.chesse_backend_api.v1alpha1.Position} message
 * @param {!jspb.BinaryWriter} writer
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.chesse_backend_api.v1alpha1.Position.serializeBinaryToWriter = function(message, writer) {
  var f = undefined;
  f = message.getFen();
  if (f.length > 0) {
    writer.writeString(
      1,
      f
    );
  }
};


/**
 * optional string fen = 1;
 * @return {string}
 */
proto.chesse_backend_api.v1alpha1.Position.prototype.getFen = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 1, ""));
};


/**
 * @param {string} value
 * @return {!proto.chesse_backend_api.v1alpha1.Position} returns this
 */
proto.chesse_backend_api.v1alpha1.Position.prototype.setFen = function(value) {
  return jspb.Message.setProto3StringField(this, 1, value);
};





if (jspb.Message.GENERATE_TO_OBJECT) {
/**
 * Creates an object representation of this proto.
 * Field names that are reserved in JavaScript and will be renamed to pb_name.
 * Optional fields that are not set will be set to undefined.
 * To access a reserved field use, foo.pb_<name>, eg, foo.pb_default.
 * For the list of reserved names please see:
 *     net/proto2/compiler/js/internal/generator.cc#kKeyword.
 * @param {boolean=} opt_includeInstance Deprecated. whether to include the
 *     JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @return {!Object}
 */
proto.chesse_backend_api.v1alpha1.PositionRatingStats.prototype.toObject = function(opt_includeInstance) {
  return proto.chesse_backend_api.v1alpha1.PositionRatingStats.toObject(opt_includeInstance, this);
};


/**
 * Static version of the {@see toObject} method.
 * @param {boolean|undefined} includeInstance Deprecated. Whether to include
 *     the JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @param {!proto.chesse_backend_api.v1alpha1.PositionRatingStats} msg The msg instance to transform.
 * @return {!Object}
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.chesse_backend_api.v1alpha1.PositionRatingStats.toObject = function(includeInstance, msg) {
  var f, obj = {
    min: jspb.Message.getFieldWithDefault(msg, 1, 0),
    avg: jspb.Message.getFieldWithDefault(msg, 2, 0),
    max: jspb.Message.getFieldWithDefault(msg, 3, 0)
  };

  if (includeInstance) {
    obj.$jspbMessageInstance = msg;
  }
  return obj;
};
}


/**
 * Deserializes binary data (in protobuf wire format).
 * @param {jspb.ByteSource} bytes The bytes to deserialize.
 * @return {!proto.chesse_backend_api.v1alpha1.PositionRatingStats}
 */
proto.chesse_backend_api.v1alpha1.PositionRatingStats.deserializeBinary = function(bytes) {
  var reader = new jspb.BinaryReader(bytes);
  var msg = new proto.chesse_backend_api.v1alpha1.PositionRatingStats;
  return proto.chesse_backend_api.v1alpha1.PositionRatingStats.deserializeBinaryFromReader(msg, reader);
};


/**
 * Deserializes binary data (in protobuf wire format) from the
 * given reader into the given message object.
 * @param {!proto.chesse_backend_api.v1alpha1.PositionRatingStats} msg The message object to deserialize into.
 * @param {!jspb.BinaryReader} reader The BinaryReader to use.
 * @return {!proto.chesse_backend_api.v1alpha1.PositionRatingStats}
 */
proto.chesse_backend_api.v1alpha1.PositionRatingStats.deserializeBinaryFromReader = function(msg, reader) {
  while (reader.nextField()) {
    if (reader.isEndGroup()) {
      break;
    }
    var field = reader.getFieldNumber();
    switch (field) {
    case 1:
      var value = /** @type {number} */ (reader.readInt32());
      msg.setMin(value);
      break;
    case 2:
      var value = /** @type {number} */ (reader.readInt32());
      msg.setAvg(value);
      break;
    case 3:
      var value = /** @type {number} */ (reader.readInt32());
      msg.setMax(value);
      break;
    default:
      reader.skipField();
      break;
    }
  }
  return msg;
};


/**
 * Serializes the message to binary data (in protobuf wire format).
 * @return {!Uint8Array}
 */
proto.chesse_backend_api.v1alpha1.PositionRatingStats.prototype.serializeBinary = function() {
  var writer = new jspb.BinaryWriter();
  proto.chesse_backend_api.v1alpha1.PositionRatingStats.serializeBinaryToWriter(this, writer);
  return writer.getResultBuffer();
};


/**
 * Serializes the given message to binary data (in protobuf wire
 * format), writing to the given BinaryWriter.
 * @param {!proto.chesse_backend_api.v1alpha1.PositionRatingStats} message
 * @param {!jspb.BinaryWriter} writer
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.chesse_backend_api.v1alpha1.PositionRatingStats.serializeBinaryToWriter = function(message, writer) {
  var f = undefined;
  f = message.getMin();
  if (f !== 0) {
    writer.writeInt32(
      1,
      f
    );
  }
  f = message.getAvg();
  if (f !== 0) {
    writer.writeInt32(
      2,
      f
    );
  }
  f = message.getMax();
  if (f !== 0) {
    writer.writeInt32(
      3,
      f
    );
  }
};


/**
 * optional int32 min = 1;
 * @return {number}
 */
proto.chesse_backend_api.v1alpha1.PositionRatingStats.prototype.getMin = function() {
  return /** @type {number} */ (jspb.Message.getFieldWithDefault(this, 1, 0));
};


/**
 * @param {number} value
 * @return {!proto.chesse_backend_api.v1alpha1.PositionRatingStats} returns this
 */
proto.chesse_backend_api.v1alpha1.PositionRatingStats.prototype.setMin = function(value) {
  return jspb.Message.setProto3IntField(this, 1, value);
};


/**
 * optional int32 avg = 2;
 * @return {number}
 */
proto.chesse_backend_api.v1alpha1.PositionRatingStats.prototype.getAvg = function() {
  return /** @type {number} */ (jspb.Message.getFieldWithDefault(this, 2, 0));
};


/**
 * @param {number} value
 * @return {!proto.chesse_backend_api.v1alpha1.PositionRatingStats} returns this
 */
proto.chesse_backend_api.v1alpha1.PositionRatingStats.prototype.setAvg = function(value) {
  return jspb.Message.setProto3IntField(this, 2, value);
};


/**
 * optional int32 max = 3;
 * @return {number}
 */
proto.chesse_backend_api.v1alpha1.PositionRatingStats.prototype.getMax = function() {
  return /** @type {number} */ (jspb.Message.getFieldWithDefault(this, 3, 0));
};


/**
 * @param {number} value
 * @return {!proto.chesse_backend_api.v1alpha1.PositionRatingStats} returns this
 */
proto.chesse_backend_api.v1alpha1.PositionRatingStats.prototype.setMax = function(value) {
  return jspb.Message.setProto3IntField(this, 3, value);
};





if (jspb.Message.GENERATE_TO_OBJECT) {
/**
 * Creates an object representation of this proto.
 * Field names that are reserved in JavaScript and will be renamed to pb_name.
 * Optional fields that are not set will be set to undefined.
 * To access a reserved field use, foo.pb_<name>, eg, foo.pb_default.
 * For the list of reserved names please see:
 *     net/proto2/compiler/js/internal/generator.cc#kKeyword.
 * @param {boolean=} opt_includeInstance Deprecated. whether to include the
 *     JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @return {!Object}
 */
proto.chesse_backend_api.v1alpha1.PositionResultStats.prototype.toObject = function(opt_includeInstance) {
  return proto.chesse_backend_api.v1alpha1.PositionResultStats.toObject(opt_includeInstance, this);
};


/**
 * Static version of the {@see toObject} method.
 * @param {boolean|undefined} includeInstance Deprecated. Whether to include
 *     the JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @param {!proto.chesse_backend_api.v1alpha1.PositionResultStats} msg The msg instance to transform.
 * @return {!Object}
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.chesse_backend_api.v1alpha1.PositionResultStats.toObject = function(includeInstance, msg) {
  var f, obj = {
    whiteWinPct: jspb.Message.getFloatingPointFieldWithDefault(msg, 1, 0.0),
    drawPct: jspb.Message.getFloatingPointFieldWithDefault(msg, 2, 0.0),
    blackWinPct: jspb.Message.getFloatingPointFieldWithDefault(msg, 3, 0.0)
  };

  if (includeInstance) {
    obj.$jspbMessageInstance = msg;
  }
  return obj;
};
}


/**
 * Deserializes binary data (in protobuf wire format).
 * @param {jspb.ByteSource} bytes The bytes to deserialize.
 * @return {!proto.chesse_backend_api.v1alpha1.PositionResultStats}
 */
proto.chesse_backend_api.v1alpha1.PositionResultStats.deserializeBinary = function(bytes) {
  var reader = new jspb.BinaryReader(bytes);
  var msg = new proto.chesse_backend_api.v1alpha1.PositionResultStats;
  return proto.chesse_backend_api.v1alpha1.PositionResultStats.deserializeBinaryFromReader(msg, reader);
};


/**
 * Deserializes binary data (in protobuf wire format) from the
 * given reader into the given message object.
 * @param {!proto.chesse_backend_api.v1alpha1.PositionResultStats} msg The message object to deserialize into.
 * @param {!jspb.BinaryReader} reader The BinaryReader to use.
 * @return {!proto.chesse_backend_api.v1alpha1.PositionResultStats}
 */
proto.chesse_backend_api.v1alpha1.PositionResultStats.deserializeBinaryFromReader = function(msg, reader) {
  while (reader.nextField()) {
    if (reader.isEndGroup()) {
      break;
    }
    var field = reader.getFieldNumber();
    switch (field) {
    case 1:
      var value = /** @type {number} */ (reader.readFloat());
      msg.setWhiteWinPct(value);
      break;
    case 2:
      var value = /** @type {number} */ (reader.readFloat());
      msg.setDrawPct(value);
      break;
    case 3:
      var value = /** @type {number} */ (reader.readFloat());
      msg.setBlackWinPct(value);
      break;
    default:
      reader.skipField();
      break;
    }
  }
  return msg;
};


/**
 * Serializes the message to binary data (in protobuf wire format).
 * @return {!Uint8Array}
 */
proto.chesse_backend_api.v1alpha1.PositionResultStats.prototype.serializeBinary = function() {
  var writer = new jspb.BinaryWriter();
  proto.chesse_backend_api.v1alpha1.PositionResultStats.serializeBinaryToWriter(this, writer);
  return writer.getResultBuffer();
};


/**
 * Serializes the given message to binary data (in protobuf wire
 * format), writing to the given BinaryWriter.
 * @param {!proto.chesse_backend_api.v1alpha1.PositionResultStats} message
 * @param {!jspb.BinaryWriter} writer
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.chesse_backend_api.v1alpha1.PositionResultStats.serializeBinaryToWriter = function(message, writer) {
  var f = undefined;
  f = message.getWhiteWinPct();
  if (f !== 0.0) {
    writer.writeFloat(
      1,
      f
    );
  }
  f = message.getDrawPct();
  if (f !== 0.0) {
    writer.writeFloat(
      2,
      f
    );
  }
  f = message.getBlackWinPct();
  if (f !== 0.0) {
    writer.writeFloat(
      3,
      f
    );
  }
};


/**
 * optional float white_win_pct = 1;
 * @return {number}
 */
proto.chesse_backend_api.v1alpha1.PositionResultStats.prototype.getWhiteWinPct = function() {
  return /** @type {number} */ (jspb.Message.getFloatingPointFieldWithDefault(this, 1, 0.0));
};


/**
 * @param {number} value
 * @return {!proto.chesse_backend_api.v1alpha1.PositionResultStats} returns this
 */
proto.chesse_backend_api.v1alpha1.PositionResultStats.prototype.setWhiteWinPct = function(value) {
  return jspb.Message.setProto3FloatField(this, 1, value);
};


/**
 * optional float draw_pct = 2;
 * @return {number}
 */
proto.chesse_backend_api.v1alpha1.PositionResultStats.prototype.getDrawPct = function() {
  return /** @type {number} */ (jspb.Message.getFloatingPointFieldWithDefault(this, 2, 0.0));
};


/**
 * @param {number} value
 * @return {!proto.chesse_backend_api.v1alpha1.PositionResultStats} returns this
 */
proto.chesse_backend_api.v1alpha1.PositionResultStats.prototype.setDrawPct = function(value) {
  return jspb.Message.setProto3FloatField(this, 2, value);
};


/**
 * optional float black_win_pct = 3;
 * @return {number}
 */
proto.chesse_backend_api.v1alpha1.PositionResultStats.prototype.getBlackWinPct = function() {
  return /** @type {number} */ (jspb.Message.getFloatingPointFieldWithDefault(this, 3, 0.0));
};


/**
 * @param {number} value
 * @return {!proto.chesse_backend_api.v1alpha1.PositionResultStats} returns this
 */
proto.chesse_backend_api.v1alpha1.PositionResultStats.prototype.setBlackWinPct = function(value) {
  return jspb.Message.setProto3FloatField(this, 3, value);
};





if (jspb.Message.GENERATE_TO_OBJECT) {
/**
 * Creates an object representation of this proto.
 * Field names that are reserved in JavaScript and will be renamed to pb_name.
 * Optional fields that are not set will be set to undefined.
 * To access a reserved field use, foo.pb_<name>, eg, foo.pb_default.
 * For the list of reserved names please see:
 *     net/proto2/compiler/js/internal/generator.cc#kKeyword.
 * @param {boolean=} opt_includeInstance Deprecated. whether to include the
 *     JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @return {!Object}
 */
proto.chesse_backend_api.v1alpha1.PositionStats.prototype.toObject = function(opt_includeInstance) {
  return proto.chesse_backend_api.v1alpha1.PositionStats.toObject(opt_includeInstance, this);
};


/**
 * Static version of the {@see toObject} method.
 * @param {boolean|undefined} includeInstance Deprecated. Whether to include
 *     the JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @param {!proto.chesse_backend_api.v1alpha1.PositionStats} msg The msg instance to transform.
 * @return {!Object}
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.chesse_backend_api.v1alpha1.PositionStats.toObject = function(includeInstance, msg) {
  var f, obj = {
    nrGames: jspb.Message.getFieldWithDefault(msg, 1, 0),
    ratingStats: (f = msg.getRatingStats()) && proto.chesse_backend_api.v1alpha1.PositionRatingStats.toObject(includeInstance, f),
    resultStats: (f = msg.getResultStats()) && proto.chesse_backend_api.v1alpha1.PositionResultStats.toObject(includeInstance, f)
  };

  if (includeInstance) {
    obj.$jspbMessageInstance = msg;
  }
  return obj;
};
}


/**
 * Deserializes binary data (in protobuf wire format).
 * @param {jspb.ByteSource} bytes The bytes to deserialize.
 * @return {!proto.chesse_backend_api.v1alpha1.PositionStats}
 */
proto.chesse_backend_api.v1alpha1.PositionStats.deserializeBinary = function(bytes) {
  var reader = new jspb.BinaryReader(bytes);
  var msg = new proto.chesse_backend_api.v1alpha1.PositionStats;
  return proto.chesse_backend_api.v1alpha1.PositionStats.deserializeBinaryFromReader(msg, reader);
};


/**
 * Deserializes binary data (in protobuf wire format) from the
 * given reader into the given message object.
 * @param {!proto.chesse_backend_api.v1alpha1.PositionStats} msg The message object to deserialize into.
 * @param {!jspb.BinaryReader} reader The BinaryReader to use.
 * @return {!proto.chesse_backend_api.v1alpha1.PositionStats}
 */
proto.chesse_backend_api.v1alpha1.PositionStats.deserializeBinaryFromReader = function(msg, reader) {
  while (reader.nextField()) {
    if (reader.isEndGroup()) {
      break;
    }
    var field = reader.getFieldNumber();
    switch (field) {
    case 1:
      var value = /** @type {number} */ (reader.readInt32());
      msg.setNrGames(value);
      break;
    case 2:
      var value = new proto.chesse_backend_api.v1alpha1.PositionRatingStats;
      reader.readMessage(value,proto.chesse_backend_api.v1alpha1.PositionRatingStats.deserializeBinaryFromReader);
      msg.setRatingStats(value);
      break;
    case 3:
      var value = new proto.chesse_backend_api.v1alpha1.PositionResultStats;
      reader.readMessage(value,proto.chesse_backend_api.v1alpha1.PositionResultStats.deserializeBinaryFromReader);
      msg.setResultStats(value);
      break;
    default:
      reader.skipField();
      break;
    }
  }
  return msg;
};


/**
 * Serializes the message to binary data (in protobuf wire format).
 * @return {!Uint8Array}
 */
proto.chesse_backend_api.v1alpha1.PositionStats.prototype.serializeBinary = function() {
  var writer = new jspb.BinaryWriter();
  proto.chesse_backend_api.v1alpha1.PositionStats.serializeBinaryToWriter(this, writer);
  return writer.getResultBuffer();
};


/**
 * Serializes the given message to binary data (in protobuf wire
 * format), writing to the given BinaryWriter.
 * @param {!proto.chesse_backend_api.v1alpha1.PositionStats} message
 * @param {!jspb.BinaryWriter} writer
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.chesse_backend_api.v1alpha1.PositionStats.serializeBinaryToWriter = function(message, writer) {
  var f = undefined;
  f = message.getNrGames();
  if (f !== 0) {
    writer.writeInt32(
      1,
      f
    );
  }
  f = message.getRatingStats();
  if (f != null) {
    writer.writeMessage(
      2,
      f,
      proto.chesse_backend_api.v1alpha1.PositionRatingStats.serializeBinaryToWriter
    );
  }
  f = message.getResultStats();
  if (f != null) {
    writer.writeMessage(
      3,
      f,
      proto.chesse_backend_api.v1alpha1.PositionResultStats.serializeBinaryToWriter
    );
  }
};


/**
 * optional int32 nr_games = 1;
 * @return {number}
 */
proto.chesse_backend_api.v1alpha1.PositionStats.prototype.getNrGames = function() {
  return /** @type {number} */ (jspb.Message.getFieldWithDefault(this, 1, 0));
};


/**
 * @param {number} value
 * @return {!proto.chesse_backend_api.v1alpha1.PositionStats} returns this
 */
proto.chesse_backend_api.v1alpha1.PositionStats.prototype.setNrGames = function(value) {
  return jspb.Message.setProto3IntField(this, 1, value);
};


/**
 * optional PositionRatingStats rating_stats = 2;
 * @return {?proto.chesse_backend_api.v1alpha1.PositionRatingStats}
 */
proto.chesse_backend_api.v1alpha1.PositionStats.prototype.getRatingStats = function() {
  return /** @type{?proto.chesse_backend_api.v1alpha1.PositionRatingStats} */ (
    jspb.Message.getWrapperField(this, proto.chesse_backend_api.v1alpha1.PositionRatingStats, 2));
};


/**
 * @param {?proto.chesse_backend_api.v1alpha1.PositionRatingStats|undefined} value
 * @return {!proto.chesse_backend_api.v1alpha1.PositionStats} returns this
*/
proto.chesse_backend_api.v1alpha1.PositionStats.prototype.setRatingStats = function(value) {
  return jspb.Message.setWrapperField(this, 2, value);
};


/**
 * Clears the message field making it undefined.
 * @return {!proto.chesse_backend_api.v1alpha1.PositionStats} returns this
 */
proto.chesse_backend_api.v1alpha1.PositionStats.prototype.clearRatingStats = function() {
  return this.setRatingStats(undefined);
};


/**
 * Returns whether this field is set.
 * @return {boolean}
 */
proto.chesse_backend_api.v1alpha1.PositionStats.prototype.hasRatingStats = function() {
  return jspb.Message.getField(this, 2) != null;
};


/**
 * optional PositionResultStats result_stats = 3;
 * @return {?proto.chesse_backend_api.v1alpha1.PositionResultStats}
 */
proto.chesse_backend_api.v1alpha1.PositionStats.prototype.getResultStats = function() {
  return /** @type{?proto.chesse_backend_api.v1alpha1.PositionResultStats} */ (
    jspb.Message.getWrapperField(this, proto.chesse_backend_api.v1alpha1.PositionResultStats, 3));
};


/**
 * @param {?proto.chesse_backend_api.v1alpha1.PositionResultStats|undefined} value
 * @return {!proto.chesse_backend_api.v1alpha1.PositionStats} returns this
*/
proto.chesse_backend_api.v1alpha1.PositionStats.prototype.setResultStats = function(value) {
  return jspb.Message.setWrapperField(this, 3, value);
};


/**
 * Clears the message field making it undefined.
 * @return {!proto.chesse_backend_api.v1alpha1.PositionStats} returns this
 */
proto.chesse_backend_api.v1alpha1.PositionStats.prototype.clearResultStats = function() {
  return this.setResultStats(undefined);
};


/**
 * Returns whether this field is set.
 * @return {boolean}
 */
proto.chesse_backend_api.v1alpha1.PositionStats.prototype.hasResultStats = function() {
  return jspb.Message.getField(this, 3) != null;
};





if (jspb.Message.GENERATE_TO_OBJECT) {
/**
 * Creates an object representation of this proto.
 * Field names that are reserved in JavaScript and will be renamed to pb_name.
 * Optional fields that are not set will be set to undefined.
 * To access a reserved field use, foo.pb_<name>, eg, foo.pb_default.
 * For the list of reserved names please see:
 *     net/proto2/compiler/js/internal/generator.cc#kKeyword.
 * @param {boolean=} opt_includeInstance Deprecated. whether to include the
 *     JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @return {!Object}
 */
proto.chesse_backend_api.v1alpha1.SimilarPosition.prototype.toObject = function(opt_includeInstance) {
  return proto.chesse_backend_api.v1alpha1.SimilarPosition.toObject(opt_includeInstance, this);
};


/**
 * Static version of the {@see toObject} method.
 * @param {boolean|undefined} includeInstance Deprecated. Whether to include
 *     the JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @param {!proto.chesse_backend_api.v1alpha1.SimilarPosition} msg The msg instance to transform.
 * @return {!Object}
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.chesse_backend_api.v1alpha1.SimilarPosition.toObject = function(includeInstance, msg) {
  var f, obj = {
    position: (f = msg.getPosition()) && proto.chesse_backend_api.v1alpha1.Position.toObject(includeInstance, f),
    similarityScore: jspb.Message.getFieldWithDefault(msg, 2, 0),
    positionStats: (f = msg.getPositionStats()) && proto.chesse_backend_api.v1alpha1.PositionStats.toObject(includeInstance, f)
  };

  if (includeInstance) {
    obj.$jspbMessageInstance = msg;
  }
  return obj;
};
}


/**
 * Deserializes binary data (in protobuf wire format).
 * @param {jspb.ByteSource} bytes The bytes to deserialize.
 * @return {!proto.chesse_backend_api.v1alpha1.SimilarPosition}
 */
proto.chesse_backend_api.v1alpha1.SimilarPosition.deserializeBinary = function(bytes) {
  var reader = new jspb.BinaryReader(bytes);
  var msg = new proto.chesse_backend_api.v1alpha1.SimilarPosition;
  return proto.chesse_backend_api.v1alpha1.SimilarPosition.deserializeBinaryFromReader(msg, reader);
};


/**
 * Deserializes binary data (in protobuf wire format) from the
 * given reader into the given message object.
 * @param {!proto.chesse_backend_api.v1alpha1.SimilarPosition} msg The message object to deserialize into.
 * @param {!jspb.BinaryReader} reader The BinaryReader to use.
 * @return {!proto.chesse_backend_api.v1alpha1.SimilarPosition}
 */
proto.chesse_backend_api.v1alpha1.SimilarPosition.deserializeBinaryFromReader = function(msg, reader) {
  while (reader.nextField()) {
    if (reader.isEndGroup()) {
      break;
    }
    var field = reader.getFieldNumber();
    switch (field) {
    case 1:
      var value = new proto.chesse_backend_api.v1alpha1.Position;
      reader.readMessage(value,proto.chesse_backend_api.v1alpha1.Position.deserializeBinaryFromReader);
      msg.setPosition(value);
      break;
    case 2:
      var value = /** @type {number} */ (reader.readInt32());
      msg.setSimilarityScore(value);
      break;
    case 3:
      var value = new proto.chesse_backend_api.v1alpha1.PositionStats;
      reader.readMessage(value,proto.chesse_backend_api.v1alpha1.PositionStats.deserializeBinaryFromReader);
      msg.setPositionStats(value);
      break;
    default:
      reader.skipField();
      break;
    }
  }
  return msg;
};


/**
 * Serializes the message to binary data (in protobuf wire format).
 * @return {!Uint8Array}
 */
proto.chesse_backend_api.v1alpha1.SimilarPosition.prototype.serializeBinary = function() {
  var writer = new jspb.BinaryWriter();
  proto.chesse_backend_api.v1alpha1.SimilarPosition.serializeBinaryToWriter(this, writer);
  return writer.getResultBuffer();
};


/**
 * Serializes the given message to binary data (in protobuf wire
 * format), writing to the given BinaryWriter.
 * @param {!proto.chesse_backend_api.v1alpha1.SimilarPosition} message
 * @param {!jspb.BinaryWriter} writer
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.chesse_backend_api.v1alpha1.SimilarPosition.serializeBinaryToWriter = function(message, writer) {
  var f = undefined;
  f = message.getPosition();
  if (f != null) {
    writer.writeMessage(
      1,
      f,
      proto.chesse_backend_api.v1alpha1.Position.serializeBinaryToWriter
    );
  }
  f = message.getSimilarityScore();
  if (f !== 0) {
    writer.writeInt32(
      2,
      f
    );
  }
  f = message.getPositionStats();
  if (f != null) {
    writer.writeMessage(
      3,
      f,
      proto.chesse_backend_api.v1alpha1.PositionStats.serializeBinaryToWriter
    );
  }
};


/**
 * optional Position position = 1;
 * @return {?proto.chesse_backend_api.v1alpha1.Position}
 */
proto.chesse_backend_api.v1alpha1.SimilarPosition.prototype.getPosition = function() {
  return /** @type{?proto.chesse_backend_api.v1alpha1.Position} */ (
    jspb.Message.getWrapperField(this, proto.chesse_backend_api.v1alpha1.Position, 1));
};


/**
 * @param {?proto.chesse_backend_api.v1alpha1.Position|undefined} value
 * @return {!proto.chesse_backend_api.v1alpha1.SimilarPosition} returns this
*/
proto.chesse_backend_api.v1alpha1.SimilarPosition.prototype.setPosition = function(value) {
  return jspb.Message.setWrapperField(this, 1, value);
};


/**
 * Clears the message field making it undefined.
 * @return {!proto.chesse_backend_api.v1alpha1.SimilarPosition} returns this
 */
proto.chesse_backend_api.v1alpha1.SimilarPosition.prototype.clearPosition = function() {
  return this.setPosition(undefined);
};


/**
 * Returns whether this field is set.
 * @return {boolean}
 */
proto.chesse_backend_api.v1alpha1.SimilarPosition.prototype.hasPosition = function() {
  return jspb.Message.getField(this, 1) != null;
};


/**
 * optional int32 similarity_score = 2;
 * @return {number}
 */
proto.chesse_backend_api.v1alpha1.SimilarPosition.prototype.getSimilarityScore = function() {
  return /** @type {number} */ (jspb.Message.getFieldWithDefault(this, 2, 0));
};


/**
 * @param {number} value
 * @return {!proto.chesse_backend_api.v1alpha1.SimilarPosition} returns this
 */
proto.chesse_backend_api.v1alpha1.SimilarPosition.prototype.setSimilarityScore = function(value) {
  return jspb.Message.setProto3IntField(this, 2, value);
};


/**
 * optional PositionStats position_stats = 3;
 * @return {?proto.chesse_backend_api.v1alpha1.PositionStats}
 */
proto.chesse_backend_api.v1alpha1.SimilarPosition.prototype.getPositionStats = function() {
  return /** @type{?proto.chesse_backend_api.v1alpha1.PositionStats} */ (
    jspb.Message.getWrapperField(this, proto.chesse_backend_api.v1alpha1.PositionStats, 3));
};


/**
 * @param {?proto.chesse_backend_api.v1alpha1.PositionStats|undefined} value
 * @return {!proto.chesse_backend_api.v1alpha1.SimilarPosition} returns this
*/
proto.chesse_backend_api.v1alpha1.SimilarPosition.prototype.setPositionStats = function(value) {
  return jspb.Message.setWrapperField(this, 3, value);
};


/**
 * Clears the message field making it undefined.
 * @return {!proto.chesse_backend_api.v1alpha1.SimilarPosition} returns this
 */
proto.chesse_backend_api.v1alpha1.SimilarPosition.prototype.clearPositionStats = function() {
  return this.setPositionStats(undefined);
};


/**
 * Returns whether this field is set.
 * @return {boolean}
 */
proto.chesse_backend_api.v1alpha1.SimilarPosition.prototype.hasPositionStats = function() {
  return jspb.Message.getField(this, 3) != null;
};


goog.object.extend(exports, proto.chesse_backend_api.v1alpha1);