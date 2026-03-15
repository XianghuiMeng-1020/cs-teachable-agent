import { useEffect, useRef, useState } from "react";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { KnowledgeGraph } from "@/components/state/KnowledgeGraph";
import { 
  Box, 
  RotateCw, 
  Maximize2, 
  Minimize2, 
  ZoomIn, 
  ZoomOut,
  Layers,
  Info,
  Sparkles,
  Grid3X3,
  X,
  Smartphone,
  Cpu
} from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";

// Mock 3D graph data
interface Node3D {
  id: string;
  name: string;
  x: number;
  y: number;
  z: number;
  size: number;
  color: string;
  mastery: number;
  level: number;
  connections: string[];
}

interface Edge3D {
  source: string;
  target: string;
  strength: number;
  type: "prerequisite" | "similar" | "dependent" | "part_of";
}

const mockNodes: Node3D[] = [
  { id: "variables", name: "变量", x: 0, y: 0, z: 0, size: 1.5, color: "#6366f1", mastery: 0.9, level: 1, connections: ["data_types", "operators"] },
  { id: "data_types", name: "数据类型", x: 3, y: 2, z: 1, size: 1.3, color: "#8b5cf6", mastery: 0.85, level: 2, connections: ["variables", "lists", "dicts"] },
  { id: "operators", name: "运算符", x: -2, y: 3, z: -1, size: 1.2, color: "#ec4899", mastery: 0.8, level: 2, connections: ["variables", "expressions"] },
  { id: "control_flow", name: "控制流", x: 1, y: 5, z: 2, size: 1.6, color: "#10b981", mastery: 0.7, level: 3, connections: ["if_else", "loops", "functions"] },
  { id: "if_else", name: "条件语句", x: 4, y: 6, z: 0, size: 1.1, color: "#f59e0b", mastery: 0.75, level: 3, connections: ["control_flow", "operators"] },
  { id: "loops", name: "循环", x: -1, y: 7, z: 3, size: 1.4, color: "#14b8a6", mastery: 0.65, level: 3, connections: ["control_flow", "lists", "range"] },
  { id: "functions", name: "函数", x: 0, y: 9, z: -2, size: 1.7, color: "#3b82f6", mastery: 0.6, level: 4, connections: ["control_flow", "parameters", "return"] },
  { id: "lists", name: "列表", x: 6, y: 4, z: -3, size: 1.3, color: "#ef4444", mastery: 0.55, level: 3, connections: ["data_types", "loops", "indexing"] },
  { id: "dicts", name: "字典", x: 5, y: 1, z: 4, size: 1.3, color: "#f97316", mastery: 0.5, level: 4, connections: ["data_types", "json"] },
  { id: "classes", name: "类与对象", x: -4, y: 8, z: 1, size: 1.8, color: "#8b5cf6", mastery: 0.4, level: 5, connections: ["functions", "inheritance", "methods"] },
  { id: "inheritance", name: "继承", x: -6, y: 10, z: 2, size: 1.2, color: "#a855f7", mastery: 0.3, level: 5, connections: ["classes", "polymorphism"] },
  { id: "modules", name: "模块", x: 2, y: 11, z: 4, size: 1.4, color: "#06b6d4", mastery: 0.45, level: 4, connections: ["functions", "import"] },
  { id: "file_io", name: "文件IO", x: 7, y: 8, z: -1, size: 1.2, color: "#84cc16", mastery: 0.35, level: 4, connections: ["exceptions", "with"] },
  { id: "exceptions", name: "异常处理", x: 3, y: 10, z: -4, size: 1.3, color: "#f43f5e", mastery: 0.4, level: 4, connections: ["try_except", "functions"] },
  { id: "json", name: "JSON处理", x: 8, y: 3, z: 2, size: 1.1, color: "#eab308", mastery: 0.5, level: 5, connections: ["dicts", "file_io"] },
];

