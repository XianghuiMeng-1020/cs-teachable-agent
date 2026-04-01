import { useState, useEffect, useRef } from "react";
import { useTranslation } from "react-i18next";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { 
  Network, 
  GitBranch, 
  Layers, 
  Zap,
  Info,
  ZoomIn,
  ZoomOut,
  RotateCcw,
  Maximize2
} from "lucide-react";
import { motion } from "framer-motion";

interface ConceptNode {
  id: string;
  name: string;
  x: number;
  y: number;
  centrality: number;
  level: number;
}

interface ConceptEdge {
  source: string;
  target: string;
  type: string;
  strength: number;
}

interface ConceptRelationData {
  concepts_count: number;
  relations_count: number;
  clusters: string[][];
  critical_paths: string[][];
  central_concepts: { id: string; centrality: number }[];
  relations_by_type: Record<string, number>;
}

interface ConceptRelationGraphProps {
  data?: ConceptRelationData;
  className?: string;
}

export function ConceptRelationGraph({ data, className }: ConceptRelationGraphProps) {
  const { t } = useTranslation();
  const [isLoading, setIsLoading] = useState(true);
  const [selectedNode, setSelectedNode] = useState<string | null>(null);
  const [zoom, setZoom] = useState(1);
  const [offset, setOffset] = useState({ x: 0, y: 0 });
  const [isDragging, setIsDragging] = useState(false);
  const [dragStart, setDragStart] = useState({ x: 0, y: 0 });
  const svgRef = useRef<SVGSVGElement>(null);

  // Generate mock graph data
  const generateMockData = (): { nodes: ConceptNode[]; edges: ConceptEdge[] } => {
    const concepts = [
      { id: "variables", name: "变量", level: 1 },
      { id: "data_types", name: "数据类型", level: 2 },
      { id: "operators", name: "运算符", level: 2 },
      { id: "control_flow", name: "控制流", level: 3 },
      { id: "functions", name: "函数", level: 4 },
      { id: "lists", name: "列表", level: 3 },
      { id: "dictionaries", name: "字典", level: 4 },
      { id: "loops", name: "循环", level: 3 },
      { id: "conditionals", name: "条件语句", level: 3 },
      { id: "modules", name: "模块", level: 5 },
    ];

    const nodes: ConceptNode[] = concepts.map((c, i) => ({
      ...c,
      x: 100 + (i % 3) * 150 + Math.random() * 50,
      y: 80 + Math.floor(i / 3) * 120 + Math.random() * 30,
      centrality: Math.floor(Math.random() * 5),
    }));

    const edges: ConceptEdge[] = [
      { source: "variables", target: "data_types", type: "prerequisite", strength: 0.9 },
      { source: "variables", target: "operators", type: "prerequisite", strength: 0.8 },
      { source: "operators", target: "control_flow", type: "prerequisite", strength: 0.7 },
      { source: "conditionals", target: "control_flow", type: "part_of", strength: 0.9 },
      { source: "loops", target: "control_flow", type: "part_of", strength: 0.9 },
      { source: "control_flow", target: "functions", type: "prerequisite", strength: 0.8 },
      { source: "lists", target: "dictionaries", type: "prerequisite", strength: 0.7 },
      { source: "functions", target: "modules", type: "prerequisite", strength: 0.6 },
      { source: "variables", target: "lists", type: "prerequisite", strength: 0.8 },
      { source: "data_types", target: "lists", type: "similar", strength: 0.5 },
    ];

    return { nodes, edges };
  };

  const [graphData, setGraphData] = useState<{ nodes: ConceptNode[]; edges: ConceptEdge[] } | null>(null);

  useEffect(() => {
    setTimeout(() => {
      setGraphData(generateMockData());
      setIsLoading(false);
    }, 1500);
  }, []);

  const handleMouseDown = (e: React.MouseEvent) => {
    setIsDragging(true);
    setDragStart({ x: e.clientX - offset.x, y: e.clientY - offset.y });
  };

  const handleMouseMove = (e: React.MouseEvent) => {
    if (isDragging) {
      setOffset({
        x: e.clientX - dragStart.x,
        y: e.clientY - dragStart.y,
      });
    }
  };

  const handleMouseUp = () => {
    setIsDragging(false);
  };

  const handleZoomIn = () => setZoom((z) => Math.min(z * 1.2, 3));
  const handleZoomOut = () => setZoom((z) => Math.max(z / 1.2, 0.3));
  const handleReset = () => {
    setZoom(1);
    setOffset({ x: 0, y: 0 });
  };

  const getEdgeColor = (type: string) => {
    const colors: Record<string, string> = {
      prerequisite: "#0D9488",
      dependent: "#8b5cf6",
      similar: "#10b981",
      contrast: "#ef4444",
      part_of: "#f59e0b",
      extends: "#3b82f6",
    };
    return colors[type] || "#94a3b8";
  };

  return (
    <Card padding="none" className={className}>
      {/* Header */}
      <div className="p-4 border-b border-stone-200 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-indigo-100 rounded-lg">
            <Network className="w-5 h-5 text-indigo-600" />
          </div>
          <div>
            <h3 className="font-semibold text-stone-900">{t("analytics.conceptGraph")}</h3>
            <p className="text-sm text-stone-500">{t("analytics.conceptGraphDesc")}</p>
          </div>
        </div>
        <div className="flex items-center gap-2">
          <Button variant="ghost" size="sm" onClick={handleZoomOut}>
            <ZoomOut className="w-4 h-4" />
          </Button>
          <span className="text-sm text-stone-600 min-w-[3rem] text-center">
            {Math.round(zoom * 100)}%
          </span>
          <Button variant="ghost" size="sm" onClick={handleZoomIn}>
            <ZoomIn className="w-4 h-4" />
          </Button>
          <Button variant="ghost" size="sm" onClick={handleReset}>
            <RotateCcw className="w-4 h-4" />
          </Button>
        </div>
      </div>

      {/* Graph Area */}
      <div 
        className="relative h-96 bg-stone-50 overflow-hidden cursor-grab active:cursor-grabbing"
        onMouseDown={handleMouseDown}
        onMouseMove={handleMouseMove}
        onMouseUp={handleMouseUp}
        onMouseLeave={handleMouseUp}
      >
        {isLoading ? (
          <div className="absolute inset-0 flex items-center justify-center">
            <motion.div
              animate={{ rotate: 360 }}
              transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
            >
              <GitBranch className="w-8 h-8 text-indigo-500" />
            </motion.div>
            <span className="ml-3 text-stone-600">{t("common.loading")}</span>
          </div>
        ) : graphData ? (
          <svg
            ref={svgRef}
            className="w-full h-full"
            style={{
              transform: `translate(${offset.x}px, ${offset.y}px) scale(${zoom})`,
              transformOrigin: "center",
            }}
          >
            {/* Edges */}
            {graphData.edges.map((edge, i) => {
              const source = graphData.nodes.find((n) => n.id === edge.source);
              const target = graphData.nodes.find((n) => n.id === edge.target);
              if (!source || !target) return null;

              return (
                <g key={i}>
                  <line
                    x1={source.x}
                    y1={source.y}
                    x2={target.x}
                    y2={target.y}
                    stroke={getEdgeColor(edge.type)}
                    strokeWidth={edge.strength * 3}
                    strokeOpacity={0.6}
                    markerEnd="url(#arrowhead)"
                  />
                </g>
              );
            })}

            {/* Arrow marker */}
            <defs>
              <marker
                id="arrowhead"
                markerWidth="10"
                markerHeight="7"
                refX="25"
                refY="3.5"
                orient="auto"
              >
                <polygon points="0 0, 10 3.5, 0 7" fill="#0D9488" opacity="0.6" />
              </marker>
            </defs>

            {/* Nodes */}
            {graphData.nodes.map((node) => (
              <g
                key={node.id}
                transform={`translate(${node.x}, ${node.y})`}
                className="cursor-pointer"
                onClick={() => setSelectedNode(node.id === selectedNode ? null : node.id)}
              >
                <circle
                  r={20 + node.centrality * 3}
                  fill={selectedNode === node.id ? "#0D9488" : "#fff"}
                  stroke={selectedNode === node.id ? "#4f46e5" : "#cbd5e1"}
                  strokeWidth={2}
                  className="transition-all duration-200"
                />
                <text
                  textAnchor="middle"
                  dominantBaseline="middle"
                  fill={selectedNode === node.id ? "#fff" : "#1e293b"}
                  fontSize="12"
                  fontWeight="500"
                  className="pointer-events-none"
                >
                  {node.name}
                </text>
                <text
                  textAnchor="middle"
                  y={35}
                  fill="#64748b"
                  fontSize="10"
                  className="pointer-events-none"
                >
                  {t("analytics.level")} {node.level}
                </text>
              </g>
            ))}
          </svg>
        ) : null}

        {/* Legend */}
        <div className="absolute bottom-4 left-4 bg-white/90 backdrop-blur rounded-lg p-3 shadow-lg">
          <p className="text-xs font-medium text-stone-700 mb-2">{t("analytics.conceptRelations")}</p>
          <div className="space-y-1">
            {[
              { type: "prerequisite", labelKey: "nav.teach", color: "#0D9488" },
              { type: "similar", labelKey: "analytics.crossDomainTitle", color: "#10b981" },
              { type: "part_of", labelKey: "mastery.topicCoverage", color: "#f59e0b" },
              { type: "extends", labelKey: "analytics.experiments", color: "#3b82f6" },
            ].map(({ type, labelKey, color }) => (
              <div key={type} className="flex items-center gap-2">
                <div 
                  className="w-4 h-0.5 rounded" 
                  style={{ backgroundColor: color }}
                />
                <span className="text-xs text-stone-600">{t(labelKey)}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Selected Node Info */}
        {selectedNode && graphData && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="absolute bottom-4 right-4 bg-white rounded-lg p-4 shadow-lg max-w-xs"
          >
            {(() => {
              const node = graphData.nodes.find((n) => n.id === selectedNode);
              if (!node) return null;
              return (
                <>
                  <h4 className="font-semibold text-stone-900">{node.name}</h4>
                  <p className="text-sm text-stone-500 mb-2">{t("analytics.level")}: {node.level}</p>
                  <div className="text-xs text-stone-600 space-y-1">
                    <p>{t("analytics.connections")}: {node.centrality}</p>
                    <p>{t("analytics.conceptRelations")}:</p>
                    <ul className="pl-4 space-y-0.5">
                      {graphData.edges
                        .filter((e) => e.source === selectedNode || e.target === selectedNode)
                        .map((e, i) => {
                          const otherId = e.source === selectedNode ? e.target : e.source;
                          const other = graphData.nodes.find((n) => n.id === otherId);
                          return (
                            <li key={i} className="text-stone-500">
                              • {other?.name} ({e.type === "prerequisite" ? t("nav.teach") : t("analytics.conceptRelations")})
                            </li>
                          );
                        })}
                    </ul>
                  </div>
                </>
              );
            })()}
          </motion.div>
        )}
      </div>

      {/* Stats */}
      {!isLoading && graphData && (
        <div className="grid grid-cols-4 gap-4 p-4 border-t border-stone-200">
          <div className="text-center">
            <p className="text-2xl font-bold text-stone-900">{graphData.nodes.length}</p>
            <p className="text-xs text-stone-500">{t("mastery.conceptMastery")}</p>
          </div>
          <div className="text-center">
            <p className="text-2xl font-bold text-stone-900">{graphData.edges.length}</p>
            <p className="text-xs text-stone-500">{t("analytics.connections")}</p>
          </div>
          <div className="text-center">
            <p className="text-2xl font-bold text-stone-900">{data?.clusters.length || 2}</p>
            <p className="text-xs text-stone-500">{t("analytics.crossDomainTitle")}</p>
          </div>
          <div className="text-center">
            <p className="text-2xl font-bold text-stone-900">{data?.critical_paths.length || 2}</p>
            <p className="text-xs text-stone-500">{t("analytics.recentTrend")}</p>
          </div>
        </div>
      )}
    </Card>
  );
}
