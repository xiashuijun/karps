package org.karps.structures

import org.apache.spark.rdd.RDD
import org.apache.spark.sql.catalyst.plans.QueryPlan
import org.apache.spark.sql.catalyst.trees.TreeNode

import karps.core.{graph => G}
import karps.core.{computation => C}
import tensorflow.node_def.NodeDef


case class RDDId private (repr: Int) extends AnyVal

object RDDId {
  def fromRDD(rdd: RDD[_]): RDDId = new RDDId(rdd.id)

  implicit object MyOrdering extends Ordering[RDDId] {
    override def compare(x: RDDId, y: RDDId): Int = x.repr.compare(y.repr)
  }
}

/**
 * Some basic information about RDDs that is exposed and sent to clients.
 */
case class RDDInfo private (
  id: RDDId,
  className: String,
  repr: String, // A human-readable representation of the RDD
  parents: Seq[RDDId],
  proto: Option[NodeDef])

object RDDInfo {
  def fromRDD(rdd: RDD[_]): RDDInfo = {
    val parents = rdd.dependencies.map(_.rdd).map(RDDId.fromRDD)
    new RDDInfo(
      RDDId.fromRDD(rdd),
      rdd.getClass.getSimpleName,
      rdd.toString(),
      parents,
      None)
  }
  
  def toProto(r: RDDInfo): C.RDDInfo = {
    C.RDDInfo(
      rddId = r.id.repr,
      className = r.className,
      repr = r.repr,
      parents = r.parents.map(_.repr.toLong),
      proto = r.proto
    )
  }
}

case class SQLTreeInfo(
    // Used as a node path
    nodeId: SQLTreeInfo.TreeInfoNodeId,
    fullName : String,
    parentNodes: Seq[SQLTreeInfo],
    proto: Option[NodeDef],
    planNode: Option[Any]) { // Should be QueryPlan[_], but erased for simplification.
  override def toString: String = s"SQLTreeInfo(nodeId=$nodeId)"
}

object SQLTreeInfo {
  type TreeInfoNodeId = String

  def toProto(sti: SQLTreeInfo): Seq[C.SQLTreeInfo] = {
    val n = C.SQLTreeInfo(
      nodeId = sti.nodeId,
      fullName = sti.fullName,
      parentNodes = sti.parentNodes.map(_.nodeId),
      proto = sti.proto
    )
    val cs = sti.parentNodes.flatMap(toProto)
    n +: cs
  }
}