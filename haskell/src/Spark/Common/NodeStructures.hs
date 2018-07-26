{-# LANGUAGE MultiParamTypeClasses #-}
{-# LANGUAGE RankNTypes #-}
{-# LANGUAGE TypeSynonymInstances #-}
{-# LANGUAGE FlexibleInstances #-}
{-# LANGUAGE TypeFamilies #-}

module Spark.Common.NodeStructures where

import Data.Vector(Vector)
import qualified Data.Vector as V
import qualified Data.Text as T

import Spark.Common.RowStructures
import Spark.Common.OpStructures
import Spark.Common.StructuresInternal
import Spark.Common.TypesStructures

{-| (internal) The main data structure that represents a data node in the
computation graph.

This data structure forms the backbone of computation graphs expressed
with spark operations.

loc is a typed locality tag.
a is the type of the data, as seen by the Haskell compiler. If erased, it
will be a Cell type.
-}
-- TODO: separate the topology info from the node info. It will help when
-- building the graphs.
data ComputeNode loc a = ComputeNode {
  -- | The id of the node.
  --
  -- Non strict because it may be expensive.
  _cnNodeId :: NodeId,
  -- The following fields are used to build a unique ID to
  -- a compute node:

  -- | The operation associated to this node.
  _cnOp :: !NodeOp,
  -- | The type of the node
  _cnType :: !DataType,
  -- | The direct parents of the node. The order of the parents is important
  -- for the semantics of the operation.
  _cnParents :: !(Vector UntypedNode),
  -- | A set of extra dependencies that can be added to force an order between
  -- the nodes.
  --
  -- The order is not important, they are sorted by ID.
  --
  -- TODO(kps) add this one to the id
  _cnLogicalDeps :: !(Vector UntypedNode),
  -- | The locality of this node.
  --
  -- TODO(kps) add this one to the id
  _cnLocality :: !Locality,
  -- Attributes that are not included in the id
  -- These attributes are mostly for the user to relate to the nodes.
  -- They are not necessary for the computation.
  --
  -- | The name
  _cnName :: !(Maybe NodeName),
  -- | A set of nodes considered as the logical input for this node.
  -- This has no influence on the calculation of the id and is used
  -- for organization purposes only.
  _cnLogicalParents :: !(Maybe (Vector UntypedNode)),
  -- | The path of this oned in a computation flow.
  --
  -- This path includes the node name.
  -- Not strict because it may be expensive to compute.
  -- By default it only contains the name of the node (i.e. the node is
  -- attached to the root)
  _cnPath :: NodePath
} deriving (Eq)

{-| Converts a compute node to an operator node.
-}
nodeOpNode :: ComputeNode loc a -> OperatorNode
nodeOpNode cn = OperatorNode {
      onId = _cnNodeId cn,
      onPath = _cnPath cn,
      onNodeInfo = CoreNodeInfo {
        cniShape = NodeShape {
          nsType = _cnType cn,
          nsLocality = _cnLocality cn
        },
        cniOp = _cnOp cn
      }
    }


nodeContext :: ComputeNode loc a -> NodeContext
nodeContext cn = NodeContext {
    ncParents = nodeOpNode <$> V.toList (_cnParents cn),
    ncLogicalDeps = nodeOpNode <$> V.toList (_cnLogicalDeps cn)
  }

-- (internal) Phantom type tags for the locality
data LocUnknown

{-| (internal/developer)
The core data structure that represents an operator.
This contains all the information that is required in
the compute graph (except topological info), which is
expected to be stored in the edges.

These nodes are meant to be used after path resolution.
-}
data OperatorNode = OperatorNode {
  {-| The ID of the node.
  Lazy because it may be expensive to compute.
  -- TODO: it should not be here?
  -}
  onId :: NodeId,
  {-| The fully resolved path of the node.
  Lazy because it may depend on the ID.
  -}
  onPath :: NodePath,
  {-| The core node information. -}
  onNodeInfo :: !CoreNodeInfo
} deriving (Eq)
-- Some helper functions:

onShape :: OperatorNode -> NodeShape
onShape = cniShape . onNodeInfo

onOp :: OperatorNode -> NodeOp
onOp = cniOp . onNodeInfo

onType :: OperatorNode -> DataType
onType = nsType . cniShape . onNodeInfo

onLocality :: OperatorNode -> Locality
onLocality = nsLocality . cniShape . onNodeInfo

{-| A node and some information about the parents of this node.

This information is enough to calculate most information relative
to a node.

This is the local context of the compute DAG.
-}
data NodeContext = NodeContext {
  ncParents :: ![OperatorNode],
  ncLogicalDeps :: ![OperatorNode]
}

-- (developer) The type for which we drop all the information expressed in
-- types.
--
-- This is useful to express parent dependencies (pending a more type-safe
-- interface)
type UntypedNode = ComputeNode LocUnknown Cell


{-| The different paths of edges in the compute DAG of nodes, at the
start of computations.

 - scope edges specify the scope of a node for naming. They are not included in
   the id.

-}
data NodeEdge = ScopeEdge | DataStructureEdge StructureEdge deriving (Show, Eq)

{-| The edges in a compute DAG, after name resolution (which is where most of
the checks and computations are being done)

- parent edges are the direct parents of a node, the only ones required for
  defining computations. They are included in the id.
- logical edges define logical dependencies between nodes to force a specific
  ordering of the nodes. They are included in the id.
-}
data StructureEdge = ParentEdge | LogicalEdge deriving (Show, Eq)

{-| A typed wrapper around the locality.
-}
data TypedLocality loc = TypedLocality { unTypedLocality :: !Locality } deriving (Eq, Show)


instance Show OperatorNode where
  show (OperatorNode _ np _) = "OperatorNode[" ++ T.unpack (prettyNodePath np) ++ "]"
