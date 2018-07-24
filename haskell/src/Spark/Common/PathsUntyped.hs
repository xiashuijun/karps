{-# OPTIONS_GHC -fno-warn-orphans #-}
{-# LANGUAGE MultiParamTypeClasses #-}
{-# LANGUAGE TypeSynonymInstances #-}
{-# LANGUAGE FlexibleInstances #-}
{-# LANGUAGE FlexibleContexts #-}
{-# LANGUAGE OverloadedStrings #-}

module Spark.Common.PathsUntyped(
  assignPathsUntyped,
  tieNodes
) where

import qualified Data.Vector as V
import Data.Maybe(fromMaybe)
import Data.List(nub)
import Control.Arrow((&&&))
import Formatting
import Control.Monad.Identity

import qualified Spark.Common.DAGFunctions as DAG
import Spark.Common.DAGStructures
-- import Spark.Common.DAGFunctions
import Spark.Common.ComputeDag
import Spark.Common.DatasetStructures
import Spark.Common.DatasetFunctions
import Spark.Common.Paths
import Spark.Common.Utilities
import Spark.Common.Try
import Spark.Common.StructuresInternal(unNodeId)

instance GraphVertexOperations UntypedNode where
  vertexToId = VertexId . unNodeId . nodeId
  expandVertexAsVertices n =
    nodeParents n
      ++ fromMaybe [] (nodeLogicalParents n)
      ++ nodeLogicalDependencies n

instance GraphOperations UntypedNode NodeEdge where
  expandVertex n =
    -- The logical parents are more important than the parents
    let
      -- If the logical parents are not specified, the logical parents are the
      -- direct parents.
      scopeNodes = fromMaybe (nodeParents n) (nodeLogicalParents n)
      loParents = [(ScopeEdge, v) | v <- scopeNodes]
      -- The direct parents. They may overload with the scoping parents, but
      -- this will be checked during the name analysis.
      parents' = (const (DataStructureEdge ParentEdge) &&& id) <$> nodeParents n
      loDeps = (const (DataStructureEdge LogicalEdge) &&& id) <$> nodeLogicalDependencies n
    in loParents ++ parents' ++ loDeps

instance GraphOperations UntypedNode StructureEdge where
  expandVertex n =
    -- The logical parents are more important than the parents
    let
      -- The direct parents. They may overload with the scoping parents, but
      -- this will be checked during the name analysis.
      parents' = (const ParentEdge &&& id) <$> nodeParents n
      loDeps = (const LogicalEdge &&& id) <$> nodeLogicalDependencies n
    in parents' ++ loDeps

instance HasNodeName UntypedNode where
  getNodeName = nodeName
  assignPath n p = updateNode n $ \n' -> n' { _cnPath = p }


-- Stitches the nodes together to make sure that the edges in the graph also
-- correspond to the dependencies in the nodes themselves.
-- This does not update the nodeIds
-- This must happen before the pruning is performed, otherwise the node IDs will
-- not match.
tieNodes :: ComputeDag UntypedNode StructureEdge -> ComputeDag UntypedNode StructureEdge
tieNodes cd =
  let g = computeGraphToGraph cd
      f :: UntypedNode -> [(UntypedNode, StructureEdge)] -> Identity UntypedNode
      f v l =
        let parents' = V.fromList [n | (n, e) <- l, e == ParentEdge]
            logDeps = V.fromList [n | (n, e) <- l, e == LogicalEdge]
            res = updateNode v $ \n -> n {
                  _cnParents = parents',
                  _cnLogicalDeps = logDeps,
                  _cnLogicalParents = Nothing }
        in return res
      g2 = runIdentity $ DAG.graphMapVertices g f
  in graphToComputeGraph g2

-- Assigns the paths, and drops the scoping edges.
assignPathsUntyped :: (HasCallStack) =>
  ComputeDag UntypedNode NodeEdge -> Try (ComputeDag UntypedNode StructureEdge)
assignPathsUntyped cd = do
  let pathCGraph = _getPathCDag cd
  paths <- computePaths pathCGraph
  let g = computeGraphToGraph $ assignPaths' paths cd
  let f _ ScopeEdge _ = Nothing
      f _ (DataStructureEdge x) _ = Just x
  let g' = DAG.graphFilterEdges g  f
  return $ graphToComputeGraph g'


-- transforms node edges into path edges
_cleanEdges :: (HasCallStack) => [VertexEdge NodeEdge v] -> [VertexEdge PathEdge v]
_cleanEdges [] = []
_cleanEdges (h : t) =
  let vid = vertexId (veEndVertex h)
      others = [ve | ve <- t, (vertexId . veEndVertex $ ve) /= vid]
      sames = [ve | ve <- t, (vertexId . veEndVertex $ ve) == vid]
      rest = _cleanEdges others
      e = veEdge h
      -- If there multiple edges between nodes, they are dropped.
      -- This distinction is not required for names.
      eData = nub $ edgeData . veEdge <$> (h : sames)
      eData' = case eData of
        [DataStructureEdge ParentEdge] -> Just InnerEdge
        [DataStructureEdge ParentEdge, ScopeEdge] -> Just SameLevelEdge
        [ScopeEdge, DataStructureEdge ParentEdge] -> Just SameLevelEdge
        [ScopeEdge] -> Just SameLevelEdge
        [DataStructureEdge LogicalEdge] -> Nothing
        l -> failure (sformat ("Could not understand combination "%shown) l)
      res = case eData' of
        Just v -> (h { veEdge = e { edgeData = v } }) : rest
        Nothing -> rest
    in res

-- transforms node edges into path edges
_cleanEdges' :: (HasCallStack) => [IndexedEdge NodeEdge] -> [IndexedEdge PathEdge]
_cleanEdges' [] = []
_cleanEdges' (h : t) =
  let vid = iedgeTo h
      others = [ie | ie <- t, (iedgeTo $ ie) /= vid]
      sames = [ie | ie <- t, (iedgeTo $ ie) == vid]
      rest = _cleanEdges' others
      -- If there multiple edges between nodes, they are dropped.
      -- This distinction is not required for names.
      eData = nub $ iedgeData <$> (h : sames)
      eData' = case eData of
        [DataStructureEdge ParentEdge] -> Just InnerEdge
        [DataStructureEdge ParentEdge, ScopeEdge] -> Just SameLevelEdge
        [ScopeEdge, DataStructureEdge ParentEdge] -> Just SameLevelEdge
        [ScopeEdge] -> Just SameLevelEdge
        [DataStructureEdge LogicalEdge] -> Nothing
        l -> failure (sformat ("Could not understand combination "%shown) l)
      res = case eData' of
        Just v -> h {iedgeData = v} : rest
        Nothing -> rest
    in res

_getPathCDag :: (HasCallStack, Show v) => ComputeDag v NodeEdge -> ComputeDag v PathEdge
_getPathCDag cd = forceRight . tryEither $ updateGraph (const g) cd where
  vxs = V.toList . cdVertices $ cd
  ies = _cleanEdges' (gIndexedEdges (computeGraphToGraph cd))
  g =  DAG.buildGraphFromList' vxs ies
  -- let adj' = M.map (V.fromList . _cleanEdges . toList) (cdEdges cd)
  -- in cd { cdEdges = adj' }