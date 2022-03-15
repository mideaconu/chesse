// source: duchess_backend_api/v1alpha1/games.proto
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

goog.provide('proto.duchess_backend_api.v1alpha1.Game');

goog.require('jspb.BinaryReader');
goog.require('jspb.BinaryWriter');
goog.require('jspb.Message');
goog.require('proto.duchess_backend_api.v1alpha1.Position');

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
proto.duchess_backend_api.v1alpha1.Game = function(opt_data) {
  jspb.Message.initialize(this, opt_data, 0, -1, null, null);
};
goog.inherits(proto.duchess_backend_api.v1alpha1.Game, jspb.Message);
if (goog.DEBUG && !COMPILED) {
  /**
   * @public
   * @override
   */
  proto.duchess_backend_api.v1alpha1.Game.displayName = 'proto.duchess_backend_api.v1alpha1.Game';
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
proto.duchess_backend_api.v1alpha1.Game.prototype.toObject = function(opt_includeInstance) {
  return proto.duchess_backend_api.v1alpha1.Game.toObject(opt_includeInstance, this);
};


/**
 * Static version of the {@see toObject} method.
 * @param {boolean|undefined} includeInstance Deprecated. Whether to include
 *     the JSPB instance for transitional soy proto support:
 *     http://goto/soy-param-migration
 * @param {!proto.duchess_backend_api.v1alpha1.Game} msg The msg instance to transform.
 * @return {!Object}
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.duchess_backend_api.v1alpha1.Game.toObject = function(includeInstance, msg) {
  var f, obj = {
    id: jspb.Message.getFieldWithDefault(msg, 1, ""),
    position: (f = msg.getPosition()) && proto.duchess_backend_api.v1alpha1.Position.toObject(includeInstance, f)
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
 * @return {!proto.duchess_backend_api.v1alpha1.Game}
 */
proto.duchess_backend_api.v1alpha1.Game.deserializeBinary = function(bytes) {
  var reader = new jspb.BinaryReader(bytes);
  var msg = new proto.duchess_backend_api.v1alpha1.Game;
  return proto.duchess_backend_api.v1alpha1.Game.deserializeBinaryFromReader(msg, reader);
};


/**
 * Deserializes binary data (in protobuf wire format) from the
 * given reader into the given message object.
 * @param {!proto.duchess_backend_api.v1alpha1.Game} msg The message object to deserialize into.
 * @param {!jspb.BinaryReader} reader The BinaryReader to use.
 * @return {!proto.duchess_backend_api.v1alpha1.Game}
 */
proto.duchess_backend_api.v1alpha1.Game.deserializeBinaryFromReader = function(msg, reader) {
  while (reader.nextField()) {
    if (reader.isEndGroup()) {
      break;
    }
    var field = reader.getFieldNumber();
    switch (field) {
    case 1:
      var value = /** @type {string} */ (reader.readString());
      msg.setId(value);
      break;
    case 2:
      var value = new proto.duchess_backend_api.v1alpha1.Position;
      reader.readMessage(value,proto.duchess_backend_api.v1alpha1.Position.deserializeBinaryFromReader);
      msg.setPosition(value);
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
proto.duchess_backend_api.v1alpha1.Game.prototype.serializeBinary = function() {
  var writer = new jspb.BinaryWriter();
  proto.duchess_backend_api.v1alpha1.Game.serializeBinaryToWriter(this, writer);
  return writer.getResultBuffer();
};


/**
 * Serializes the given message to binary data (in protobuf wire
 * format), writing to the given BinaryWriter.
 * @param {!proto.duchess_backend_api.v1alpha1.Game} message
 * @param {!jspb.BinaryWriter} writer
 * @suppress {unusedLocalVariables} f is only used for nested messages
 */
proto.duchess_backend_api.v1alpha1.Game.serializeBinaryToWriter = function(message, writer) {
  var f = undefined;
  f = message.getId();
  if (f.length > 0) {
    writer.writeString(
      1,
      f
    );
  }
  f = message.getPosition();
  if (f != null) {
    writer.writeMessage(
      2,
      f,
      proto.duchess_backend_api.v1alpha1.Position.serializeBinaryToWriter
    );
  }
};


/**
 * optional string id = 1;
 * @return {string}
 */
proto.duchess_backend_api.v1alpha1.Game.prototype.getId = function() {
  return /** @type {string} */ (jspb.Message.getFieldWithDefault(this, 1, ""));
};


/**
 * @param {string} value
 * @return {!proto.duchess_backend_api.v1alpha1.Game} returns this
 */
proto.duchess_backend_api.v1alpha1.Game.prototype.setId = function(value) {
  return jspb.Message.setProto3StringField(this, 1, value);
};


/**
 * optional Position position = 2;
 * @return {?proto.duchess_backend_api.v1alpha1.Position}
 */
proto.duchess_backend_api.v1alpha1.Game.prototype.getPosition = function() {
  return /** @type{?proto.duchess_backend_api.v1alpha1.Position} */ (
    jspb.Message.getWrapperField(this, proto.duchess_backend_api.v1alpha1.Position, 2));
};


/**
 * @param {?proto.duchess_backend_api.v1alpha1.Position|undefined} value
 * @return {!proto.duchess_backend_api.v1alpha1.Game} returns this
*/
proto.duchess_backend_api.v1alpha1.Game.prototype.setPosition = function(value) {
  return jspb.Message.setWrapperField(this, 2, value);
};


/**
 * Clears the message field making it undefined.
 * @return {!proto.duchess_backend_api.v1alpha1.Game} returns this
 */
proto.duchess_backend_api.v1alpha1.Game.prototype.clearPosition = function() {
  return this.setPosition(undefined);
};


/**
 * Returns whether this field is set.
 * @return {boolean}
 */
proto.duchess_backend_api.v1alpha1.Game.prototype.hasPosition = function() {
  return jspb.Message.getField(this, 2) != null;
};