const mockEdges: Edge3D[] = [
  { source: "variables", target: "data_types", strength: 0.9, type: "prerequisite" },
  { source: "variables", target: "operators", strength: 0.8, type: "prerequisite" },
  { source: "operators", target: "control_flow", strength: 0.7, type: "prerequisite" },
  { source: "control_flow", target: "functions", strength: 0.8, type: "prerequisite" },
  { source: "data_types", target: "lists", strength: 0.7, type: "dependent" },
  { source: "data_types", target: "dicts", strength: 0.6, type: "dependent" },
  { source: "functions", target: "classes", strength: 0.9, type: "prerequisite" },
  { source: "classes", target: "inheritance", strength: 0.9, type: "part_of" },
  { source: "functions", target: "modules", strength: 0.6, type: "dependent" },
  { source: "lists", target: "loops", strength: 0.7, type: "similar" },
  { source: "if_else", target: "loops", strength: 0.5, type: "similar" },
  { source: "exceptions", target: "file_io", strength: 0.6, type: "prerequisite" },
  { source: "dicts", target: "json", strength: 0.8, type: "dependent" },
];

interface KnowledgeGraph3DProps {
  className?: string;
  units?: Array<{ unit_id: string; status: string; topic_group?: string }>;
  knowledgeUnitDefinitions?: unknown;
}

// Detect low-end device
function useDevicePerformance() {
  const [isLowEnd, setIsLowEnd] = useState(false);
  const [isMobile, setIsMobile] = useState(false);

  useEffect(() => {
    // Check for mobile device
    const mobileCheck = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(
      navigator.userAgent
    );
    setIsMobile(mobileCheck);

    // Check for low memory
    const memory = (navigator as any).deviceMemory;
    if (memory && memory < 4) {
      setIsLowEnd(true);
      return;
    }

    // Check for low-end CPU
    const cores = navigator.hardwareConcurrency;
    if (cores && cores < 4) {
      setIsLowEnd(true);
      return;
    }

    // Check connection speed
    const connection = (navigator as any).connection;
    if (connection && (connection.saveData || connection.effectiveType === '2g' || connection.effectiveType === 'slow-2g')) {
      setIsLowEnd(true);
      return;
    }

    // Test frame rate
    let frameCount = 0;
    const startTime = performance.now();
    
    const countFrames = () => {
      frameCount++;
      if (performance.now() - startTime < 1000) {
        requestAnimationFrame(countFrames);
      } else {
        // Less than 30fps is considered low-end
        if (frameCount < 30) {
          setIsLowEnd(true);
        }
      }
    };
    
    requestAnimationFrame(countFrames);
  }, []);

  return { isLowEnd, isMobile };
}

