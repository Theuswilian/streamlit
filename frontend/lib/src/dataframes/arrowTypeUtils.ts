/**
 * Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022-2024)
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

import { Dictionary, Struct, StructRow, Vector } from "apache-arrow"

/** Data types used by ArrowJS. */
export type DataType =
  | null
  | boolean
  | number
  | string
  | Date // datetime
  | Int32Array // int
  | Uint8Array // bytes
  | Uint32Array // Decimal
  | Vector // arrays
  | StructRow // interval
  | Dictionary // categorical
  | Struct // dict
  | bigint // period

export enum IndexTypeName {
  CategoricalIndex = "categorical",
  DatetimeIndex = "datetime",
  Float64Index = "float64",
  Int64Index = "int64",
  RangeIndex = "range",
  UInt64Index = "uint64",
  UnicodeIndex = "unicode",

  // Throws an error.
  TimedeltaIndex = "time",
}

/** Type information for single-index columns, and data columns. */
export interface Type {
  /** The type label returned by pandas.api.types.infer_dtype */
  // NOTE: `DataTypeName` should be used here, but as it's hard (maybe impossible)
  // to define such recursive types in TS, `string` will suffice for now.
  pandas_type: IndexTypeName | string

  /** The numpy dtype that corresponds to the types returned in df.dtypes */
  numpy_type: string

  /** Type metadata. */
  meta?: Record<string, any> | null
}

/** Metadata for the "range" index type. */
export interface RangeIndex {
  kind: "range"
  name: string | null
  start: number
  step: number
  stop: number
}

/** True if the index name represents a "range" index. */
export function isRangeIndex(
  indexName: string | RangeIndex
): indexName is RangeIndex {
  return typeof indexName === "object" && indexName.kind === "range"
}

/** Returns type for a single-index column or data column. */
export function getTypeName(type: Type): IndexTypeName | string {
  // For `PeriodType` and `IntervalType` types are kept in `numpy_type`,
  // for the rest of the indexes in `pandas_type`.
  return type.pandas_type === "object" ? type.numpy_type : type.pandas_type
}

/** True if both arrays contain the same data types in the same order. */
export function sameDataTypes(t1: Type[], t2: Type[]): boolean {
  // NOTE: We remove extra columns from the DataFrame that we add rows from.
  // Thus, as long as the length of `t2` is >= than `t1`, this will work properly.
  // For columns, `pandas_type` will point us to the correct type.
  return t1.every(
    (type: Type, index: number) => type.pandas_type === t2[index]?.pandas_type
  )
}

/** True if both arrays contain the same index types in the same order. */
export function sameIndexTypes(t1: Type[], t2: Type[]): boolean {
  // Make sure both indexes have same dimensions.
  if (t1.length !== t2.length) {
    return false
  }

  return t1.every(
    (type: Type, index: number) =>
      index < t2.length && getTypeName(type) === getTypeName(t2[index])
  )
}

/** Returns the timezone of the arrow type metadata. */
export function getTimezone(arrowType: Type): string | undefined {
  // TODO(lukasmasuch): Use info from field instead:
  // return arrowType?.field?.type?.timezone
  return arrowType?.meta?.timezone
}

/** True if the arrow type is an integer type.
 * For example: int8, int16, int32, int64, uint8, uint16, uint32, uint64, range
 */
export function isIntegerType(arrowType: Type): boolean {
  const typeName = getTypeName(arrowType) ?? ""
  return (
    (typeName.startsWith("int") && !typeName.startsWith("interval")) ||
    typeName === "range" ||
    typeName.startsWith("uint")
  )
}

/** True if the arrow type is an unsigned integer type. */
export function isUnsignedIntegerType(arrowType: Type): boolean {
  const typeName = getTypeName(arrowType) ?? ""
  return typeName.startsWith("uint")
}

/** True if the arrow type is a float type.
 * For example: float16, float32, float64, float96, float128
 */
export function isFloatType(arrowType: Type): boolean {
  const typeName = getTypeName(arrowType) ?? ""
  return typeName.startsWith("float")
}

/** True if the arrow type is a decimal type. */
export function isDecimalType(arrowType: Type): boolean {
  return getTypeName(arrowType) === "decimal"
}

/** True if the arrow type is a numeric type. */
export function isNumericType(arrowType: Type): boolean {
  return (
    isIntegerType(arrowType) ||
    isFloatType(arrowType) ||
    isDecimalType(arrowType)
  )
}

/** True if the arrow type is a boolean type. */
export function isBooleanType(arrowType: Type): boolean {
  return getTypeName(arrowType) === "bool"
}
