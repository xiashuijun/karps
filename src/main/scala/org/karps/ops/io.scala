package org.karps.ops

import org.apache.spark.sql.{DataFrame, DataFrameReader}
import com.typesafe.scalalogging.slf4j.{StrictLogging => Logging}
import org.apache.spark.sql.types._
import org.karps.row._
// import spray.json.{JsArray, JsBoolean, JsNull, JsNumber, JsObject, JsString, JsValue}

import scala.util.{Failure, Success, Try}
import karps.core.{io => IO}
import karps.core.{types => T}
import org.karps.structures._

/**
 * Reader objects for Spark.
 */
object Readers {

//   import JsonSparkConversions._

  import org.karps.structures.ProtoUtils._

//   def buildDF(reader: DataFrameReader, opts: JsValue): Try[DataFrame] = {
//     opts match {
//       case JsObject(m) =>
//         for {
//           o <- getObject(m, "options")
//           inputPath <- getString(m, "inputPath")
//           inputSource <- getString(m, "inputSource")
//           reader2 <- addOptions(reader, o)
//           reader3 <- addSchema(reader2, m)
//           // This can blow up badly if the file does not exist
//           res <- Try(reader3.format(inputSource).load(inputPath))
//         } yield {
//           res
//         }
//       case x => Failure(new Exception(s"Expected dictionary, got $x"))
//     }
//   }
  
  def buildDF(reader: DataFrameReader, ex: OpExtra): Try[DataFrame] = {
    ProtoUtils.fromExtra[IO.SourceDescription](ex).flatMap(buildDF(reader, _))
  }
  
  private def buildDF(reader: DataFrameReader, opts: IO.SourceDescription): Try[DataFrame] = {
    for {
      inputPath <- checkField(opts.path, "path")
      inputSource <- checkField(opts.source, "source")
      reader2 <- addOptions(reader, opts.options)
      reader3 <- addSchema(reader2, opts.schema)
      // This can blow up badly if the file does not exist
      res <- Try(reader3.format(inputSource).load(inputPath))      
    } yield { res }
  }
  
  private def addSchema(
      reader: DataFrameReader,
      schema: Option[T.SQLType]): Try[DataFrameReader] = schema match {
    case Some(sqlt) =>
      AugmentedDataType.fromProto(sqlt).map(_.topLevelStruct).flatMap {
        case Some(st) => Success(reader.schema(st))
        case None => Failure(new Exception(s"Expected a structure at the top level"))
      }      
    case _ => Success(reader)
  }

//   private def addSchema(reader: DataFrameReader,
//                         m: Map[String, JsValue]): Try[DataFrameReader] = {
//     getFlatten(m, "inputSchema") {
//       case JsNull => Success(reader)
//       case JsString("infer_schema") => Success(reader)
//       case x => (for {
//         adt <- deserializeDataType(x)
//       } yield {
//         adt.topLevelStruct match {
//           case Some(str) => Success(reader.schema(str))
//           case x => Failure(new Exception(s"Expected a structure at the top level"))
//         }
//       }).flatten
//     }
//   }
  
  private def addOptions(
      reader: DataFrameReader,
      opts: Seq[IO.InputOption]): Try[DataFrameReader] = {
    if (opts.isEmpty) {
      Success(reader)
    } else {
      val o = opts.head
      for {
        k <- checkField(o.key, "key")
        r2 <- addOption(reader, k, o.value)
        r2 <- addOptions(r2, opts.tail)
      } yield { r2 }
    }
  }
  
  private def addOption(
      r: DataFrameReader,
      k: String,
      v: IO.InputOption.Value): Try[DataFrameReader] = {
    import IO.InputOption.Value
    v match {
      case Value.Empty =>
        Failure(new Exception("Missing value"))
      case Value.IntValue(i) =>
        Success(r.option(k, i))
      case Value.DoubleValue(i) =>
        Success(r.option(k, i))
      case Value.StrValue(i) =>
        Success(r.option(k, i))
      case Value.BoolValue(i) =>
        Success(r.option(k, i))
      }
  }

//   private def addOptions(reader: DataFrameReader, opts: JsObject): Try[DataFrameReader] = {
//     def f(m: Map[String, JsValue]): Try[DataFrameReader] = {
//       if (m.isEmpty) Success(reader) else {
//         val (k, v) = m.head
//         for {
//           reader2 <- f(m.tail)
//           reader3 <- addOption(reader2, k, v)
//         } yield reader3
//       }
//     }
//     f(opts.fields)
//   }
// 
//   private def addOption(reader: DataFrameReader, key: String, o: JsValue): Try[DataFrameReader] = {
//     o match {
//       case JsBoolean(b) =>
//         Success(reader.option(key, b))
//       case JsString(s) =>
//         Success(reader.option(key, s))
//       case JsNumber(x) => // TODO: ambiguous here
//         Success(reader.option(key, x.toLong))
//       case x => Failure(new Exception(s"Not understood as value: $x"))
//     }
//   }
}

object TypeConversions {

  private val cellStructure = {
    StructType(Seq(
      StructField("fieldNames", ArrayType(StringType, containsNull = false), nullable = false),
      StructField("isNullable", BooleanType, nullable = false),
      StructField("typeId", IntegerType, nullable = false),
      StructField("fieldIndex", IntegerType, nullable = false)
    ))
  }

  val typeStructure = {
    StructType(Seq(
      StructField("rows", ArrayType(cellStructure, containsNull = false))
    ))
  }

  def toRow(s: StructType): AlgebraicRow = {
    AlgebraicRow(Seq(RowArray(toRows(s, IsStrict, Nil, 0))))
  }

  private def toRows(
      dt: DataType, nl: Nullable, path: Seq[String], pos: Int): Seq[Cell] = dt match {
    case IntegerType => prim(0, nl, path, pos)
    // TODO: this is a shortcut for the long data for now.
    case LongType => prim(0, nl, path, pos)
    case StringType => prim(1, nl, path, pos)
    case BooleanType => prim(2, nl, path, pos)


    case st: StructType =>
      val names = st.fields.map { f => StringElement(f.name) }
      val innerTypes = st.fields.zipWithIndex.flatMap { case (f, idx) =>
        val inNl = if (f.nullable) IsNullable else IsStrict
        toRows(f.dataType, inNl, path :+ f.name, idx)
      }
      val s = rowCell(
        RowArray(path.map(StringElement)),
        nullableFlag(nl),
        IntElement(10),
        IntElement(pos)
      )
      innerTypes :+ s

    case at: ArrayType =>
      val inNl = if (at.containsNull) IsNullable else IsStrict
      val s1 = rowCell(
          RowArray(path.map(StringElement)),
          nullableFlag(nl),
          IntElement(11),
          IntElement(pos)
        )
      val s2 = toRows(at.elementType, inNl, path :+ "arr", 0)
      s1 +: s2
  }

  private def prim(tpId: Int, nl: Nullable, path: Seq[String], pos: Int): Seq[Cell] = {
    Seq(RowCell(AlgebraicRow(Seq(
      RowArray(path.map(StringElement)),
      nullableFlag(nl),
      IntElement(tpId),
      IntElement(pos)))))
  }

  private def nullableFlag(nl: Nullable): BoolElement = {
    val isNullable = if (nl == IsStrict) false else true
    BoolElement(isNullable)
  }

  private def rowCell(xs: Cell*): Cell = RowCell(AlgebraicRow(xs))
}