export function KnowledgeGraph3D({ className, units, knowledgeUnitDefinitions }: KnowledgeGraph3DProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [isExpanded, setIsExpanded] = useState(false);
  const [selectedNode, setSelectedNode] = useState<Node3D | null>(null);
  const [autoRotate, setAutoRotate] = useState(true);
  const [zoom, setZoom] = useState(1);
  const { isLowEnd, isMobile } = useDevicePerformance();
  const [viewMode, setViewMode] = useState<"3d" | "2d">(isLowEnd || isMobile ? "2d" : "3d");
  const [rotation, setRotation] = useState({ x: 0.3, y: 0.5 });
  const [isDragging, setIsDragging] = useState(false);
  const [lastMouse, setLastMouse] = useState({ x: 0, y: 0 });
  const [showPerformanceWarning, setShowPerformanceWarning] = useState(isLowEnd);

  // Simple 3D projection
  const project3D = (x: number, y: number, z: number, rotX: number, rotY: number, scale: number) => {
    // Rotate around Y axis
    let x1 = x * Math.cos(rotY) - z * Math.sin(rotY);
    let z1 = x * Math.sin(rotY) + z * Math.cos(rotY);
    
    // Rotate around X axis
    let y2 = y * Math.cos(rotX) - z1 * Math.sin(rotX);
    let z2 = y * Math.sin(rotX) + z1 * Math.cos(rotX);
    
    // Perspective projection
    const perspective = 800;
    const scale2 = perspective / (perspective + z2 + 10);
    
    return {
      x: x1 * scale * scale2,
      y: y2 * scale * scale2,
      z: z2,
      scale: scale2,
    };
  };

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    let animationId: number;

    const render = () => {
      // Auto rotation
      if (autoRotate && !isDragging) {
        setRotation((prev) => ({ ...prev, y: prev.y + 0.002 }));
      }

      // Clear canvas
      ctx.fillStyle = "#0f172a";
      ctx.fillRect(0, 0, canvas.width, canvas.height);

      const centerX = canvas.width / 2;
      const centerY = canvas.height / 2;

      // Project all nodes
      const projectedNodes = mockNodes.map((node) => {
        const projected = project3D(
          node.x * 30,
          node.y * 25,
          node.z * 20,
          rotation.x,
          rotation.y,
          zoom
        );
        return { ...node, projected };
      });

      // Sort by Z for proper rendering
      projectedNodes.sort((a, b) => b.projected.z - a.projected.z);

      // Draw edges first
      mockEdges.forEach((edge) => {
        const source = projectedNodes.find((n) => n.id === edge.source);
        const target = projectedNodes.find((n) => n.id === edge.target);
        if (!source || !target) return;

        const alpha = Math.max(0.1, (source.projected.scale + target.projected.scale) / 2 * 0.6);
        
        ctx.beginPath();
        ctx.moveTo(centerX + source.projected.x, centerY + source.projected.y);
        ctx.lineTo(centerX + target.projected.x, centerY + target.projected.y);
        ctx.strokeStyle = edge.type === "prerequisite" 
          ? `rgba(99, 102, 241, ${alpha})`
          : edge.type === "dependent"
          ? `rgba(16, 185, 129, ${alpha})`
          : `rgba(245, 158, 11, ${alpha})`;
        ctx.lineWidth = edge.strength * 2 * ((source.projected.scale + target.projected.scale) / 2);
        ctx.stroke();
      });

      // Draw nodes
      projectedNodes.forEach((node) => {
        const x = centerX + node.projected.x;
        const y = centerY + node.projected.y;
        const size = node.size * 15 * node.projected.scale;
        const alpha = Math.max(0.3, node.projected.scale);

        // Glow effect
        const gradient = ctx.createRadialGradient(x, y, 0, x, y, size * 2);
        gradient.addColorStop(0, `${node.color}${Math.floor(alpha * 255).toString(16).padStart(2, "0")}`);
        gradient.addColorStop(1, "transparent");
        
        ctx.beginPath();
        ctx.arc(x, y, size * 2, 0, Math.PI * 2);
        ctx.fillStyle = gradient;
        ctx.fill();

        // Core node
        ctx.beginPath();
        ctx.arc(x, y, size, 0, Math.PI * 2);
        ctx.fillStyle = node.color;
        ctx.globalAlpha = alpha;
        ctx.fill();
        ctx.globalAlpha = 1;

        // Mastery ring
        if (node.mastery > 0) {
          ctx.beginPath();
          ctx.arc(x, y, size + 5, -Math.PI / 2, -Math.PI / 2 + Math.PI * 2 * node.mastery);
          ctx.strokeStyle = `rgba(255, 255, 255, ${alpha * 0.8})`;
          ctx.lineWidth = 2;
          ctx.stroke();
        }

        // Label
        ctx.font = `${Math.max(10, 12 * node.projected.scale)}px system-ui`;
        ctx.fillStyle = `rgba(255, 255, 255, ${alpha})`;
        ctx.textAlign = "center";
        ctx.textBaseline = "middle";
        ctx.fillText(node.name, x, y + size + 15);
      });

      animationId = requestAnimationFrame(render);
    };

    render();

    return () => cancelAnimationFrame(animationId);
  }, [rotation, zoom, autoRotate, isDragging]);

  const handleMouseDown = (e: React.MouseEvent) => {
    setIsDragging(true);
    setLastMouse({ x: e.clientX, y: e.clientY });
    setAutoRotate(false);
  };

  const handleMouseMove = (e: React.MouseEvent) => {
    if (!isDragging) return;
    const dx = e.clientX - lastMouse.x;
    const dy = e.clientY - lastMouse.y;
    setRotation((prev) => ({
      y: prev.y + dx * 0.01,
      x: Math.max(-Math.PI / 2, Math.min(Math.PI / 2, prev.x + dy * 0.01)),
    }));
    setLastMouse({ x: e.clientX, y: e.clientY });
  };

  const handleMouseUp = () => {
    setIsDragging(false);
  };

  const handleNodeClick = (e: React.MouseEvent) => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const rect = canvas.getBoundingClientRect();
    const x = e.clientX - rect.left - canvas.width / 2;
    const y = e.clientY - rect.top - canvas.height / 2;

    // Find clicked node
    let closest: Node3D | null = null;
    let minDist = Infinity;

    mockNodes.forEach((node) => {
      const projected = project3D(
        node.x * 30,
        node.y * 25,
        node.z * 20,
        rotation.x,
        rotation.y,
        zoom
      );
      const dist = Math.hypot(x - projected.x, y - projected.y);
      const size = node.size * 15 * projected.scale;
      if (dist < size && dist < minDist) {
        minDist = dist;
        closest = node;
      }
    });

    setSelectedNode(closest);
  };

  // Handle performance warning dismiss
  const dismissPerformanceWarning = () => {
    setShowPerformanceWarning(false);
    setViewMode("2d");
  };

  return (
    <Card 
      padding="none" 
      className={`relative overflow-hidden ${isExpanded ? "fixed inset-4 z-50" : className}`}
    >
      {/* Performance Warning */}
      <AnimatePresence>
        {showPerformanceWarning && viewMode === "3d" && (
          <motion.div
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            className="absolute top-0 left-0 right-0 z-20 bg-amber-500/90 backdrop-blur-sm p-2 text-center text-white text-sm"
          >
            <div className="flex items-center justify-center gap-2">
              <span>⚡ 检测到设备性能较低，建议使用2D视图以获得更流畅体验</span>
              <button 
                onClick={dismissPerformanceWarning}
                className="px-2 py-0.5 bg-white/20 hover:bg-white/30 rounded text-xs font-medium transition-colors"
              >
                切换到2D
              </button>
              <button 
                onClick={() => setShowPerformanceWarning(false)}
                className="p-1 hover:bg-white/20 rounded"
              >
                <X className="w-4 h-4" />
              </button>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Header */}
      <div className="absolute top-0 left-0 right-0 z-10 flex items-center justify-between p-4 bg-gradient-to-b from-slate-900/80 to-transparent">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-indigo-500/20 rounded-lg backdrop-blur">
            {viewMode === "3d" ? (
              <Box className="w-5 h-5 text-indigo-400" />
            ) : (
              <Grid3X3 className="w-5 h-5 text-emerald-400" />
            )}
          </div>
          <div>
            <h3 className="font-semibold text-white">
              {viewMode === "3d" ? "3D知识图谱" : "2D知识图谱"}
            </h3>
            <p className="text-sm text-slate-400">
              {viewMode === "3d" ? "沉浸式概念探索" : "清晰的概念关系视图"}
              {(isMobile || isLowEnd) && viewMode === "3d" && " (性能模式推荐2D)"}
            </p>
          </div>
        </div>
        <div className="flex items-center gap-2">
          <Button
            variant="ghost"
            size="sm"
            onClick={() => setAutoRotate(!autoRotate)}
            className="text-slate-300 hover:text-white hover:bg-white/10"
          >
            <RotateCw className={`w-4 h-4 ${autoRotate ? "animate-spin" : ""}`} />
          </Button>
          <Button
            variant="ghost"
            size="sm"
            onClick={() => setZoom((z) => Math.min(z * 1.2, 3))}
            className="text-slate-300 hover:text-white hover:bg-white/10"
          >
            <ZoomIn className="w-4 h-4" />
          </Button>
          <Button
            variant="ghost"
            size="sm"
            onClick={() => setZoom((z) => Math.max(z / 1.2, 0.3))}
            className="text-slate-300 hover:text-white hover:bg-white/10"
          >
            <ZoomOut className="w-4 h-4" />
          </Button>
          <Button
            variant="ghost"
            size="sm"
            onClick={() => setViewMode(viewMode === "3d" ? "2d" : "3d")}
            className="text-slate-300 hover:text-white hover:bg-white/10 hidden sm:flex"
            title={viewMode === "3d" ? "Switch to 2D View" : "Switch to 3D View"}
          >
            {viewMode === "3d" ? <Grid3X3 className="w-4 h-4" /> : <Box className="w-4 h-4" />}
          </Button>
          <Button
            variant="ghost"
            size="sm"
            onClick={() => setIsExpanded(!isExpanded)}
            className="text-slate-300 hover:text-white hover:bg-white/10"
          >
            {isExpanded ? <Minimize2 className="w-4 h-4" /> : <Maximize2 className="w-4 h-4" />}
          </Button>
        </div>
      </div>

      {/* Content Area */}
      {viewMode === "2d" && units ? (
        <div className="h-full bg-slate-50 p-4 overflow-auto">
          <KnowledgeGraph 
            units={units} 
            knowledgeUnitDefinitions={knowledgeUnitDefinitions}
            className="h-full"
          />
        </div>
      ) : (
        /* Canvas */
        <canvas
          ref={canvasRef}
          width={isExpanded ? window.innerWidth - 32 : 800}
          height={isExpanded ? window.innerHeight - 32 : 500}
          className="cursor-grab active:cursor-grabbing"
          onMouseDown={handleMouseDown}
          onMouseMove={handleMouseMove}
          onMouseUp={handleMouseUp}
          onMouseLeave={handleMouseUp}
          onClick={handleNodeClick}
        />
      )}

      {/* Legend */}
      <div className="absolute bottom-4 left-4 bg-slate-900/80 backdrop-blur rounded-lg p-3">
        <p className="text-xs text-slate-400 mb-2">关系类型</p>
        <div className="space-y-1">
          <div className="flex items-center gap-2">
            <div className="w-6 h-0.5 bg-indigo-500 rounded" />
            <span className="text-xs text-slate-300">前置知识</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-6 h-0.5 bg-emerald-500 rounded" />
            <span className="text-xs text-slate-300">依赖关系</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-6 h-0.5 bg-amber-500 rounded" />
            <span className="text-xs text-slate-300">相似概念</span>
          </div>
        </div>
      </div>

      {/* Stats */}
      <div className="absolute bottom-4 right-4 bg-slate-900/80 backdrop-blur rounded-lg p-3">
        <div className="grid grid-cols-2 gap-4 text-center">
          <div>
            <p className="text-xl font-bold text-white">{mockNodes.length}</p>
            <p className="text-xs text-slate-400">概念节点</p>
          </div>
          <div>
            <p className="text-xl font-bold text-white">{mockEdges.length}</p>
            <p className="text-xs text-slate-400">知识连接</p>
          </div>
        </div>
      </div>

      {/* Selected Node Info */}
      <AnimatePresence>
        {selectedNode && (
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: 20 }}
            className="absolute top-20 right-4 w-64 bg-slate-900/95 backdrop-blur-xl rounded-xl p-4 border border-slate-700"
          >
            <div className="flex items-center gap-3 mb-3">
              <div 
                className="w-3 h-3 rounded-full"
                style={{ backgroundColor: selectedNode.color }}
              />
              <h4 className="font-semibold text-white">{selectedNode.name}</h4>
            </div>
            <div className="space-y-2 text-sm">
              <div className="flex justify-between">
                <span className="text-slate-400">难度等级</span>
                <span className="text-white">L{selectedNode.level}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-400">掌握程度</span>
                <span className="text-emerald-400">{Math.round(selectedNode.mastery * 100)}%</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-400">关联概念</span>
                <span className="text-white">{selectedNode.connections.length}个</span>
              </div>
            </div>
            <Button
              variant="outline"
              size="sm"
              className="w-full mt-3"
              onClick={() => setSelectedNode(null)}
            >
              关闭
            </Button>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Instructions */}
      <div className="absolute bottom-16 left-4 text-xs text-slate-500">
        <p>拖拽旋转 • 滚轮缩放 • 点击查看详情</p>
      </div>
    </Card>
  );
}
